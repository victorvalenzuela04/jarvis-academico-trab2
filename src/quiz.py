"""
quiz.py
-------
Funcionalidade de Aprendizado #2 — Quiz Interativo (active recall).

O quiz é um MODO INTERATIVO separado do agente conversacional. O usuário
inicia com '/quiz <tema>', o sistema gera N perguntas de uma vez e depois
faz uma por vez, avaliando cada resposta.

Este módulo expõe duas operações puras (sem estado próprio):
    - gerar_perguntas(tema, n): cria N perguntas estruturadas em JSON
    - avaliar_resposta(pergunta, resposta_usuario): avalia uma resposta

O loop interativo em si vive em main.py.
"""
import json
import re

from src import llm_client, rag


# Letras válidas para resposta direta
_LETRAS_VALIDAS = {"a", "b", "c", "d"}


def gerar_perguntas(tema: str, n: int = 5) -> dict:
    """
    Gera N perguntas de múltipla escolha sobre um tema, retornando JSON estruturado.

    Returns:
        dict com:
            - 'perguntas': lista de dicts, cada um com
                { numero, enunciado, alternativas: {a,b,c,d}, correta, explicacao }
            - 'tema': tema original
            - 'erro': mensagem se algo deu errado (opcional)
    """
    if not tema or not tema.strip():
        return {"erro": "Tema vazio. Informe um tópico para o quiz."}
    try:
        n = int(n)
    except (TypeError, ValueError):
        n = 5
    n = max(1, min(n, 10))  # entre 1 e 10

    # Mesmo filtro de relevância usado em exercicios.py
    trechos = rag.buscar(tema, top_k=4)
    if not trechos:
        return {"erro": f"Não encontrei material sobre '{tema}'."}
    SIMILARIDADE_MINIMA = 0.35
    if trechos[0]["similaridade"] < SIMILARIDADE_MINIMA:
        return {"erro": f"O tema '{tema}' não está coberto pelos materiais. "
                        f"Melhor similaridade encontrada: {trechos[0]['similaridade']:.2f}"}

    contexto = "\n\n".join(
        f"[Trecho {i+1} — fonte: {t['arquivo']}]\n{t['chunk']}"
        for i, t in enumerate(trechos)
    )

    prompt = f"""Você é um professor universitário criando um quiz para um aluno.

Com base APENAS nos trechos abaixo, crie {n} questão(ões) de múltipla escolha
sobre o tema: "{tema}".

REGRAS:
1. Cada questão tem 4 alternativas (a, b, c, d), APENAS UMA correta.
2. Distratores plausíveis (não óbvios).
3. NÃO invente nada que não esteja nos trechos.
4. Português claro e direto.

RESPONDA APENAS UM JSON VÁLIDO, sem texto antes ou depois, neste formato exato:

{{
  "perguntas": [
    {{
      "numero": 1,
      "enunciado": "Texto da pergunta...",
      "alternativas": {{
        "a": "texto da alternativa a",
        "b": "texto da alternativa b",
        "c": "texto da alternativa c",
        "d": "texto da alternativa d"
      }},
      "correta": "b",
      "explicacao": "Justificativa breve para a resposta correta."
    }}
  ]
}}

=== TRECHOS DE REFERÊNCIA ===
{contexto}

JSON com as {n} perguntas:"""

    bruto = llm_client.chat(
        [{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    # Extrai o primeiro bloco JSON da resposta (defensivo)
    match = re.search(r"\{.*\}", bruto, re.DOTALL)
    if not match:
        return {"erro": "Não consegui interpretar a resposta do LLM (JSON ausente)."}

    try:
        dados = json.loads(match.group())
    except json.JSONDecodeError as e:
        return {"erro": f"JSON inválido retornado pelo LLM: {e}"}

    perguntas = dados.get("perguntas", [])
    if not perguntas:
        return {"erro": "O LLM não retornou nenhuma pergunta."}

    # Validação básica de cada pergunta
    perguntas_validas = []
    for p in perguntas:
        if not all(k in p for k in ("enunciado", "alternativas", "correta")):
            continue
        if set(p["alternativas"].keys()) != _LETRAS_VALIDAS:
            continue
        if p["correta"] not in _LETRAS_VALIDAS:
            continue
        perguntas_validas.append(p)

    if not perguntas_validas:
        return {"erro": "Nenhuma pergunta válida foi gerada pelo LLM."}

    return {"perguntas": perguntas_validas, "tema": tema}


def normalizar_resposta(resposta: str) -> str | None:
    """
    Extrai uma letra (a/b/c/d) da resposta do usuário, se possível.
    Aceita variações como 'a', 'A', 'a)', 'letra a', 'alternativa b'.
    Retorna None se não conseguir identificar uma letra.
    """
    if not resposta:
        return None
    txt = resposta.strip().lower()
    # Caso comum: usuário digita só a letra
    if txt in _LETRAS_VALIDAS:
        return txt
    # Procura primeira ocorrência de a/b/c/d como palavra isolada ou seguida de )
    m = re.search(r"\b([abcd])\b", txt)
    if m:
        return m.group(1)
    return None


def avaliar_resposta(pergunta: dict, resposta_usuario: str) -> dict:
    """
    Avalia a resposta do usuário a uma pergunta.

    Se o usuário respondeu com uma letra (a/b/c/d), faz comparação direta.
    Se respondeu com texto livre, pede ao LLM para comparar semanticamente
    com a alternativa correta.

    Returns dict com:
        - 'acertou': bool
        - 'parcial': bool (verdadeiro só em comparação semântica)
        - 'feedback': texto explicativo
        - 'correta': letra correta
        - 'metodo': 'letra' ou 'semantico'
    """
    correta = pergunta["correta"]
    explicacao = pergunta.get("explicacao", "")
    texto_correto = pergunta["alternativas"][correta]

    letra = normalizar_resposta(resposta_usuario)

    if letra is not None:
        # Comparação direta por letra
        acertou = (letra == correta)
        if acertou:
            feedback = f"✓ Correto! {explicacao}"
        else:
            feedback = (f"✗ Incorreto. A resposta correta é {correta.upper()}) "
                        f"\"{texto_correto}\".\n  {explicacao}")
        return {
            "acertou": acertou,
            "parcial": False,
            "feedback": feedback,
            "correta": correta,
            "metodo": "letra",
        }

    # Texto livre: comparação semântica via LLM
    prompt = f"""Avalie semanticamente a resposta de um aluno em um quiz.

PERGUNTA: {pergunta['enunciado']}

RESPOSTA CORRETA: {texto_correto}

RESPOSTA DO ALUNO: {resposta_usuario}

A resposta do aluno está: CORRETA, PARCIAL ou INCORRETA?

Responda APENAS um JSON neste formato:
{{"classificacao": "CORRETA|PARCIAL|INCORRETA", "comentario": "1-2 frases de feedback"}}"""

    bruto = llm_client.chat(
        [{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    match = re.search(r"\{.*\}", bruto, re.DOTALL)
    classificacao = "INCORRETA"
    comentario = "Não consegui avaliar a resposta automaticamente."
    if match:
        try:
            dados = json.loads(match.group())
            classificacao = dados.get("classificacao", "INCORRETA").upper()
            comentario = dados.get("comentario", comentario)
        except json.JSONDecodeError:
            pass

    acertou = (classificacao == "CORRETA")
    parcial = (classificacao == "PARCIAL")

    icone = "✓" if acertou else ("≈" if parcial else "✗")
    feedback = (f"{icone} {classificacao}. {comentario}\n"
                f"  Resposta esperada: {correta.upper()}) \"{texto_correto}\"\n"
                f"  {explicacao}")

    return {
        "acertou": acertou,
        "parcial": parcial,
        "feedback": feedback,
        "correta": correta,
        "metodo": "semantico",
    }


def gerar_sumario(perguntas: list, respostas: list) -> str:
    """
    Gera um sumário final do quiz (estatísticas + sugestões).

    Args:
        perguntas: lista de perguntas usadas no quiz
        respostas: lista de dicts retornados por avaliar_resposta()
    """
    total = len(respostas)
    if total == 0:
        return "Nenhuma resposta registrada."

    acertos = sum(1 for r in respostas if r["acertou"])
    parciais = sum(1 for r in respostas if r.get("parcial"))
    erros = total - acertos - parciais
    pct = (acertos / total) * 100

    linhas = [
        "═══════════════════════════════════════",
        f"  RESULTADO FINAL",
        "═══════════════════════════════════════",
        f"  ✓ Acertos:    {acertos}/{total}",
        f"  ≈ Parciais:   {parciais}/{total}",
        f"  ✗ Erros:      {erros}/{total}",
        f"  ➤ Aproveitamento: {pct:.0f}%",
        "═══════════════════════════════════════",
    ]

    if pct >= 80:
        linhas.append("Excelente! Você domina bem este tópico.")
    elif pct >= 60:
        linhas.append("Bom desempenho! Revisar os pontos errados consolidará o aprendizado.")
    else:
        linhas.append("Vale a pena revisar este tópico com calma e refazer o quiz.")

    # Lista questões erradas para revisão direcionada
    erradas = [
        i + 1 for i, r in enumerate(respostas)
        if not r["acertou"] and not r.get("parcial")
    ]
    if erradas:
        linhas.append(f"Questões para revisar: {', '.join(map(str, erradas))}")

    return "\n".join(linhas)