# Redes Neurais Artificiais

## Inspiração Biológica

Redes neurais artificiais são modelos computacionais inspirados no
funcionamento do cérebro. A unidade básica é o neurônio artificial
(também chamado de perceptron), que recebe várias entradas, aplica
pesos, soma, passa por uma função de ativação e produz uma saída.

## Estrutura do Neurônio

Matematicamente, o neurônio calcula:

    saida = f(w1*x1 + w2*x2 + ... + wn*xn + b)

onde:
- x são as entradas
- w são os pesos
- b é o viés (bias)
- f é a função de ativação (não linear, como ReLU, sigmoide, tanh)

## Arquitetura em Camadas

Uma rede neural típica tem três tipos de camadas:

- Camada de entrada: recebe os dados brutos.
- Camadas ocultas: realizam transformações intermediárias. Uma rede
  com várias camadas ocultas é chamada de "rede profunda" (deep).
- Camada de saída: produz o resultado final (classe prevista,
  probabilidade, regressão, etc).

Cada neurônio de uma camada se conecta a todos os neurônios da camada
seguinte (em uma rede totalmente conectada / dense).

## Funções de Ativação

- ReLU (Rectified Linear Unit): f(x) = max(0, x). Mais usada hoje,
  rápida e evita saturação para entradas positivas.
- Sigmoide: f(x) = 1/(1+e^(-x)). Útil em saída binária.
- Tanh: f(x) = (e^x - e^(-x)) / (e^x + e^(-x)). Saída entre -1 e 1.
- Softmax: usada na camada de saída para classificação multiclasse,
  produzindo uma distribuição de probabilidade.

## Treinamento: Backpropagation

O treinamento é feito em quatro passos repetidos:

1. Forward pass: passa os dados pela rede e calcula a saída.
2. Cálculo do erro: compara saída prevista com a esperada usando uma
   função de perda (Cross-Entropy para classificação, MSE para
   regressão).
3. Backward pass: calcula o gradiente do erro em relação a cada peso
   usando a regra da cadeia (algoritmo de backpropagation).
4. Atualização: ajusta os pesos na direção oposta ao gradiente, com
   um passo controlado pela taxa de aprendizado (learning rate).

## Otimizadores

O Gradiente Descendente Estocástico (SGD) é o otimizador clássico.
Variantes modernas como Adam, RMSProp e AdaGrad usam taxas de
aprendizado adaptativas e funcionam melhor na maioria dos casos.

## Tipos de Redes

- MLP (Multi-Layer Perceptron): rede densa básica.
- CNN (Convolutional Neural Network): especializada em imagens.
- RNN / LSTM / GRU: para sequências (texto, série temporal).
- Transformer: arquitetura baseada em atenção, padrão atual para
  processamento de linguagem natural e cada vez mais para visão.

## Regularização

Redes neurais tendem ao overfitting. Técnicas para combater:

- Dropout: desliga neurônios aleatoriamente durante o treino.
- L1/L2 regularization: penaliza pesos grandes.
- Early stopping: para o treinamento quando a perda em validação
  começa a subir.
- Data augmentation: amplia o dataset com transformações.
