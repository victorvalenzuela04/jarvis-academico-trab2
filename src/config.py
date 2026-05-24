"""
config.py
---------
Centraliza todas as configurações do JARVIS Acadêmico em um único lugar.
Assim, se você quiser mudar um caminho ou uma chave de API, edita só aqui.
"""
import os

# ====== LLM (Gemma 12B fornecido pelo professor) ======
GEMMA_BASE_URL = "https://llm.liaufms.org/v1/gemma-3-12b-it"
GEMMA_API_KEY  = "Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A"
GEMMA_MODEL    = "google/gemma-3-12b-it"

# ====== Embeddings (modelo multilíngue, suporta português) ======
# Esse modelo roda LOCALMENTE no seu computador (download automático na 1ª vez).
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# ====== Caminhos dos diretórios e arquivos ======
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR     = os.path.join(PROJECT_ROOT, "data")      # documentos do RAG
STORAGE_DIR  = os.path.join(PROJECT_ROOT, "storage")   # agenda e tarefas em JSON
LOGS_DIR     = os.path.join(PROJECT_ROOT, "logs")      # logs de tool calling
INDEX_DIR    = os.path.join(PROJECT_ROOT, "index")     # índice vetorial do RAG

AGENDA_FILE  = os.path.join(STORAGE_DIR, "agenda.json")
TAREFAS_FILE = os.path.join(STORAGE_DIR, "tarefas.json")
LOG_FILE     = os.path.join(LOGS_DIR, "tool_calls.log")
INDEX_FILE   = os.path.join(INDEX_DIR, "indice.pkl")

# ====== Parâmetros do RAG ======
CHUNK_SIZE    = 500   # tamanho aproximado de cada pedaço (em caracteres)
CHUNK_OVERLAP = 50    # sobreposição entre pedaços (preserva contexto)
TOP_K         = 3     # quantos trechos recuperar por pergunta

# ====== Garantir que os diretórios existem ======
for d in [DATA_DIR, STORAGE_DIR, LOGS_DIR, INDEX_DIR]:
    os.makedirs(d, exist_ok=True)
