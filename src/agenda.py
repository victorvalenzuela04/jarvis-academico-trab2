"""
agenda.py
---------
Gerencia a agenda acadêmica (aulas, provas, trabalhos, reuniões).
Armazenamento simples: um JSON em storage/agenda.json.
"""
import json
import os
from datetime import datetime, timedelta

from src import config


def _carregar() -> list:
    if not os.path.exists(config.AGENDA_FILE):
        return []
    with open(config.AGENDA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _salvar(agenda: list) -> None:
    with open(config.AGENDA_FILE, "w", encoding="utf-8") as f:
        json.dump(agenda, f, ensure_ascii=False, indent=2)


def adicionar_evento(titulo: str,
                      data: str,
                      hora: str = "",
                      tipo: str = "aula",
                      descricao: str = "") -> dict:
    """Adiciona um evento. `data` no formato YYYY-MM-DD; `hora` HH:MM."""
    agenda = _carregar()
    novo_id = max((e["id"] for e in agenda), default=0) + 1
    evento = {
        "id": novo_id,
        "titulo": titulo,
        "data": data,
        "hora": hora,
        "tipo": tipo,
        "descricao": descricao,
    }
    agenda.append(evento)
    _salvar(agenda)
    return evento


def consultar_agenda(periodo: str = "hoje") -> list:
    """
    Consulta a agenda. `periodo` aceita:
      - 'hoje', 'amanha', 'semana', 'todos'
      - ou uma data específica no formato YYYY-MM-DD
    """
    agenda = _carregar()
    hoje = datetime.now().date()

    if periodo == "todos":
        return sorted(agenda, key=lambda x: (x["data"], x.get("hora", "")))

    if periodo == "hoje":
        alvo = {hoje.isoformat()}
    elif periodo == "amanha":
        alvo = {(hoje + timedelta(days=1)).isoformat()}
    elif periodo == "semana":
        alvo = {(hoje + timedelta(days=i)).isoformat() for i in range(7)}
    else:
        # Considera que o usuário passou uma data específica
        alvo = {periodo}

    filtrado = [e for e in agenda if e["data"] in alvo]
    return sorted(filtrado, key=lambda x: (x["data"], x.get("hora", "")))


def remover_evento(id_evento: int) -> bool:
    agenda = _carregar()
    nova = [e for e in agenda if e["id"] != id_evento]
    if len(nova) == len(agenda):
        return False
    _salvar(nova)
    return True
