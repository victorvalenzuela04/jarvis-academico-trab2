# Listas Encadeadas

## Conceito

Uma lista encadeada (linked list) é uma estrutura de dados linear em
que cada elemento, chamado de "nó", contém duas partes: o dado em si e
um ponteiro (referência) para o próximo nó. Diferente de um vetor, os
nós não precisam ocupar posições contíguas na memória — eles são
alocados dinamicamente conforme necessário.

## Estrutura básica em C

```c
typedef struct No {
    int dado;
    struct No* proximo;
} No;
```

A lista é representada por um ponteiro para o primeiro nó (cabeça).
Quando esse ponteiro é NULL, a lista está vazia.

## Tipos de listas encadeadas

- Simplesmente encadeada: cada nó aponta apenas para o próximo.
- Duplamente encadeada: cada nó tem dois ponteiros, um para o próximo
  e um para o anterior. Permite percorrer a lista nos dois sentidos.
- Circular: o último nó aponta de volta para o primeiro, formando um
  ciclo. Pode ser simples ou dupla.

## Operações principais e custos

- Inserção no início: O(1) — basta criar um nó novo e fazê-lo apontar
  para o que era a cabeça.
- Inserção no fim: O(n) em listas simples sem ponteiro para o fim;
  O(1) se mantivermos um ponteiro de cauda.
- Busca por valor: O(n) no pior caso, pois precisamos percorrer nó a
  nó até achar.
- Remoção: O(1) se já temos o ponteiro do nó anterior; O(n) se
  precisamos buscá-lo antes.

## Vantagens

- Tamanho dinâmico: cresce e diminui conforme necessário, sem custo
  de realocação.
- Inserções e remoções no meio são O(1) se temos o ponteiro do nó.
- Não desperdiça memória pré-alocada.

## Desvantagens

- Acesso aleatório é O(n): não dá para pular direto ao índice k.
- Maior consumo de memória: cada nó carrega ponteiros extras.
- Pior localidade de cache: os nós podem estar espalhados pela RAM,
  o que prejudica performance comparado a um array contíguo.

## Aplicações típicas

Implementação de pilhas e filas, listas de adjacência em grafos,
tabelas hash com tratamento de colisão por encadeamento (chaining),
sistemas de gerenciamento de memória, históricos de undo/redo,
playlists de música, e qualquer cenário em que o tamanho dos dados é
imprevisível e inserções/remoções frequentes.
