# Introdução ao Aprendizado de Máquina

## O que é Aprendizado de Máquina

Aprendizado de Máquina (Machine Learning, ML) é o subcampo da
Inteligência Artificial dedicado a construir sistemas que aprendem
padrões a partir de dados, em vez de seguir regras explicitamente
programadas. A definição clássica de Tom Mitchell (1997): "Um
programa aprende com a experiência E em relação a uma tarefa T e
medida de desempenho P se seu desempenho em T, medido por P, melhora
com E."

## Os três tipos principais

### Aprendizado Supervisionado

O modelo aprende a partir de exemplos rotulados — pares (entrada,
saída esperada). O objetivo é generalizar para entradas novas. Tem
duas variantes:

- Regressão: a saída é um valor contínuo (preço, temperatura, peso).
- Classificação: a saída é uma categoria (spam/não spam, dígito de
  0 a 9, diagnóstico).

Algoritmos: Regressão Linear, Regressão Logística, Árvores de
Decisão, Random Forest, SVM, KNN, Redes Neurais.

### Aprendizado Não Supervisionado

Os dados não têm rótulos. O modelo encontra estrutura sozinho.
Tarefas comuns:

- Agrupamento (clustering): K-means, DBSCAN, agrupamento hierárquico.
- Redução de dimensionalidade: PCA, t-SNE, UMAP.
- Detecção de anomalias: Isolation Forest, autoencoders.

### Aprendizado por Reforço

Um agente interage com um ambiente, toma ações e recebe recompensas.
Ele aprende uma política que maximiza a recompensa acumulada. Usado
em jogos (AlphaGo, AlphaZero), robótica, condução autônoma e
otimização de cadeias de suprimentos.

## Fluxo Típico de um Projeto de ML

1. Definição do problema e métricas de sucesso.
2. Coleta e exploração dos dados.
3. Pré-processamento: limpeza, tratamento de valores faltantes,
   normalização, encoding de variáveis categóricas.
4. Divisão em conjuntos: treino, validação e teste (típico: 70/15/15
   ou 80/10/10).
5. Escolha do modelo e treinamento.
6. Avaliação no conjunto de validação. Ajuste de hiperparâmetros
   (Grid Search, Random Search, otimização bayesiana).
7. Avaliação final no conjunto de teste.
8. Deploy e monitoramento em produção.

## Overfitting e Underfitting

- Underfitting: o modelo é simples demais para capturar o padrão dos
  dados. Erro alto tanto no treino quanto no teste.
- Overfitting: o modelo decora os dados de treino e não generaliza.
  Erro baixo no treino mas alto no teste.

Combate ao overfitting: mais dados, modelos mais simples,
regularização (L1, L2), dropout (em redes), early stopping,
validação cruzada.

## Métricas Comuns

- Classificação: acurácia, precisão, recall, F1-score, matriz de
  confusão, AUC-ROC.
- Regressão: MAE, MSE, RMSE, R².

A escolha da métrica depende do problema. Em diagnóstico médico, por
exemplo, recall é mais importante que acurácia, pois é pior deixar
um doente passar do que um falso alarme.

## Ferramentas Populares

- Python: scikit-learn (clássicos), TensorFlow e PyTorch (deep
  learning), pandas (dados tabulares), Hugging Face (NLP e modelos
  pré-treinados).
- Ambientes: Jupyter Notebook, Google Colab, Kaggle.
- Tracking de experimentos: MLflow, Weights & Biases.
