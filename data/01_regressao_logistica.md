# Regressão Logística

## Definição

A regressão logística é um modelo estatístico usado para problemas de
classificação binária, ou seja, quando a variável de saída assume apenas
dois valores possíveis (por exemplo: aprovado/reprovado, spam/não spam,
positivo/negativo). Apesar do nome "regressão", ela é um algoritmo de
classificação supervisionada.

## Função Logística (Sigmoide)

O coração do modelo é a função sigmoide, definida como:

    sigmoid(z) = 1 / (1 + e^(-z))

Essa função mapeia qualquer número real para o intervalo (0, 1),
permitindo interpretar a saída como uma probabilidade. O valor z é uma
combinação linear das variáveis de entrada:

    z = w1*x1 + w2*x2 + ... + wn*xn + b

onde wi são os pesos (coeficientes) aprendidos durante o treinamento e
b é o viés (bias).

## Treinamento

O treinamento consiste em encontrar os pesos w e o bias b que melhor
ajustam o modelo aos dados. Para isso, minimizamos uma função de custo
chamada Log Loss (ou Entropia Cruzada Binária):

    L = -[y * log(p) + (1 - y) * log(1 - p)]

onde y é o rótulo verdadeiro (0 ou 1) e p é a probabilidade prevista
pelo modelo. A otimização normalmente é feita com Gradiente Descendente
ou variantes como SGD e Adam.

## Limiar de Decisão

Para transformar a probabilidade p em uma classe, definimos um limiar
(normalmente 0.5):

    se p >= 0.5 -> classe 1
    se p <  0.5 -> classe 0

O limiar pode ser ajustado conforme o problema. Em diagnósticos
médicos, por exemplo, é comum baixar o limiar para aumentar a
sensibilidade.

## Vantagens e Limitações

Vantagens: fácil de interpretar (os pesos indicam importância das
variáveis), rápida para treinar, funciona bem em dados linearmente
separáveis e serve de baseline para problemas complexos.

Limitações: assume relação linear entre as variáveis de entrada e o
log-odds; não captura relações não lineares sem engenharia de atributos
ou kernels; é sensível a outliers e multicolinearidade.

## Extensão Multiclasse

Para mais de duas classes, usamos a Regressão Logística Multinomial
(também chamada de softmax regression), que usa a função softmax no
lugar da sigmoide.
