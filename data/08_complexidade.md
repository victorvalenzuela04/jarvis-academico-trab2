# Complexidade de Algoritmos e Notação Big-O

## O que é análise de complexidade

Analisar a complexidade de um algoritmo significa estimar como seu
tempo de execução (ou uso de memória) cresce conforme o tamanho da
entrada aumenta. O objetivo é prever o desempenho independentemente
do hardware ou da linguagem usada — focando no número de operações.

## Notação Big-O

A notação Big-O (O grande) descreve o limite superior do crescimento
de uma função. Dizemos que um algoritmo é O(f(n)) se, a partir de um
n suficientemente grande, seu tempo de execução é, no máximo, uma
constante vezes f(n). É uma forma de medir o "pior caso" assintótico.

Existem também notações relacionadas:

- Ω (ômega): limite inferior — o algoritmo nunca é mais rápido que
  uma certa função.
- Θ (theta): limite justo — o algoritmo tem o mesmo crescimento que a
  função, tanto por cima quanto por baixo.

## Classes de complexidade comuns

Em ordem crescente de "velocidade de crescimento" (mais lento à
direita, ou seja, pior):

- O(1) — constante: não depende do tamanho da entrada. Exemplos:
  acessar um índice de array, inserir no início de uma lista
  encadeada com cabeça.

- O(log n) — logarítmica: divide o problema pela metade a cada passo.
  Exemplo: busca binária em vetor ordenado.

- O(n) — linear: percorre todos os elementos uma vez. Exemplo: busca
  linear, soma de elementos.

- O(n log n) — log-linear: algoritmos eficientes de ordenação como
  Merge Sort, Quick Sort (caso médio) e Heap Sort.

- O(n²) — quadrática: dois loops aninhados sobre a entrada. Exemplo:
  Bubble Sort, Selection Sort.

- O(n³) — cúbica: três loops aninhados. Exemplo: multiplicação de
  matrizes ingênua, algoritmo de Floyd-Warshall para caminhos
  mínimos.

- O(2^n) — exponencial: cada elemento dobra o trabalho. Exemplo:
  Fibonacci recursivo ingênuo, problema da mochila por força bruta.

- O(n!) — fatorial: todas as permutações. Exemplo: caixeiro viajante
  por força bruta.

## Como analisar um algoritmo

Regras simples para encontrar a complexidade:

1. Sequência de operações: soma das complexidades. Se uma domina, ela
   determina o total.
2. Loops aninhados: multiplica as complexidades.
3. Constantes e termos de menor ordem são descartados: O(3n² + 5n + 7)
   simplifica para O(n²).
4. Recursão: usar o Teorema Mestre ou desenhar a árvore de chamadas.

## Complexidade de espaço

Além do tempo, analisamos a memória usada. Um algoritmo pode ser
rápido mas consumir muita memória (como Merge Sort, que usa O(n)
auxiliar). Algoritmos in-place usam apenas O(1) ou O(log n) de
memória extra.

## Por que isso importa

Um algoritmo O(n²) com 10 mil elementos faz cerca de 100 milhões de
operações — gerenciável. Com 1 milhão de elementos, faz 1 trilhão —
inviável. Já um O(n log n) com 1 milhão faz ~20 milhões: rápido. A
diferença entre algoritmos cresce drasticamente com o tamanho da
entrada, por isso a análise de complexidade é tão importante.
