# Dataset do JARVIS Acadêmico

Este documento descreve o dataset utilizado pelo sistema RAG, conforme
exigido pelo enunciado.

## Origem dos dados

Os 10 documentos desta pasta foram **escritos especificamente para este
trabalho**, com base no conhecimento técnico consolidado dos próprios
autores da dupla e em revisão cruzada com material de IA (Claude da
Anthropic) para garantir correção factual. Não foram copiados de
livros, sites ou apostilas — são sínteses originais em português.

A escolha do conteúdo refletiu duas diretrizes:

1. Tópicos que aparecem nas disciplinas cursadas atualmente
   (Estruturas de Dados, Algoritmos, Banco de Dados, IA).
2. Tópicos que a LLM Gemma 12B provavelmente reconhece bem, para
   facilitar a comparação entre respostas "RAG-only" e "LLM puro" na
   etapa de avaliação (Trabalho 2).

## Tipo de conteúdo

Material acadêmico em formato Markdown (.md), texto contínuo em
português brasileiro. Cada documento aborda um tema único, com
subseções claras (definição, exemplos, complexidade, aplicações, etc),
e tem entre 350 e 700 palavras.

Lista dos documentos:

| Arquivo                          | Tema                              |
|----------------------------------|-----------------------------------|
| 01_regressao_logistica.md        | Regressão Logística               |
| 02_embeddings.md                 | Embeddings                        |
| 03_listas_encadeadas.md          | Listas Encadeadas (TAD)           |
| 04_tabelas_hash.md               | Tabelas Hash e colisões           |
| 05_redes_neurais.md              | Redes Neurais Artificiais         |
| 06_ordenacao.md                  | Algoritmos de Ordenação           |
| 07_recursao.md                   | Recursão                          |
| 08_complexidade.md               | Análise de Complexidade / Big-O   |
| 09_banco_de_dados.md             | Banco de Dados Relacional         |
| 10_machine_learning.md           | Introdução ao Machine Learning    |

## Limitações conhecidas

- Cobertura limitada: 10 tópicos não cobrem o currículo inteiro. Em
  perguntas fora do escopo, o sistema deve admitir que não tem material.
- Profundidade média: cada documento dá uma visão geral, não substitui
  bibliografia formal.
- Sem imagens, diagramas ou fórmulas em LaTeX: apenas texto. Algumas
  equações estão em notação ASCII, o que pode reduzir a qualidade da
  resposta em perguntas matematicamente densas.
- Idioma único (português): consultas em inglês podem retornar chunks
  menos relevantes pela diferença de vocabulário, mesmo com o modelo
  multilíngue de embeddings.
- Sem referências bibliográficas externas: os documentos não citam
  fontes — todos foram escritos do zero pela dupla.

## Estratégia de chunking

A divisão em chunks está implementada em `src/rag.py`, função
`dividir_em_chunks`. Parâmetros padrão (em `src/config.py`):

- `CHUNK_SIZE = 500` caracteres (aproximadamente um parágrafo médio).
- `CHUNK_OVERLAP = 50` caracteres (sobreposição entre chunks
  consecutivos quando um parágrafo é grande demais e precisa ser
  quebrado).

A estratégia funciona em duas etapas:

1. **Primeiro tenta quebrar por parágrafo** (`\n\n` no texto).
   Vamos acumulando parágrafos inteiros num "buffer" enquanto o
   tamanho total ficar abaixo de `CHUNK_SIZE`. Isso preserva o
   contexto natural do texto.
2. **Se um único parágrafo for maior que `CHUNK_SIZE`**, ele é
   quebrado em pedaços de até 500 caracteres com sobreposição de 50.
   A sobreposição garante que frases cortadas no meio ainda apareçam
   integralmente em pelo menos um dos chunks vizinhos.

## Impacto no RAG

Essa estratégia foi escolhida pelos seguintes motivos:

- **Preservar contexto local**: parágrafos contêm uma ideia
  completa. Chunks "por parágrafo" mantêm coesão semântica.
- **Evitar fragmentação excessiva**: chunks muito pequenos (50–100
  caracteres) perdem contexto e fazem o LLM gerar respostas
  superficiais.
- **Evitar chunks grandes demais**: chunks de 2000+ caracteres
  diluem a similaridade — o trecho relevante fica "afogado" em ruído
  e a busca semântica perde precisão.
- **Sobreposição mínima**: 50 caracteres bastam para suavizar bordas
  sem inchar o índice com duplicações.

Para cada chunk, armazenamos um metadado com o nome do arquivo de
origem e o índice ordinal do chunk. Isso permite citar a fonte na
resposta final e facilita o debugging quando o RAG recupera algo
errado.

Esses parâmetros podem ser ajustados em `src/config.py`. Em testes
informais durante o desenvolvimento, chunks de 300 a 700 caracteres
produziram resultados parecidos para este dataset — 500 foi adotado
como meio-termo razoável.
