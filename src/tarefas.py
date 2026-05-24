"""
tarefas.py
----------
CRUD simples de tarefas. Armazena em storage/tarefas.json.
"""
import json
import os
from datetime import datetime

from src import config


def _carregar() -> list:
    if not os.path.exists(config.TAREFAS_FILE):
        return []
    with open(config.TAREFAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _salvar(tarefas: list) -> None:
    with open(config.TAREFAS_FILE, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)


def adicionar_tarefa(descricao: str,
                      prazo: str = "",
                      prioridade: str = "media") -> dict:
    """Adiciona uma nova tarefa. `prazo` no formato YYYY-MM-DD."""
    tarefas = _carregar()
    novo_id = max((t["id"] for t in tarefas), default=0) + 1
    tarefa = {
        "id": novo_id,
        "descricao": descricao,
        "prazo": prazo,
        "prioridade": prioridade,   # alta, media, baixa
        "concluida": False,
        "criada_em": datetime.now().isoformat(timespec="seconds"),
    }
    tarefas.append(tarefa)
    _salvar(tarefas)
    return tarefa


def listar_tarefas(filtro: str = "pendentes") -> list:
    """`filtro` aceita: 'pendentes', 'concluidas', 'todas'."""
    tarefas = _carregar()
    if filtro == "pendentes":
        return [t for t in tarefas if not t["concluida"]]
    if filtro == "concluidas":
        return [t for t in tarefas if t["concluida"]]
    return tarefas


def concluir_tarefa(id_tarefa: int) -> dict | None:
    tarefas = _carregar()
    for t in tarefas:
        if t["id"] == id_tarefa:
            t["concluida"] = True
            t["concluida_em"] = datetime.now().isoformat(timespec="seconds")
            _salvar(tarefas)
            return t
    return None


def remover_tarefa(id_tarefa: int) -> bool:
    tarefas = _carregar()
    nova = [t for t in tarefas if t["id"] != id_tarefa]
    if len(nova) == len(tarefas):
        return False
    _salvar(nova)
    return True
