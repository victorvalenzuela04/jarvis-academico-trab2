"""
planejador.py
-------------
Funcionalidade 3.4 — Planejamento de estudos.

Combina três fontes de informação:
    1. Agenda acadêmica (provas, trabalhos, aulas próximas)
    2. Tarefas pendentes (com prazos)
    3. Tópicos disponíveis nos materiais de estudo

E pede ao Gemma para montar um plano de estudos priorizado.
"""
import json
import os
import re
from datetime import datetime

from src import agenda, config, llm_client, tarefas


def listar_topicos_materiais() -> list[str]:
    """
    Extrai o título principal (primeiro '# H1') de cada documento em /data.
    Usa esses títulos como proxy dos 'tópicos disponíveis para estudar'.

    Ignora READMEs e arquivos não-markdown (consistente com o filtro do RAG).
    """
    topicos: list[str] = []
    for arquivo in sorted(os.listdir(config.DATA_DIR)):
        if not arquivo.lower().endswith(".md"):
            continue
        if arquivo.lower().startswith("readme"):
            continue
        caminho = os.path.join(config.DATA_DIR, arquivo)
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                for linha in f:
                    m = re.match(r"^#\s+(.+)", linha.strip())
                    if m:
                        topicos.append(m.group(1).strip())
                        break
        except OSError:
            # Se o arquivo não puder ser aberto, simplesmente ignora
            continue
    return topicos


def gerar_plano_estudos(periodo: str = "semana", foco: str = "") -> dict:
    """
    Constrói o contexto (agenda + tarefas + tópicos) e pede um plano ao Gemma.

    Args:
        periodo: 'hoje', 'amanha', 'semana', 'todos' ou data YYYY-MM-DD.
        foco: tópico opcional para priorizar no plano.

    Returns:
        dict com o plano em texto e contadores (úteis para debug/logs).
    """
    eventos = agenda.consultar_agenda(periodo=periodo)
    pendentes = tarefas.listar_tarefas("pendentes")
    topicos = listar_topicos_materiais()

    # Monta um "briefing" estruturado para o LLM
    eventos_str = (
        json.dumps(eventos, ensure_ascii=False, indent=2, default=str)
        if eventos else "Nenhum evento agendado neste período."
    )
    tarefas_str = (
        json.dumps(pendentes, ensure_ascii=False, indent=2, default=str)
        if pendentes else "Nenhuma tarefa pendente."
    )
    topicos_str = (
        "\n".join(f"- {t}" for t in topicos)
        if topicos else "Nenhum material indexado."
    )

    hoje_str = datetime.now().strftime("%Y-%m-%d (%A)")
    foco_str = f"\nFOCO ESPECIAL solicitado pelo estudante: {foco}\n" if foco else ""

    prompt = f"""Você é um coach acadêmico experiente.
Com base no contexto abaixo, monte um plano de estudos PRÁTICO e PRIORIZADO.

=== CONTEXTO ===
Data de hoje: {hoje_str}

AGENDA ({periodo}):
{eventos_str}

TAREFAS PENDENTES:
{tarefas_str}

TÓPICOS DISPONÍVEIS NOS MATERIAIS DE ESTUDO:
{topicos_str}
{foco_str}

=== DIRETRIZES PARA O PLANO ===
1. Priorize provas e tarefas com PRAZO MAIS PRÓXIMO.
2. Distribua o estudo em sessões curtas (45 a 90 minutos cada).
3. Sugira QUAIS tópicos estudar em cada sessão, escolhendo entre os
   tópicos disponíveis nos materiais quando fizer sentido.
4. Inclua pelo menos um momento de revisão (active recall ou quiz).
5. Seja realista: não monte um cronograma exaustivo de 10h/dia.
6. Use linguagem direta, motivacional e em português.
7. Formate o plano de forma legível: dia → sessões → tópicos.

Plano de estudos:"""

    plano_texto = llm_client.chat(
        [{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return {
        "plano": plano_texto,
        "eventos_considerados": len(eventos),
        "tarefas_pendentes": len(pendentes),
        "topicos_disponiveis": len(topicos),
        "periodo": periodo,
        "foco": foco,
    }
