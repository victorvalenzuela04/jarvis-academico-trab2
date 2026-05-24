"""
rag.py
------
Sistema RAG (Retrieval-Augmented Generation).

Pipeline:
    1. Ler documentos da pasta /data  (txt, md, pdf)
    2. Dividir em "chunks" (pedaços) com sobreposição
    3. Gerar embeddings (vetores numéricos) com sentence-transformers
    4. Salvar tudo em um índice (pickle) na pasta /index
    5. Na hora de buscar: vetorizar a pergunta e achar os trechos mais
       parecidos via similaridade do cosseno
    6. Mandar os trechos + pergunta ao LLM para gerar a resposta final
"""
import os
import pickle

from src import config

# Imports pesados são feitos de forma "preguiçosa" (lazy) dentro das funções
# que realmente precisam deles. Assim, módulos que só usam `dividir_em_chunks`
# (como os testes) não precisam de numpy ou sentence-transformers instalados.

# Cache em memória para não recarregar a cada chamada
_embedding_model = None
_index = None  # dict com chaves: 'chunks', 'embeddings', 'metadata'


# ------------------------- Modelo de embeddings -------------------------
def get_embedding_model():
    """Carrega o modelo de embeddings (faz download na 1ª vez)."""
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        print("[RAG] Carregando modelo de embeddings (pode demorar na 1ª vez)...")
        _embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _embedding_model


# ------------------------- Leitura de arquivos -------------------------
def ler_documento(caminho: str) -> str | None:
    """Lê o conteúdo de um arquivo .txt, .md ou .pdf. Retorna None se não suportado."""
    ext = os.path.splitext(caminho)[1].lower()

    if ext in (".txt", ".md"):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()

    if ext == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            from PyPDF2 import PdfReader  # fallback
        leitor = PdfReader(caminho)
        return "\n".join((p.extract_text() or "") for p in leitor.pages)

    return None


# ------------------------- Estratégia de chunking -------------------------
def dividir_em_chunks(texto: str,
                       chunk_size: int = None,
                       overlap: int = None) -> list[str]:
    """
    Divide texto em chunks tentando preservar parágrafos.

    Estratégia (importante para o relatório):
    1. Quebra primeiro por parágrafos (\n\n).
    2. Vai juntando parágrafos no mesmo chunk até atingir chunk_size.
    3. Se um parágrafo único for maior que chunk_size, quebra por caracteres
       com sobreposição (overlap) para não perder contexto na borda.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap    = overlap    or config.CHUNK_OVERLAP

    paragrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    chunks: list[str] = []
    buffer = ""

    for p in paragrafos:
        # Cabe no buffer atual?
        if len(buffer) + len(p) + 2 <= chunk_size:
            buffer = (buffer + "\n\n" + p) if buffer else p
            continue

        # Não cabe: descarrega buffer
        if buffer:
            chunks.append(buffer)
            buffer = ""

        # Parágrafo gigante: quebra por caractere
        if len(p) > chunk_size:
            inicio = 0
            while inicio < len(p):
                chunks.append(p[inicio:inicio + chunk_size])
                inicio += chunk_size - overlap
        else:
            buffer = p

    if buffer:
        chunks.append(buffer)
    return chunks


# ------------------------- Construção do índice -------------------------
# Extensões aceitas pelo RAG (mantém em sintonia com ler_documento)
_EXTENSOES_VALIDAS = {".txt", ".md", ".pdf"}


def _eh_indexavel(nome_arquivo: str) -> bool:
    """Decide se um arquivo da pasta /data deve ser indexado pelo RAG.
    Ignora arquivos ocultos, com extensão não suportada, e README
    (que é meta-documentação do dataset, não conteúdo acadêmico)."""
    if nome_arquivo.startswith("."):
        return False
    if nome_arquivo.lower().startswith("readme"):
        return False
    extensao = os.path.splitext(nome_arquivo)[1].lower()
    return extensao in _EXTENSOES_VALIDAS


def construir_indice() -> dict | None:
    """Lê /data, gera chunks + embeddings e salva em /index/indice.pkl."""
    import numpy as np  # noqa: F401  (usado indiretamente pelo modelo)
    modelo = get_embedding_model()

    arquivos = sorted(
        f for f in os.listdir(config.DATA_DIR)
        if os.path.isfile(os.path.join(config.DATA_DIR, f))
        and _eh_indexavel(f)
    )
    if not arquivos:
        print(f"[RAG] Nenhum documento em {config.DATA_DIR}. Adicione arquivos!")
        return None

    chunks: list[str] = []
    metadata: list[dict] = []

    print(f"[RAG] Processando {len(arquivos)} documento(s)...")
    for arquivo in arquivos:
        caminho = os.path.join(config.DATA_DIR, arquivo)
        texto = ler_documento(caminho)
        if not texto:
            print(f"[RAG]   - {arquivo} pulado (formato não suportado)")
            continue
        sub = dividir_em_chunks(texto)
        for i, c in enumerate(sub):
            chunks.append(c)
            metadata.append({"arquivo": arquivo, "chunk_idx": i})
        print(f"[RAG]   - {arquivo}: {len(sub)} chunks")

    if not chunks:
        print("[RAG] Nada foi indexado.")
        return None

    print(f"[RAG] Gerando embeddings para {len(chunks)} chunks...")
    embeddings = modelo.encode(chunks, show_progress_bar=False, convert_to_numpy=True)

    indice = {"chunks": chunks, "embeddings": embeddings, "metadata": metadata}
    with open(config.INDEX_FILE, "wb") as f:
        pickle.dump(indice, f)

    global _index
    _index = indice
    print(f"[RAG] Índice salvo em {config.INDEX_FILE} ({len(chunks)} chunks)")
    return indice


def carregar_indice() -> dict | None:
    """Carrega o índice do disco para memória. Constrói se não existir."""
    global _index
    if _index is not None:
        return _index
    if not os.path.exists(config.INDEX_FILE):
        print("[RAG] Índice não encontrado. Construindo do zero...")
        return construir_indice()
    with open(config.INDEX_FILE, "rb") as f:
        _index = pickle.load(f)
    return _index


# ------------------------- Busca semântica -------------------------
def buscar(query: str, top_k: int = None) -> list[dict]:
    """Retorna os top_k trechos mais relevantes para a query."""
    import numpy as np
    top_k = top_k or config.TOP_K
    indice = carregar_indice()
    if not indice or not indice["chunks"]:
        return []

    modelo = get_embedding_model()
    q_emb = modelo.encode([query], convert_to_numpy=True)[0]

    embeddings = indice["embeddings"]
    # Similaridade do cosseno = (a · b) / (||a|| * ||b||)
    norms = np.linalg.norm(embeddings, axis=1) * np.linalg.norm(q_emb)
    norms[norms == 0] = 1e-10
    sims = np.dot(embeddings, q_emb) / norms

    top_idx = np.argsort(sims)[::-1][:top_k]
    return [
        {
            "chunk": indice["chunks"][i],
            "arquivo": indice["metadata"][i]["arquivo"],
            "similaridade": float(sims[i]),
        }
        for i in top_idx
    ]


def buscar_e_responder(pergunta: str) -> dict:
    """Roda o pipeline completo de RAG e devolve resposta + trechos usados."""
    from src import llm_client

    trechos = buscar(pergunta)
    if not trechos:
        return {
            "resposta": "Não encontrei materiais relevantes para responder.",
            "trechos": [],
        }

    contexto = "\n\n".join(
        f"[Trecho {i+1} — fonte: {t['arquivo']}]\n{t['chunk']}"
        for i, t in enumerate(trechos)
    )

    prompt = f"""Você é um assistente acadêmico. Use APENAS os trechos abaixo para responder.
Se a resposta não estiver nos trechos, diga claramente que essa informação não está nos materiais.

TRECHOS RECUPERADOS:
{contexto}

PERGUNTA: {pergunta}

Resposta (clara, didática, em português):"""

    resposta = llm_client.chat([{"role": "user", "content": prompt}])
    return {"resposta": resposta, "trechos": trechos}
