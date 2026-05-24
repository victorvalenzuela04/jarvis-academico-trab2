"""
jarvis.py
---------
O "cérebro" do agente.

Fluxo de uma mensagem do usuário:
    1. Pergunta -> LLM decide qual FERRAMENTA chamar (em JSON)
    2. Executa a ferramenta (via tools.executar_ferramenta)
    3. LLM transforma o resultado em resposta natural ao usuário
"""
import json
import re
from datetime import datetime

from src import llm_client, tools

SYSTEM_PROMPT = """Você é o JARVIS Acadêmico, um assistente para estudantes universitários.
Sua tarefa é entender o pedido do usuário e DECIDIR qual ferramenta chamar.

{ferramentas}

REGRAS IMPORTANTES:
1. Responda SOMENTE com um JSON, sem nenhum texto antes ou depois.
2. O JSON deve ter exatamente este formato:
   {{"ferramenta": "<nome>", "argumentos": {{<chave>: <valor>, ...}}}}
3. Use 'buscar_material_rag' para perguntas sobre CONTEÚDO acadêmico
   (regressão logística, embeddings, estruturas de dados, algoritmos, etc).
4. Use 'consultar_agenda' para perguntas sobre aulas/provas/compromissos.
5. Use 'listar_tarefas' para listar pendências.
6. Use 'responder_diretamente' para saudações ou conversas curtas.
7. A data de hoje é {hoje}.
"""


# --------------------- Decisão da ferramenta ---------------------
def decidir_ferramenta(mensagem: str, historico: list | None = None) -> dict:
    """Pergunta ao LLM qual ferramenta usar. Retorna {'ferramenta': ..., 'argumentos': {...}}."""
    prompt = SYSTEM_PROMPT.format(
        ferramentas=tools.descricao_ferramentas_para_prompt(),
        hoje=datetime.now().strftime("%Y-%m-%d (%A)"),
    )

    mensagens = [{"role": "system", "content": prompt}]
    if historico:
        mensagens.extend(historico)
    mensagens.append({"role": "user", "content": mensagem})

    bruto = llm_client.chat(mensagens, temperature=0.1)

    # Extrai o primeiro objeto JSON da resposta
    match = re.search(r"\{.*\}", bruto, re.DOTALL)
    if not match:
        return {"ferramenta": "responder_diretamente",
                "argumentos": {"resposta": bruto}}
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {"ferramenta": "responder_diretamente",
                "argumentos": {"resposta": bruto}}


# --------------------- Resposta final ---------------------
def gerar_resposta_final(mensagem: str, ferramenta: str, saida) -> str:
    """Transforma o resultado da ferramenta em uma resposta natural."""
    # Casos triviais: já vem texto pronto
    if ferramenta == "responder_diretamente":
        return saida if isinstance(saida, str) else str(saida)
    if ferramenta == "buscar_material_rag" and isinstance(saida, dict):
        return saida.get("resposta", "")
    if ferramenta == "planejar_estudos" and isinstance(saida, dict):
        return saida.get("plano", "")
    if ferramenta == "gerar_exercicios" and isinstance(saida, dict):
        if "erro" in saida:
            return saida["erro"]
        return saida.get("exercicios", "")

    prompt = f"""O usuário perguntou: "{mensagem}"

Eu chamei a ferramenta '{ferramenta}' e obtive este resultado bruto (JSON):
{json.dumps(saida, ensure_ascii=False, indent=2, default=str)}

Formule uma resposta natural, amigável e em português para o usuário,
sem mencionar JSON nem nomes técnicos."""
    return llm_client.chat([{"role": "user", "content": prompt}], temperature=0.3)


# --------------------- Pipeline completo ---------------------
def processar(mensagem: str, historico: list | None = None) -> dict:
    """Pipeline completo: decide -> executa -> formata."""
    decisao    = decidir_ferramenta(mensagem, historico)
    nome       = decisao.get("ferramenta", "responder_diretamente")
    argumentos = decisao.get("argumentos", {})

    saida    = tools.executar_ferramenta(nome, argumentos)
    resposta = gerar_resposta_final(mensagem, nome, saida)

    return {
        "ferramenta": nome,
        "argumentos": argumentos,
        "saida": saida,
        "resposta": resposta,
    }
