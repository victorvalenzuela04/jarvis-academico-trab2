# ANÁLISE DE FALHAS — JARVIS Acadêmico

Este documento apresenta a análise crítica das principais falhas
identificadas durante a avaliação do JARVIS Acadêmico (ver
`AVALIACAO.md` para o detalhamento dos 12 testes que originaram
estas observações).

Conforme exigência do enunciado do Trabalho 2, foram identificadas
**3 falhas distintas**, cada uma documentada com tipo, causa raiz,
evidência concreta do sistema em execução, e proposta de solução.

Também foi incluída uma **falha bônus**, identificada e **já
corrigida** durante o desenvolvimento, para demonstrar o ciclo
completo de avaliação crítica → identificação → correção.

---

## Sumário das falhas

| # | Falha                                          | Tipo                       | Severidade |
|---|------------------------------------------------|----------------------------|------------|
| 1 | Roteamento incorreto para `responder_diretamente` | Decisão do agente          | Alta       |
| 2 | Alucinação na formatação da resposta              | Geração de linguagem       | Média      |
| 3 | Atalho via histórico de conversação               | Decisão do agente          | Alta       |
| Bônus | Recuperação de chunks irrelevantes no gerador de exercícios | Recuperação (RAG) | — (resolvida) |

---

## Falha 1 — Roteamento incorreto para `responder_diretamente`

**Tipo:** Falha de decisão do agente (tool calling).

### Descrição

Em pelo menos uma das perguntas avaliadas, o LLM Gemma 12B optou
por chamar a ferramenta `responder_diretamente` em vez de
`buscar_material_rag`, embora o tema da pergunta estivesse
plenamente coberto pelos materiais do dataset. Como `responder_
diretamente` não consulta o RAG, o sistema acabou respondendo com
o **conhecimento pré-treinado do modelo**, contornando totalmente
o pipeline de recuperação que é o coração do JARVIS Acadêmico.

### Evidência

Caso 1 — Pergunta 4 da avaliação:

> Usuário: "Compare Merge Sort com Quick Sort, citando vantagens de
> cada um"
>
> JARVIS: [resposta detalhada usando conhecimento geral]
>
>    [ferramenta utilizada: **responder_diretamente**]

O arquivo `06_ordenacao.md` contém uma seção específica sobre cada
algoritmo, com exatamente os pontos pedidos (estabilidade,
complexidade no pior caso, in-place vs auxiliar, etc.). A
ferramenta correta seria `buscar_material_rag`.

### Causa raiz

A decisão de qual ferramenta usar é feita pelo Gemma a partir do
system prompt em `src/jarvis.py`. Ao receber a pergunta, o modelo
"reconhece" que conhece o tema (Merge Sort e Quick Sort são
tópicos clássicos amplamente representados no corpus de
pré-treinamento de qualquer LLM moderna) e toma o atalho de
responder direto, mesmo sendo instruído a consultar os materiais
para perguntas de conteúdo acadêmico.

A instrução atual do prompt diz:
> "Use 'buscar_material_rag' para perguntas sobre CONTEÚDO
> acadêmico"
> "Use 'responder_diretamente' para saudações ou conversas curtas"

A regra é clara, mas o LLM tem uma **propensão a tomar atalhos**
quando "acha que sabe a resposta" — fenômeno conhecido na
literatura de tool calling como *over-eager direct response*.

### Impacto

**Alto**, pelos seguintes motivos:

- Compromete a **rastreabilidade pedagógica** do sistema: o
  estudante não tem como saber se a resposta veio dos seus
  materiais ou do conhecimento geral do modelo.
- **Permite alucinações** que o RAG normalmente filtraria, pois
  sem trechos como referência, o modelo pode misturar fontes
  internas inconsistentes.
- **Viola o critério "Funcionalidade RAG" do enunciado**, que vale
  20% da nota da avaliação.

### Possível solução

Três caminhos, em ordem crescente de complexidade:

1. **Reforçar o system prompt** com regras mais explícitas e
   exemplos negativos. Adicionar:
   > "NUNCA use `responder_diretamente` para perguntas técnicas,
   > algoritmos, definições, comparações entre conceitos, ou
   > qualquer coisa que poderia estar em um livro/apostila —
   > mesmo que você 'saiba a resposta'."

2. **Estreitar drasticamente a função de `responder_diretamente`**
   no catálogo: restringir explicitamente a saudações, pequenas
   conversas e perguntas sobre o próprio JARVIS. Qualquer dúvida
   técnica obrigatoriamente passa pelo RAG.

3. **Implementar um fallback pós-decisão**: se o LLM escolher
   `responder_diretamente` para uma pergunta que contenha palavras-
   chave técnicas (algoritmo, função, complexidade, etc.), forçar
   uma segunda decisão, agora com prompt mais restritivo. Tem
   custo adicional de latência mas elimina o problema.

A correção 1 é a mais barata e provavelmente resolve a maior parte
dos casos. As correções 2 e 3 são candidatas a melhorias futuras.

---

## Falha 2 — Alucinação na formatação da resposta natural

**Tipo:** Falha de geração de linguagem natural (pós-processamento).

### Descrição

Depois de uma ferramenta retornar um resultado estruturado (por
exemplo, um JSON com os dados do evento adicionado), o `jarvis.py`
faz uma segunda chamada ao Gemma para "formatar" esse resultado em
linguagem natural amigável ao usuário. Nessa etapa de formatação,
foi observado que o modelo **insere informação inventada que não
estava na saída original da ferramenta**.

### Evidência

Pergunta 6 da avaliação:

> Usuário: "Adicione uma aula de Inteligência Artificial dia
> 2026-06-15 às 10:00"
>
> JARVIS: "Pronto! Adicionei uma aula de Inteligência Artificial
> para o dia 15 de junho de 2026, às 10h. **Ela será uma
> introdução aos fundamentos da Inteligência Artificial.** Tudo
> certo?"

A ferramenta `adicionar_evento` foi chamada corretamente. O JSON
salvo em `storage/agenda.json` contém apenas os campos pedidos
(título, data, hora, tipo); o campo `descricao` está vazio. Mas
o LLM, ao formatar a resposta natural, **inventou** a descrição
"introdução aos fundamentos da Inteligência Artificial".

### Causa raiz

Na arquitetura atual, o método `gerar_resposta_final()` em
`src/jarvis.py` chama o LLM com um prompt do tipo:

```
O usuário perguntou: "{mensagem}"
Eu chamei a ferramenta '{ferramenta}' e obtive este resultado: {json}
Formule uma resposta natural, amigável e em português...
```

O LLM tem **temperatura 0.3** nesse passo. Mesmo com temperatura
relativamente baixa, ele tende a preencher lacunas com conteúdo
plausível — comportamento padrão de LLMs autoregressivos. Como
nada no prompt o impede de adicionar informação não-solicitada,
ele o faz.

### Impacto

**Médio**, porque:

- A **persistência está correta**: o JSON foi salvo sem o campo
  inventado, então não há contaminação dos dados.
- O usuário pode achar que o sistema entendeu mais do que
  realmente entendeu (descrição que nunca foi pedida).
- Em casos extremos, o LLM poderia inventar detalhes mais
  problemáticos (data ligeiramente diferente, etc.) — embora isso
  não tenha sido observado nos testes.

### Possível solução

Duas abordagens complementares:

1. **Restringir o prompt de formatação** com instruções negativas
   explícitas:
   > "Reescreva o resultado abaixo em linguagem natural. NÃO
   > acrescente nenhuma informação que não esteja no resultado.
   > NÃO interprete, NÃO especule, NÃO complete lacunas."

2. **Para ferramentas com saída simples**, pular a formatação via
   LLM e usar templates Python diretos. Por exemplo, para
   `adicionar_evento`, em vez de chamar o LLM, gerar a resposta
   via f-string:
   ```python
   return (f"Pronto! Adicionei o evento '{titulo}' para "
           f"{data} às {hora}.")
   ```
   Essa abordagem elimina a alucinação pela construção (não há LLM
   para alucinar), mas perde naturalidade. Pode ser usada
   seletivamente para operações críticas (criação de eventos,
   tarefas, etc.).

A solução 1 mantém a flexibilidade e é provavelmente suficiente
para a maioria dos casos.

---

## Falha 3 — Atalho via histórico de conversação

**Tipo:** Falha de decisão do agente (mascaramento de
funcionalidade).

### Descrição

O JARVIS mantém um histórico curto da conversa (últimas 10
mensagens) para dar contexto ao LLM na hora de decidir qual
ferramenta usar. Em pelo menos uma das perguntas avaliadas, esse
histórico se mostrou **uma faca de dois gumes**: o LLM "lembrou"
a resposta a partir das mensagens recentes e **decidiu responder
diretamente, sem chamar a ferramenta que liga ao armazenamento
real**.

Isso é especialmente perigoso porque a **resposta apresentada
está aparentemente correta**, dando a falsa impressão de que tudo
funcionou.

### Evidência

Sequência de Perguntas 8 e 9 da avaliação:

> [Pergunta 8]
> Usuário: "Adicione uma tarefa: preparar apresentação do TCC,
> prazo 2026-06-12, prioridade alta"
>
> JARVIS: "...adicionada... 2026-06-12... prioridade alta."
>    [ferramenta utilizada: adicionar_tarefa] ✓
>
> [Pergunta 9]
> Usuário: "Liste minhas tarefas pendentes"
>
> JARVIS: "Aqui estão suas tarefas pendentes: 1. Preparar
> apresentação do TCC - Prazo: 2026-06-12 - Prioridade: alta"
>    [ferramenta utilizada: **responder_diretamente**] ✗

Na Pergunta 9, o LLM **não consultou** o `storage/tarefas.json` —
ele simplesmente parafraseou a Pergunta 8 que estava no histórico
recente.

### Causa raiz

O histórico de conversação é injetado no prompt de decisão do
LLM por `src/jarvis.py` (variável `historico`). Esse histórico é
útil porque permite ao usuário fazer perguntas curtas
("e a próxima?", "mostra de novo"), mas tem como **efeito colateral**
fazer o LLM ter "memória curta", levando-o a:

- Achar que pode responder a partir do que viu nas mensagens
  recentes (cache implícito).
- Pular a chamada da ferramenta que faria a consulta real ao
  armazenamento.

### Impacto

**Alto**, porque introduz **inconsistência silenciosa**:

- Se houver tarefas adicionadas em **sessões anteriores** (não no
  histórico atual), elas serão ignoradas.
- Se uma tarefa for **modificada por outro processo** (ou pelo
  próprio sistema entre turnos), o LLM não percebe.
- O sistema se comporta como "memória conversacional" em vez de
  "interface ao banco de dados", o que é frágil e
  imprevisível.

A gravidade aumenta com o tempo de uso: quanto mais o sistema é
usado em sessões longas e múltiplas, mais provável é o desalinhamento
entre "o que o LLM lembra" e "o que está realmente armazenado".

### Possível solução

Três caminhos possíveis:

1. **Reforço no system prompt** com regra explícita:
   > "Para QUALQUER operação que leia ou escreva dados (agenda,
   > tarefas, materiais), você DEVE chamar a ferramenta apropriada,
   > MESMO QUE você acredite saber a resposta a partir do histórico
   > de conversa. O histórico pode estar desatualizado."

2. **Filtragem do histórico antes de injetar no prompt**: remover
   das mensagens passadas qualquer conteúdo "estruturado" (listas
   de tarefas, eventos, etc.). Mantém-se apenas o tom da conversa,
   não o conteúdo factual. Isso obriga o LLM a sempre consultar
   a fonte verdadeira.

3. **Solução estrutural**: para perguntas de listagem/consulta,
   **interceptar antes de chamar o LLM**. Se a entrada do usuário
   contém padrões como "liste", "mostre", "quais são", "tenho",
   forçar a chamada da ferramenta correspondente sem passar pelo
   passo de decisão do LLM. É menos elegante mas mais robusto.

A solução 1 é a mais simples e provavelmente funciona em 80% dos
casos. A 2 é mais robusta porém envolve refatoração maior. A 3
quebra parcialmente o paradigma "decisão pela LLM" do enunciado.

---

## Falha bônus (já corrigida) — Recuperação de chunks irrelevantes no gerador de exercícios

**Tipo:** Falha de recuperação (RAG).

### Descrição

Durante o desenvolvimento da funcionalidade "Gerador de Exercícios",
foi observado que quando o usuário pedia exercícios sobre um tema
**não presente nos materiais** (ex: "física quântica"), o sistema
**gerava exercícios sobre tópicos vagamente relacionados** em vez
de avisar que não tinha material adequado.

### Evidência (antes da correção)

> Usuário: "Gere exercícios sobre física quântica"
>
> JARVIS: [gera 3 questões sobre... Big-O, função Softmax e
> complexidade fatorial]
>    [ferramenta utilizada: gerar_exercicios]

O sistema acabou gerando exercícios sobre conteúdo que **estava
nos materiais** (algoritmos), mas que **não correspondia** ao
pedido do usuário (física quântica).

### Causa raiz

A função `rag.buscar()` sempre retorna os top-K chunks
encontrados, **independentemente do score de similaridade**. Em
um pedido sobre "física quântica" contra um dataset 100%
focado em Computação, todos os scores eram baixos (~0.26), mas
mesmo assim os "menos não-relacionados" eram retornados como se
fossem relevantes. O LLM, recebendo esses chunks, criou
exercícios sobre eles, ignorando o tema original.

### Solução implementada

Foi adicionado um **filtro de similaridade mínima (0.35)** no
`src/exercicios.py`:

```python
SIMILARIDADE_MINIMA = 0.35
if trechos[0]["similaridade"] < SIMILARIDADE_MINIMA:
    return {
        "erro": f"Não encontrei material suficientemente "
                f"relevante sobre '{tema}' (melhor similaridade: "
                f"{trechos[0]['similaridade']:.2f}). Os materiais "
                f"disponíveis cobrem tópicos como estruturas de "
                f"dados, algoritmos, IA e banco de dados. "
                f"Tente um tema desses.",
        "tema": tema,
    }
```

O valor de 0.35 foi escolhido empiricamente: chunks acima desse
limiar nos testes anteriores estavam consistentemente relacionados
ao tema; abaixo, eram majoritariamente ruído.

### Evidência (depois da correção)

> Usuário: "Gere exercícios sobre física quântica"
>
> JARVIS: "Não encontrei material suficientemente relevante sobre
> 'física quântica' (melhor similaridade: 0.26). Os materiais
> disponíveis cobrem tópicos como estruturas de dados, algoritmos,
> IA e banco de dados. Tente um tema desses."

O mesmo filtro foi aplicado em `src/quiz.py` para consistência.
Verificou-se também que o caso "bom" (`Gere exercícios sobre
tabelas hash`) continua funcionando — a similaridade ali é ~0.65,
muito acima do limiar.

### Lição aprendida

Esta falha ilustra um princípio importante de sistemas RAG:
**recuperação não-filtrada é pior do que recuperação vazia**. Em
casos em que nenhum chunk é relevante, é melhor avisar honestamente
do que entregar resposta plausível mas errada.

---

## Conclusão da análise de erros

Das 3 falhas identificadas, **duas (Falhas 1 e 3) têm a mesma causa
raiz**: a **camada de decisão do LLM tende a tomar atalhos** quando
acredita poder responder sem ferramenta. Isso indica que o sistema é
sensível ao prompt design, e que melhorias no system prompt
poderiam resolver simultaneamente várias falhas.

A Falha 2 é de natureza diferente: é uma alucinação na fase de
**geração de linguagem natural**, não na fase de decisão.

A Falha Bônus, já corrigida, demonstra que o ciclo "identificar →
analisar → corrigir → validar" é viável dentro do prazo do trabalho.

Estas observações são importantes para o **roadmap do sistema** em
trabalhos futuros: priorizar refinamento do prompt do agente,
seguido de melhorias na fase de formatação de respostas, oferece
o melhor custo-benefício de melhoria de qualidade.
