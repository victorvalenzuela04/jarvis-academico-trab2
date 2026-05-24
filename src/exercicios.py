"""
exercicios.py
-------------
Funcionalidade de Aprendizado #1 — Gerador de Exercícios.

Recebe um tema e uma quantidade desejada de questões, busca trechos
relevantes nos materiais (via RAG) e pede ao Gemma para criar questões
de múltipla escolha com gabarito.

Diferente do RAG normal (que RESPONDE perguntas), aqui o LLM cria
NOVAS perguntas a partir dos trechos.
"""
from src import llm_client, rag


def gerar_exercicios(tema: str, quantidade: int = 3) -> dict:
    """
    Gera questões de múltipla escolha sobre um tema dos materiais.

    Args:
        tema: assunto das questões (ex: 'tabelas hash', 'recursão').
        quantidade: quantas questões gerar. Defaults to 3.

    Returns:
        dict com:
            - 'exercicios': texto formatado com questões + gabarito
            - 'tema': tema original
            - 'quantidade': número solicitado
            - 'trechos': fontes usadas (para debug/log)
            - 'erro': mensagem se algo deu errado (opcional)
    """
    # Validação básica
    if not tema or not tema.strip():
        return {"erro": "Tema vazio. Informe sobre o que gerar exercícios."}
    try:
        quantidade = int(quantidade)
    except (TypeError, ValueError):
        quantidade = 3
    quantidade = max(1, min(quantidade, 10))  # limita entre 1 e 10

    # Busca trechos relevantes nos materiais
    trechos = rag.buscar(tema, top_k=4)
    if not trechos:
        return {
            "erro": f"Não encontrei material sobre '{tema}'. "
                    "Adicione documentos relevantes na pasta data/ e use /reindex.",
            "tema": tema,
        }

    # Filtro de relevância: se nem o melhor trecho atinge o limiar mínimo
    # de similaridade, o tema provavelmente não está coberto pelos materiais.
    # Sem isso, o sistema geraria exercícios sobre tópicos vagamente
    # relacionados (ex: pedir 'física quântica' e receber sobre complexidade).
    SIMILARIDADE_MINIMA = 0.35
    if trechos[0]["similaridade"] < SIMILARIDADE_MINIMA:
        return {
            "erro": f"Não encontrei material suficientemente relevante sobre "
                    f"'{tema}' (melhor similaridade: {trechos[0]['similaridade']:.2f}). "
                    "Os materiais disponíveis cobrem tópicos como estruturas de "
                    "dados, algoritmos, IA e banco de dados. Tente um tema desses.",
            "tema": tema,
        }

    contexto = "\n\n".join(
        f"[Trecho {i+1} — fonte: {t['arquivo']}]\n{t['chunk']}"
        for i, t in enumerate(trechos)
    )

    prompt = f"""Você é um professor universitário criando exercícios para estudantes.

Com base APENAS nos trechos abaixo, crie {quantidade} questão(ões) de múltipla
escolha sobre o tema: "{tema}".

REGRAS:
1. Cada questão deve ter 4 alternativas (a, b, c, d), com APENAS UMA correta.
2. As alternativas erradas (distratores) devem ser plausíveis, não óbvias.
3. NÃO invente conteúdo que não esteja nos trechos.
4. Use linguagem clara e direta, em português.
5. Coloque o GABARITO completo no final, com BREVE justificativa para cada resposta.
6. Numere as questões.

FORMATO DE SAÍDA (siga exatamente):

═══════════════════════════════════════
EXERCÍCIOS — {tema.upper()}
═══════════════════════════════════════

Questão 1: <enunciado>
a) <alternativa>
b) <alternativa>
c) <alternativa>
d) <alternativa>

Questão 2: ...
[etc.]

═══════════════════════════════════════
GABARITO
═══════════════════════════════════════
Questão 1: <letra> — <justificativa breve>
Questão 2: <letra> — <justificativa breve>
[etc.]

=== TRECHOS DE REFERÊNCIA ===
{contexto}

Agora gere as questões:"""

    texto = llm_client.chat(
        [{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return {
        "exercicios": texto,
        "tema": tema,
        "quantidade": quantidade,
        "trechos": [
            {"arquivo": t["arquivo"], "similaridade": t["similaridade"]}
            for t in trechos
        ],
    }
