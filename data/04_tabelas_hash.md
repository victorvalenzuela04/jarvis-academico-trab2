# Tabelas Hash

## Conceito

Uma tabela hash (hash table) é uma estrutura de dados que associa
chaves a valores, oferecendo, em condições ideais, operações de
inserção, busca e remoção em tempo médio O(1). Internamente é um
vetor onde a posição de cada elemento é determinada por uma função
hash aplicada à chave.

## Função Hash

A função hash transforma uma chave (geralmente uma string ou número)
em um índice válido do vetor. Uma boa função hash deve:

- Ser rápida de calcular.
- Distribuir as chaves de forma uniforme entre os índices.
- Ser determinística: a mesma chave sempre produz o mesmo índice.
- Minimizar colisões (chaves diferentes que vão para o mesmo índice).

## Método da Multiplicação de Knuth

Um método clássico para chaves numéricas é a multiplicação de Knuth:

    h(k) = floor(M * (k * A mod 1))

onde M é o tamanho da tabela e A é uma constante irracional. O valor
recomendado por Knuth é A ≈ 0.6180339887 (relacionado à proporção
áurea), que distribui bem as chaves para a maioria dos valores de M.

Para chaves do tipo string, primeiro transformamos a string em um
inteiro, por exemplo somando os códigos ASCII de cada caractere
multiplicados por potências de uma constante (31 é comum):

    valor = c1*31^(n-1) + c2*31^(n-2) + ... + cn

## Tratamento de Colisões

Mesmo com uma boa função hash, colisões são inevitáveis (princípio da
casa dos pombos). Há duas estratégias principais:

### Encadeamento (chaining)

Cada posição da tabela armazena uma lista encadeada com todos os
elementos cuja chave caiu naquele índice. É simples de implementar e
permite que o número de elementos exceda o tamanho da tabela.

### Endereçamento aberto

Se a posição calculada está ocupada, procura-se outra posição segundo
uma sequência de sondagem (probing). Variantes:

- Sondagem linear: testa a próxima posição, depois a seguinte, etc.
- Sondagem quadrática: pula 1, 4, 9, 16... posições.
- Hash duplo: usa uma segunda função hash para definir o passo.

## Fator de Carga

O fator de carga α = n/M (número de elementos / tamanho da tabela)
influencia diretamente o desempenho. Em encadeamento, α pode passar
de 1; em endereçamento aberto, deve ficar abaixo de 0.7 para manter
boa performance. Quando ultrapassa um limite, faz-se rehashing:
cria-se uma tabela maior e reinsere todos os elementos.

## Aplicações

Tabelas hash estão por toda parte: dicionários e mapas das linguagens
modernas (dict em Python, HashMap em Java), caches, indexação de
bancos de dados, contagem de frequências (como contar palavras-chave
em código-fonte), detecção de duplicatas e implementação de conjuntos.
