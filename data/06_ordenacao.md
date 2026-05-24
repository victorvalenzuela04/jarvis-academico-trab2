# Algoritmos de Ordenação

## Por que estudar ordenação

Ordenação é uma das operações mais fundamentais em computação.
Estudar seus algoritmos é essencial porque eles ilustram conceitos
centrais: divisão e conquista, análise de complexidade, recursividade,
in-place vs. fora do lugar, estabilidade e trade-offs entre tempo e
memória.

## Bubble Sort

Compara elementos adjacentes e troca se estiverem fora de ordem,
repetindo até que nenhuma troca seja necessária. É simples de
entender, mas extremamente lento: complexidade O(n²) no pior e caso
médio, O(n) no melhor caso (lista já ordenada com otimização de
flag). Raramente usado na prática.

## Selection Sort

Encontra o menor elemento da parte não ordenada e o coloca no início.
Tem complexidade O(n²) em todos os casos. Faz no máximo O(n) trocas,
o que pode ser útil quando trocas são caras. Não é estável.

## Insertion Sort

Constrói a lista ordenada um elemento por vez, inserindo cada novo
elemento na posição correta entre os já ordenados (como organizar
cartas na mão). Complexidade O(n²) no pior caso, mas O(n) no melhor.
É excelente para listas pequenas ou quase ordenadas, e por isso é
usado como caso base em algoritmos híbridos como Timsort.

## Merge Sort

Algoritmo de divisão e conquista. Divide a lista pela metade
recursivamente até ter listas de tamanho 1, depois faz "merges"
combinando-as ordenadamente. Complexidade garantida O(n log n) em
todos os casos. Estável. Desvantagem: usa O(n) de memória auxiliar.

## Quick Sort

Outro algoritmo de divisão e conquista. Escolhe um elemento como pivô
e particiona a lista em "menores que o pivô" e "maiores que o pivô",
depois ordena cada parte recursivamente. Complexidade média
O(n log n), mas pior caso O(n²) se o pivô for mal escolhido (lista já
ordenada com pivô fixo, por exemplo). Estratégias como escolher um
pivô aleatório ou usar a mediana de três elementos minimizam isso.
É in-place (não exige memória extra significativa) e geralmente o
mais rápido na prática.

## Heap Sort

Usa uma estrutura de dados chamada heap (árvore binária com
propriedade de máximo ou mínimo). Construir o heap leva O(n) e
extrair os elementos um a um leva O(n log n). Complexidade total
O(n log n) no pior caso. É in-place mas não estável.

## Counting Sort, Radix Sort, Bucket Sort

São algoritmos de ordenação não comparativos, que exploram a
estrutura dos dados. Podem atingir complexidade linear O(n) quando
aplicáveis, mas têm restrições: o intervalo de valores deve ser
conhecido e limitado (Counting), os elementos devem ser inteiros ou
strings (Radix), ou a distribuição deve ser uniforme (Bucket).

## Quando usar cada um

- Dados pequenos (< 50): Insertion Sort.
- Garantia de O(n log n): Merge Sort ou Heap Sort.
- Performance na prática: Quick Sort com pivô aleatório.
- Inteiros com intervalo pequeno: Counting ou Radix Sort.
- Linguagens modernas: o sort padrão geralmente é Timsort (Python,
  Java) ou Introsort (C++), híbridos que combinam várias estratégias.
