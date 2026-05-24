"""
llm_client.py
-------------
Camada fina sobre o cliente OpenAI para conversar com o Gemma 12B.
Mantemos isso isolado para, no futuro, trocar o LLM sem mudar o resto.
"""
from openai import OpenAI
from src import config

_client = None  # singleton: criamos só uma vez


def get_client() -> OpenAI:
    """Devolve o cliente OpenAI configurado para o endpoint do Gemma."""
    global _client
    if _client is None:
        _client = OpenAI(
            base_url=config.GEMMA_BASE_URL,
            api_key=config.GEMMA_API_KEY,
        )
    return _client


def chat(messages: list, temperature: float = 0.3) -> str:
    """
    Envia uma lista de mensagens (formato OpenAI) e retorna o texto da resposta.

    `messages` é uma lista de dicionários, ex:
        [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]

    `temperature` controla criatividade: 0 = determinístico, 1 = bem livre.
    """
    client = get_client()
    resp = client.chat.completions.create(
        model=config.GEMMA_MODEL,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content


def ping() -> bool:
    """Teste rápido de conectividade com o LLM. Retorna True se funcionar."""
    try:
        resposta = chat([{"role": "user", "content": "Diga apenas: OK"}])
        return bool(resposta)
    except Exception as e:
        print(f"[LLM] Falha no ping: {e}")
        return False
