# Recursão

## Definição

Recursão é uma técnica em que uma função resolve um problema chamando
a si mesma com uma instância menor do mesmo problema. É uma das ideias
mais elegantes e poderosas da computação, e está diretamente ligada ao
conceito matemático de definição por indução.

## Anatomia de uma função recursiva

Toda função recursiva precisa de duas partes:

1. Caso base: a condição em que a função para de chamar a si mesma e
   retorna um valor diretamente. Sem caso base, a recursão é infinita
   e estoura a pilha (stack overflow).
2. Caso recursivo: a função reduz o problema e chama a si mesma com
   essa versão menor.

## Exemplo clássico: Fatorial

```c
int fatorial(int n) {
    if (n <= 1) return 1;        // caso base
    return n * fatorial(n - 1);  // caso recursivo
}
```

Outra implementação clássica é a sequência de Fibonacci, embora a
versão recursiva ingênua tenha complexidade exponencial O(2^n) por
recalcular os mesmos valores várias vezes — para isso usamos
memoização ou versão iterativa.

## Pilha de Execução

Cada chamada recursiva empilha um novo "quadro de pilha" (stack
frame) com as variáveis locais. Quando o caso base é atingido, as
chamadas começam a retornar, desempilhando os quadros. Por isso
chamadas muito profundas estouram a memória da pilha — em Python o
limite padrão é 1000 chamadas, ajustável com sys.setrecursionlimit().

## Recursão vs Iteração

Toda recursão pode ser convertida em iteração (e vice-versa). A
recursão costuma produzir código mais limpo para problemas com
estrutura naturalmente recursiva (árvores, divisão e conquista),
enquanto iteração é geralmente mais eficiente em memória.

## Recursão de Cauda (Tail Recursion)

Quando a chamada recursiva é a última instrução da função, dizemos
que é recursão de cauda. Alguns compiladores otimizam isso reusando
o mesmo stack frame, evitando o estouro de pilha. C e Python não
otimizam tail calls, mas linguagens funcionais como Haskell e Scheme
sim.

## Divisão e Conquista

Recursão é a base de algoritmos de divisão e conquista, em que um
problema é dividido em subproblemas menores, resolvidos
recursivamente, e depois combinados. Exemplos: Merge Sort, Quick
Sort, busca binária, multiplicação de Karatsuba e a transformada de
Fourier rápida (FFT).

## Backtracking

Recursão também é usada em backtracking, onde a função tenta uma
escolha, chama-se recursivamente, e se a escolha não funcionar,
desfaz e tenta outra. Problemas clássicos: N-rainhas, sudoku, geração
de permutações e labirintos.

## Problemas Comuns

- Esquecer o caso base: recursão infinita.
- Caso base mal posicionado: a função retorna valor errado.
- Recálculo: usar memoização (cache) para evitar repetir trabalho.
- Recursão indireta: A chama B que chama A — também precisa de caso
  base, em algum ponto da cadeia.
