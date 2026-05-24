# Embeddings

## O que são embeddings

Embeddings são representações vetoriais densas de objetos discretos
(palavras, frases, documentos, imagens, usuários, produtos) em um espaço
de dimensão fixa, geralmente entre 64 e 1024 dimensões. A ideia central
é transformar dados de natureza simbólica em vetores numéricos que
preservem relações semânticas: itens "parecidos" devem ficar próximos
no espaço vetorial.

## Por que usar embeddings

Modelos de aprendizado de máquina trabalham com números, não com texto
puro. A abordagem tradicional, one-hot encoding, cria vetores enormes e
esparsos onde cada palavra é independente das outras — "gato" e
"gatinho" ficam totalmente separados. Embeddings resolvem isso: vetores
densos onde palavras semelhantes têm representações próximas.

## Métrica de similaridade

A medida mais comum entre dois embeddings é a similaridade do cosseno:

    sim(a, b) = (a · b) / (||a|| * ||b||)

O resultado fica entre -1 e 1. Valores próximos de 1 indicam alta
similaridade, próximos de 0 indicam ortogonalidade (sem relação) e
próximos de -1 indicam oposição. Outras métricas usadas são distância
euclidiana e produto interno.

## Word Embeddings clássicos

- Word2Vec (Mikolov et al., 2013): aprende vetores prevendo palavras de
  contexto (Skip-gram) ou a palavra central a partir do contexto (CBOW).
- GloVe (Pennington et al., 2014): usa estatísticas globais de
  coocorrência de palavras em um corpus.
- FastText (Bojanowski et al., 2016): representa palavras como soma de
  n-gramas de caracteres, lidando bem com palavras fora do vocabulário.

## Embeddings contextuais

Modelos modernos baseados em Transformers (BERT, GPT, T5) produzem
embeddings contextuais: a mesma palavra recebe vetores diferentes
dependendo do contexto da frase. A palavra "banco" em "banco de praça"
e em "banco do Brasil" terá embeddings distintos.

## Sentence Embeddings

Para representar frases ou parágrafos inteiros, usamos modelos como
Sentence-BERT (SBERT). Eles geram um único vetor por frase, otimizado
para tarefas de similaridade semântica. São a base de sistemas de busca
semântica e de Retrieval-Augmented Generation (RAG).

## Aplicações

Embeddings são pilares da IA moderna: busca semântica, sistemas de
recomendação, classificação de texto, detecção de duplicatas,
agrupamento (clustering), tradução automática, sistemas RAG e bancos de
dados vetoriais como FAISS, Pinecone, Weaviate e Qdrant.
