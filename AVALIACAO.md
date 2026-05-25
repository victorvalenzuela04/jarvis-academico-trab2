# AVALIAÇÃO DO SISTEMA — JARVIS Acadêmico

Este documento apresenta a avaliação sistemática do JARVIS Acadêmico,
conforme exigido pelo item "Avaliação do Sistema" do enunciado do
Trabalho 2.

## 1. Metodologia

Foram executadas **12 perguntas** (acima do mínimo de 10 exigido),
escolhidas para cobrir todas as funcionalidades implementadas:

- 4 perguntas de **RAG** (consulta a materiais)
- 1 pergunta **fora do escopo** do dataset
- 2 perguntas de **agenda**
- 2 perguntas de **tarefas**
- 1 pergunta de **planejamento de estudos** (Funcionalidade 3.4)
- 1 pergunta de **geração de exercícios**
- 1 pergunta de **iniciar quiz**

Para cada pergunta foram registrados:
- A pergunta enviada
- A ferramenta escolhida pelo LLM
- Os documentos / trechos recuperados (quando aplicável)
- A resposta apresentada
- Uma classificação: **Correta**, **Parcial** ou **Incorreta**
- Uma análise crítica curta

Todos os testes foram executados em uma única sessão do JARVIS, no
mesmo ambiente em que será gravado o vídeo de entrega.

## 2. Resumo dos resultados

| #  | Pergunta                                              | Ferramenta              | Classificação |
|----|-------------------------------------------------------|-------------------------|---------------|
| 1  | "O que é regressão logística?"                        | `buscar_material_rag`   | Correta       |
| 2  | "Como funciona o método da multiplicação de Knuth?"   | `buscar_material_rag`   | Correta       |
| 3  | "O que é recursão de cauda e em que linguagens..."    | `buscar_material_rag`   | Correta       |
| 4  | "Compare Merge Sort com Quick Sort..."                | `responder_diretamente` | **Incorreta** |
| 5  | "O que é a teoria da relatividade de Einstein?"       | `responder_diretamente` | **Parcial**   |
| 6  | "Adicione uma aula de IA dia 2026-06-15 às 10:00"     | `adicionar_evento`      | **Parcial**   |
| 7  | "O que tenho na agenda essa semana?"                  | `consultar_agenda`      | Correta       |
| 8  | "Adicione uma tarefa: preparar apresentação do TCC"   | `adicionar_tarefa`      | Correta       |
| 9  | "Liste minhas tarefas pendentes"                      | `responder_diretamente` | **Incorreta** |
| 10 | "Monte um plano de estudos para essa semana"          | `planejar_estudos`      | Correta       |
| 11 | "Gere 3 exercícios sobre redes neurais"               | `gerar_exercicios`      | Correta       |
| 12 | "Quero fazer um quiz sobre listas encadeadas"         | `sugerir_quiz`          | Correta       |

**Totais:** Correta: 8/12 (67%) · Parcial: 2/12 (17%) · Incorreta: 2/12 (17%)

## 3. Avaliação detalhada

---

### Pergunta 1 — "O que é regressão logística?"

**Ferramenta utilizada:** `buscar_material_rag`

**Documentos recuperados (top-3 por similaridade do cosseno):**

| # | Arquivo                       | Similaridade |
|---|-------------------------------|--------------|
| 1 | `01_regressao_logistica.md`   | 0.639        |
| 2 | `07_recursao.md`              | 0.455        |
| 3 | `07_recursao.md`              | 0.429        |

**Resposta:**
> A regressão logística é um modelo estatístico usado para problemas
> de classificação binária. Isso significa que ela é utilizada quando
> a variável que se deseja prever pode assumir apenas dois valores
> possíveis, como "aprovado/reprovado" ou "spam/não spam". Apesar do
> nome, é um algoritmo de classificação supervisionada. O elemento
> central desse modelo é a função sigmoide.

**Classificação:** ✅ **Correta**

**Análise:** O top-1 retornado tem alta similaridade (0.64) e é o
documento certo. Os chunks 2 e 3 (sobre recursão) têm similaridade
mais baixa e não foram aproveitados pelo LLM na resposta — o modelo
ignorou ruído corretamente. Resposta concisa e fiel ao material.

---

### Pergunta 2 — "Como funciona o método da multiplicação de Knuth para tabelas hash?"

**Ferramenta utilizada:** `buscar_material_rag`

**Documentos recuperados:**

| # | Arquivo                | Similaridade |
|---|------------------------|--------------|
| 1 | `04_tabelas_hash.md`   | 0.653        |
| 2 | `04_tabelas_hash.md`   | 0.612        |
| 3 | `04_tabelas_hash.md`   | 0.543        |

**Resposta (resumida):**
> O método da multiplicação de Knuth é um método clássico... funciona
> assim: h(k) = floor(M * (k * A mod 1)), onde h(k) é o índice
> calculado, M é o tamanho do vetor, A é uma constante de
> multiplicação (geralmente um número irracional entre 0 e 1)...

**Classificação:** ✅ **Correta**

**Análise:** Todos os 3 trechos vieram do arquivo certo
(`04_tabelas_hash.md`), com similaridades altas e consistentes (entre
0.54 e 0.65). A fórmula está correta. Pequena perda de informação: o
material original cita o valor recomendado por Knuth (A ≈ 0.6180339887,
ligado à proporção áurea), mas o LLM simplificou para "constante
irracional entre 0 e 1". Aceitável.

---

### Pergunta 3 — "O que é recursão de cauda e em que linguagens ela é otimizada?"

**Ferramenta utilizada:** `buscar_material_rag`

**Documentos recuperados:**

| # | Arquivo             | Similaridade |
|---|---------------------|--------------|
| 1 | `07_recursao.md`    | 0.690        |
| 2 | `07_recursao.md`    | 0.636        |
| 3 | `07_recursao.md`    | 0.498        |

**Resposta:**
> Recursão de cauda ocorre quando a chamada recursiva é a última
> instrução de uma função. Algumas linguagens, como Haskell e Scheme,
> otimizam a recursão de cauda, reutilizando o mesmo "stack frame"
> para evitar o estouro de pilha. No entanto, C e Python não otimizam
> tail calls.

**Classificação:** ✅ **Correta**

**Análise:** Resposta exemplar. Todos os trechos vieram do arquivo
correto, a definição está precisa e as linguagens citadas (Haskell,
Scheme, C, Python) batem 100% com o material original. Caso ideal
de RAG funcionando como esperado.

---

### Pergunta 4 — "Compare Merge Sort com Quick Sort, citando vantagens de cada um"

**Ferramenta utilizada:** `responder_diretamente` ⚠️

**Documentos recuperados:** Nenhum (a ferramenta `responder_diretamente`
não consulta o RAG).

**Resposta:** Resposta longa, detalhada, com sub-seções para cada
algoritmo (Como funciona / Vantagens / Desvantagens) e resumo final.
Conteúdo tecnicamente correto: cita estabilidade do Merge Sort,
desempenho O(n log n) garantido vs. O(n²) no pior caso do Quick Sort,
in-place vs uso de O(n) auxiliar etc.

**Classificação:** ❌ **Incorreta**

**Análise:** Embora o **conteúdo da resposta esteja correto**, esta
é a **classificação mais grave** dos 12 testes — pelo seguinte motivo:

O JARVIS Acadêmico é projetado para responder com base **nos
materiais do estudante**, não no conhecimento geral pré-treinado do
LLM. Esta pergunta era perfeitamente coberta pelo arquivo
`06_ordenacao.md`, que contém seções específicas sobre Merge Sort e
Quick Sort com exatamente os pontos pedidos.

Ao escolher `responder_diretamente`, o LLM contornou o pipeline RAG
e respondeu por conta própria. Isso viola a premissa pedagógica do
sistema: o aluno **não fica sabendo** se o conteúdo veio dos seus
materiais ou da memória do modelo, comprometendo a confiabilidade
da resposta como ferramenta de estudo.

Esta falha aparece na análise de erros (ver `ERROS.md`) como caso
de **falha de roteamento de ferramenta**.

---

### Pergunta 5 — "O que é a teoria da relatividade de Einstein?"

**Ferramenta utilizada:** `responder_diretamente` ⚠️

**Documentos recuperados:** Nenhum.

**Resposta:** Resposta extensa e tecnicamente correta sobre as duas
teorias da relatividade (Restrita e Geral), com postulados,
consequências, equação E=mc², ondas gravitacionais etc.

**Classificação:** 🟡 **Parcial**

**Análise:** Caso diferente do anterior. Aqui o tópico está **fora
do dataset acadêmico** do estudante — não há material sobre física
no `data/`. Existem duas escolhas defensáveis para o sistema:

1. **Caminho atual:** `responder_diretamente` com o conhecimento
   geral do LLM. Vantagem: o estudante recebe uma resposta útil.
   Desvantagem: ele não sabe que está usando o "conhecimento extra"
   do LLM, e não os materiais.
2. **Caminho mais "puro":** tentar `buscar_material_rag`, falhar (a
   similaridade ficaria abaixo do limiar 0.35), e responder que o
   tema não está nos materiais.

O JARVIS optou pelo caminho (1). A classificação é **Parcial**
porque a resposta é útil e correta, mas o sistema deveria avisar
explicitamente que está respondendo "fora dos materiais", para
respeitar o paradigma acadêmico do projeto.

---

### Pergunta 6 — "Adicione uma aula de Inteligência Artificial dia 2026-06-15 às 10:00"

**Ferramenta utilizada:** `adicionar_evento`

**Resposta:**
> Pronto! Adicionei uma aula de Inteligência Artificial para o dia
> 15 de junho de 2026, às 10h. **Ela será uma introdução aos
> fundamentos da Inteligência Artificial.** Tudo certo?

**Classificação:** 🟡 **Parcial**

**Análise:** A ferramenta foi chamada corretamente, os dados foram
persistidos em `storage/agenda.json` com os parâmetros certos
(título, data, hora). No entanto, **a resposta apresentada inventou
uma descrição** ("introdução aos fundamentos da Inteligência
Artificial") que nunca foi pedida pelo usuário.

Esse comportamento é a **alucinação do LLM na fase de geração de
linguagem natural** — o passo em que `jarvis.py` recebe a saída
estruturada da ferramenta e pede ao Gemma para "formatar para o
usuário". O modelo enriqueceu a resposta com informação inventada.

A persistência está correta (o JSON foi salvo sem o campo
`descricao`), mas a apresentação ao usuário pode induzir a falsa
impressão de que algo foi registrado.

---

### Pergunta 7 — "O que tenho na agenda essa semana?"

**Ferramenta utilizada:** `consultar_agenda`

**Resposta:**
> Parece que sua agenda está livre essa semana! Não tenho nenhum
> compromisso agendado para você. Aproveite! 😊

**Classificação:** ✅ **Correta**

**Análise:** Resposta **logicamente correta**. A aula adicionada na
Pergunta 6 está marcada para **15 de junho de 2026**, mas a data do
teste é **24 de maio de 2026** — ou seja, "essa semana" (24/05 a
30/05) realmente não contém nenhum evento. O sistema filtrou
corretamente por data.

Esse é um caso interessante: poderia parecer um erro à primeira
vista ("eu acabei de adicionar uma aula!"), mas a lógica de
janela temporal funcionou exatamente como esperada.

---

### Pergunta 8 — "Adicione uma tarefa: preparar apresentação do TCC, prazo 2026-06-12, prioridade alta"

**Ferramenta utilizada:** `adicionar_tarefa`

**Resposta:**
> Ok, a tarefa "Preparar apresentação do TCC" foi adicionada! O
> prazo é 12 de junho de 2026 e está marcada como prioridade alta.

**Classificação:** ✅ **Correta**

**Análise:** Todos os 3 campos extraídos pelo LLM batem com o pedido:
descrição, prazo (formato YYYY-MM-DD correto) e prioridade. Tarefa
persistida em `storage/tarefas.json` com `id: 1` e `concluida: false`.
Caso ideal.

---

### Pergunta 9 — "Liste minhas tarefas pendentes"

**Ferramenta utilizada:** `responder_diretamente` ⚠️

**Documentos recuperados:** Nenhum (e nenhuma tool de tarefas chamada).

**Resposta:**
> Aqui estão suas tarefas pendentes:
> 1. Preparar apresentação do TCC
>    - Prazo: 2026-06-12
>    - Prioridade: alta

**Classificação:** ❌ **Incorreta**

**Análise:** A **resposta apresentada está correta por coincidência**,
mas a ferramenta usada está errada. O LLM deveria ter chamado
`listar_tarefas`, que lê o arquivo `storage/tarefas.json` e devolve a
lista atual. Em vez disso, o LLM "lembrou" a tarefa que tinha
acabado de ser adicionada na Pergunta 8 (estava no histórico de
conversação) e respondeu a partir dessa memória.

Por que isso é um problema sério:
- Se houvesse tarefas adicionadas **em sessões anteriores**, o LLM
  não as veria — só as persistidas no JSON.
- Se a tarefa atual fosse modificada por outro processo, o LLM
  responderia desatualizado.
- O sistema deixa de funcionar como "interface ao banco de dados" e
  vira "respondedor de histórico", o que é frágil.

Essa falha também aparece em `ERROS.md`.

---

### Pergunta 10 — "Monte um plano de estudos para essa semana"

**Ferramenta utilizada:** `planejar_estudos`

**Resposta:** Plano de estudos completo, organizado em 3 semanas
(24/05 a 12/06, fechando exatamente no prazo da tarefa do TCC),
distribuído em sessões de 45-90 minutos, com pausas e momento de
descanso. Inclui tópicos do dataset (Aprendizado de Máquina,
Big-O, Banco de Dados, Listas Encadeadas, Tabelas Hash, Regressão
Logística).

**Classificação:** ✅ **Correta**

**Análise:** Resposta excelente do ponto de vista qualitativo. O
sistema combinou as três fontes (agenda vazia para essa semana,
1 tarefa pendente com prazo distante, 10 tópicos disponíveis) e
priorizou o TCC corretamente. Aponta tópicos reais dos materiais,
não inventou novos tópicos. Estrutura clara e linguagem motivacional
adequada.

---

### Pergunta 11 — "Gere 3 exercícios sobre redes neurais"

**Ferramenta utilizada:** `gerar_exercicios`

**Resposta:** 3 questões de múltipla escolha (a/b/c/d cada),
sobre viés (bias), camadas ocultas e rede totalmente conectada
(dense). Gabarito completo no final com justificativa para cada
resposta correta.

**Classificação:** ✅ **Correta**

**Análise:** Formato esperado seguido fielmente. Distratores
plausíveis (não obviamente errados). Todas as respostas corretas
podem ser confirmadas no `05_redes_neurais.md`. Gabarito com
justificativas curtas e referência implícita ao material.

---

### Pergunta 12 — "Quero fazer um quiz sobre listas encadeadas"

**Ferramenta utilizada:** `sugerir_quiz`

**Resposta:**
> Para iniciar o quiz interativo sobre 'listas encadeadas', digite
> o comando:
>     /quiz listas encadeadas
> O sistema vai gerar perguntas e avaliar suas respostas uma a uma,
> com feedback no final.

**Classificação:** ✅ **Correta**

**Análise:** O sistema reconheceu corretamente a **intenção de fazer
um quiz interativo** (diferente de gerar uma lista de exercícios
estática) e orientou o usuário a usar o comando `/quiz`. O design
de separar o quiz do tool calling normal (porque envolve estado
entre turnos) foi explicado ao usuário sem usar jargão técnico.

---

## 4. Análise quantitativa

```
Total de testes:    12
Corretas:            8  (66.7%)
Parciais:            2  (16.7%)
Incorretas:          2  (16.7%)

Por ferramenta:
- buscar_material_rag:    3/3 corretas    (100%)
- responder_diretamente:  0/3 corretas    (0%)  ← problemática
- adicionar_evento:       0/1 corretas    (parcial — alucinação)
- consultar_agenda:       1/1 corretas    (100%)
- adicionar_tarefa:       1/1 corretas    (100%)
- planejar_estudos:       1/1 corretas    (100%)
- gerar_exercicios:       1/1 corretas    (100%)
- sugerir_quiz:           1/1 corretas    (100%)
```

## 5. Análise qualitativa

**Pontos fortes:**

1. **RAG funciona muito bem para perguntas dentro do escopo.** Os
   três testes que usaram `buscar_material_rag` foram 100% corretos,
   com similaridades altas (top-1 sempre acima de 0.63) e respostas
   fiéis ao material.
2. **Persistência (agenda/tarefas/plano) é confiável.** Os campos são
   extraídos corretamente pelo LLM, datas no formato YYYY-MM-DD são
   respeitadas, e o JSON é salvo corretamente.
3. **Geração estruturada (exercícios, plano de estudos) supera as
   expectativas.** O LLM segue formatos rigorosos e mantém coerência
   com o dataset disponível.

**Pontos fracos:**

1. **`responder_diretamente` é uma rota de escape problemática.** Em
   3 ocasiões o LLM preferiu responder com o próprio conhecimento em
   vez de chamar a ferramenta correta. Isso comprometeu a coerência
   pedagógica do sistema.
2. **Alucinação na geração de resposta natural.** A Pergunta 6
   mostrou que o passo final do pipeline (transformar saída da
   ferramenta em texto) pode introduzir informação não solicitada.
3. **Dependência do histórico de conversação como atalho.** A
   Pergunta 9 mostrou que o LLM pode "burlar" a chamada de ferramenta
   se a resposta está no contexto recente — o que dá uma falsa
   sensação de funcionamento.

## 6. Conclusão

O JARVIS Acadêmico atinge **67% de acerto pleno** em 12 testes
diversos, com mais 17% de respostas parcialmente úteis. As **3
falhas identificadas** (2 incorretas + 1 alucinação parcial) são
todas relacionadas à **camada de decisão do LLM**, não às
ferramentas em si — o que indica que o pipeline base (RAG,
persistência, lógica de domínio) é sólido, e que melhorias futuras
devem focar em **reforçar a obediência do LLM ao prompt do agente**.

As falhas concretas estão detalhadas no documento `ERROS.md`.
