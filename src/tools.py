"""
tools.py
--------
Define as ferramentas (tools) que o agente JARVIS pode chamar, executa
a ferramenta solicitada e registra logs (ferramenta, entrada, saída).

A LLM decide qual chamar — a lógica de decisão fica em jarvis.py.
Aqui só catalogamos e despachamos.
"""
import json
import logging
from typing import Any

from src import config, agenda, tarefas, rag


# ===================== Logger de tool calling =====================
logger = logging.getLogger("tool_calls")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
    logger.addHandler(handler)


# ===================== Catálogo de ferramentas =====================
# Cada item descreve a ferramenta para o LLM (em português, ele entende bem).
FERRAMENTAS = [
    {
        "nome": "consultar_agenda",
        "descricao": "Consulta eventos da agenda. Use para perguntas sobre aulas, provas, "
                     "trabalhos ou compromissos do estudante.",
        "parametros": {
            "periodo": "Pode ser: 'hoje', 'amanha', 'semana', 'todos', ou uma data YYYY-MM-DD"
        },
    },
    {
        "nome": "adicionar_evento",
        "descricao": "Adiciona um novo evento na agenda acadêmica.",
        "parametros": {
            "titulo":   "Título do evento, ex: 'Prova de Cálculo'",
            "data":     "Data no formato YYYY-MM-DD",
            "hora":     "Hora HH:MM (opcional)",
            "tipo":     "'aula' | 'prova' | 'trabalho' | 'reuniao' (opcional)",
            "descricao":"Descrição opcional",
        },
    },
    {
        "nome": "listar_tarefas",
        "descricao": "Lista as tarefas do estudante.",
        "parametros": {
            "filtro": "'pendentes' | 'concluidas' | 'todas'"
        },
    },
    {
        "nome": "adicionar_tarefa",
        "descricao": "Adiciona uma nova tarefa à lista do estudante.",
        "parametros": {
            "descricao": "Descrição da tarefa",
            "prazo":     "YYYY-MM-DD (opcional)",
            "prioridade":"'alta' | 'media' | 'baixa' (opcional)",
        },
    },
    {
        "nome": "concluir_tarefa",
        "descricao": "Marca uma tarefa como concluída.",
        "parametros": {"id": "ID numérico da tarefa"},
    },
    {
        "nome": "remover_tarefa",
        "descricao": "Remove uma tarefa da lista.",
        "parametros": {"id": "ID numérico da tarefa"},
    },
    {
        "nome": "buscar_material_rag",
        "descricao": "Busca informações nos materiais de estudo (PDFs, notas, textos) "
                     "e responde a pergunta com base neles. Use para perguntas sobre "
                     "conteúdo de matéria (regressão, embeddings, algoritmos, etc).",
        "parametros": {"pergunta": "A pergunta a ser respondida com base nos materiais"},
    },
    {
        "nome": "planejar_estudos",
        "descricao": "Monta um plano de estudos personalizado combinando a agenda, "
                     "as tarefas pendentes e os tópicos disponíveis nos materiais. "
                     "Use quando o usuário pedir um plano, planejamento, cronograma "
                     "ou quiser saber 'o que estudar', 'por onde começar', "
                     "'como me preparar para a prova'.",
        "parametros": {
            "periodo": "Janela de tempo: 'hoje', 'amanha', 'semana', 'todos' "
                       "ou data YYYY-MM-DD",
            "foco":    "Tópico para priorizar no plano (opcional, ex: 'algoritmos')",
        },
    },
    {
        "nome": "responder_diretamente",
        "descricao": "Use quando puder responder sem precisar de nenhuma fonte "
                     "(saudações, pequenas conversas, perguntas sobre o próprio JARVIS).",
        "parametros": {"resposta": "Texto da resposta direta"},
    },
]


def descricao_ferramentas_para_prompt() -> str:
    """Converte o catálogo em texto que vai dentro do system prompt do LLM."""
    linhas = ["FERRAMENTAS DISPONÍVEIS:"]
    for f in FERRAMENTAS:
        params = ", ".join(f"{k} ({v})" for k, v in f["parametros"].items())
        linhas.append(f"\n• {f['nome']}: {f['descricao']}")
        linhas.append(f"  parâmetros: {params}")
    return "\n".join(linhas)


# ===================== Despachante (dispatcher) =====================
def executar_ferramenta(nome: str, argumentos: dict) -> Any:
    """Executa a ferramenta nomeada com os argumentos. Loga sempre."""
    entrada_log = {"ferramenta": nome, "argumentos": argumentos}
    try:
        if nome == "consultar_agenda":
            saida = agenda.consultar_agenda(argumentos.get("periodo", "hoje"))

        elif nome == "adicionar_evento":
            saida = agenda.adicionar_evento(
                titulo    = argumentos["titulo"],
                data      = argumentos["data"],
                hora      = argumentos.get("hora", ""),
                tipo      = argumentos.get("tipo", "aula"),
                descricao = argumentos.get("descricao", ""),
            )

        elif nome == "listar_tarefas":
            saida = tarefas.listar_tarefas(argumentos.get("filtro", "pendentes"))

        elif nome == "adicionar_tarefa":
            saida = tarefas.adicionar_tarefa(
                descricao  = argumentos["descricao"],
                prazo      = argumentos.get("prazo", ""),
                prioridade = argumentos.get("prioridade", "media"),
            )

        elif nome == "concluir_tarefa":
            saida = tarefas.concluir_tarefa(int(argumentos["id"]))

        elif nome == "remover_tarefa":
            saida = tarefas.remover_tarefa(int(argumentos["id"]))

        elif nome == "buscar_material_rag":
            saida = rag.buscar_e_responder(argumentos["pergunta"])

        elif nome == "planejar_estudos":
            from src import planejador
            saida = planejador.gerar_plano_estudos(
                periodo = argumentos.get("periodo", "semana"),
                foco    = argumentos.get("foco", ""),
            )

        elif nome == "responder_diretamente":
            saida = argumentos.get("resposta", "")

        else:
            saida = {"erro": f"Ferramenta desconhecida: {nome}"}

        logger.info(json.dumps(
            {"entrada": entrada_log, "saida": _resumir(saida)},
            ensure_ascii=False, default=str,
        ))
        return saida

    except Exception as e:
        logger.error(json.dumps(
            {"entrada": entrada_log, "erro": str(e)},
            ensure_ascii=False,
        ))
        return {"erro": str(e)}


def _resumir(obj: Any, limite: int = 500) -> str:
    """Resume uma saída para caber no log sem poluir o arquivo."""
    s = json.dumps(obj, ensure_ascii=False, default=str)
    return s if len(s) <= limite else s[:limite] + "...[truncado]"
