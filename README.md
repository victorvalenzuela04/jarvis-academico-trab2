# JARVIS Acadêmico — Trabalho 2 

> Assistente pessoal inteligente para estudantes universitários, com **RAG**, **Tool Calling**, **Planejador de Estudos**, **Gerador de Exercícios** e **Quiz Interativo**, tudo orquestrado pelo LLM **Gemma 12B**.

Trabalho prático da disciplina de Inteligência Artificial — **Entrega 2** (Funcionalidade 3.4 + Melhorias de Aprendizado + Avaliação + Análise de Erros).

> 📌 O Trabalho 1 (Funcionalidades 3.1, 3.2 e 3.3) está em um repositório separado: [jarvis-academico](https://github.com/victorvalenzuela04/jarvis-academico). Esta entrega expande aquele projeto com novas funcionalidades, avaliação sistemática e análise crítica.

---

## Visão geral

O JARVIS Acadêmico é um agente conversacional em Python que ajuda estudantes a:

- 💬 Consultar materiais de estudo via **RAG** (Retrieval-Augmented Generation)
- 📅 Gerenciar uma **agenda acadêmica** (aulas, provas, trabalhos)
- ✅ Gerenciar uma **lista de tarefas** (adicionar, listar, concluir, remover)
- 🗓️ Receber um **plano de estudos personalizado** combinando agenda + tarefas + materiais  **(NOVO)**
- 📝 Gerar **exercícios de múltipla escolha** sobre qualquer tópico do dataset  **(NOVO)**
- 🎯 Fazer **quizzes interativos** com avaliação automática das respostas  **(NOVO)**

A "inteligência" do sistema vem da LLM **Gemma 12B**, que decide autonomamente qual **ferramenta** chamar para cada pergunta do usuário — não há lógica fixa de roteamento.

---

## O que mudou em relação ao Trabalho 1

| Aspecto                       | Trabalho 1          | Trabalho 2 (atual)  |
|-------------------------------|---------------------|---------------------|
| Funcionalidades obrigatórias  | 3.1, 3.2, 3.3       | + 3.4 (planejador)  |
| Funcionalidades de aprendizado | —                  | + 2 (exercícios + quiz interativo) |
| Ferramentas (tool calling)    | 8                   | **10**              |
| Módulos em `src/`             | 7                   | **10**              |
| Testes unitários              | 9                   | **14**              |
| Avaliação sistemática         | —                   | ✅ 12 perguntas     |
| Análise de erros              | —                   | ✅ 3 falhas + 1 corrigida |

---

## Arquitetura

```
┌──────────────────┐    ┌─────────────────────────────────────────────┐
│                  │    │               JARVIS (Python)               │
│   Usuário (CLI)  │◀──▶│  ┌──────────────────┐  ┌─────────────────┐  │
│                  │    │  │    Cérebro       │  │   10 Tools      │  │
└──────────────────┘    │  │   (jarvis.py)    │─▶│   (tools.py)    │  │
                        │  │                  │  │                 │  │
                        │  │   Decide qual    │  │ consultar_...   │  │
                        │  │   ferramenta     │  │ listar_...      │  │
                        │  │   chamar         │  │ adicionar_...   │  │
                        │  └──────────────────┘  │ buscar_rag      │  │
                        │           │            │ planejar_...    │  │
                        │           ▼            │ gerar_exerc...  │  │
                        │  ┌──────────────────┐  │ sugerir_quiz    │  │
                        │  │   Gemma 12B      │  └─────────────────┘  │
                        │  │ (llm_client.py)  │                       │
                        │  └──────────────────┘                       │
                        │           │                                 │
                        │           ▼                                 │
                        │  ┌───────┐ ┌───────┐ ┌────────┐ ┌─────────┐ │
                        │  │  RAG  │ │Agenda │ │Tarefas │ │  Quiz   │ │
                        │  │ rag.py│ │ JSON  │ │ JSON   │ │ quiz.py │ │
                        │  └───────┘ └───────┘ └────────┘ └─────────┘ │
                        │           │                                 │
                        │           ▼                                 │
                        │  ┌──────────────┐  ┌───────────────────┐    │
                        │  │ Planejador   │  │ Gerador exercícios│    │
                        │  │planejador.py │  │   exercicios.py   │    │
                        │  └──────────────┘  └───────────────────┘    │
                        └─────────────────────────────────────────────┘
```

**Pipeline de uma pergunta:**
1. Usuário digita uma mensagem.
2. `jarvis.py` envia ao LLM com a lista de ferramentas disponíveis.
3. O LLM responde em JSON indicando qual ferramenta usar e com quais argumentos.
4. `tools.py` executa a ferramenta e registra log em `logs/tool_calls.log`.
5. O LLM transforma o resultado bruto em resposta natural ao usuário.

**Exceção:** o Quiz Interativo é um **modo dedicado** ativado pelo comando `/quiz <tema>` — não passa pelo agente conversacional porque envolve estado entre turnos.

---

## Funcionalidades

### Funcionalidades base (Trabalho 1)

#### 3.1 — Consulta a materiais de estudo (RAG)
- Carregamento automático de `.txt`, `.md` e `.pdf` da pasta `data/`.
- Chunking inteligente preservando parágrafos (~500 caracteres com 50 de sobreposição).
- Embeddings com `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- Similaridade do cosseno para recuperar os top-K trechos.
- Resposta gerada pelo Gemma usando apenas os trechos recuperados.

#### 3.2 — Agenda acadêmica
- Adicionar e remover eventos (aulas, provas, trabalhos, reuniões).
- Consultar por "hoje", "amanhã", "semana", "todos" ou data específica.
- Armazenamento em JSON.

#### 3.3 — Lista de tarefas
- Adicionar tarefa com prazo e prioridade.
- Listar (pendentes / concluídas / todas).
- Marcar como concluída e remover.

### Novas funcionalidades (Trabalho 2)

#### 3.4 — Planejamento de estudos 
Combina três fontes para sugerir um plano:
- Eventos próximos da **agenda** (provas, trabalhos)
- **Tarefas pendentes** (com prazos)
- **Tópicos disponíveis** nos materiais de estudo (extraídos automaticamente dos títulos H1 dos `.md`)

Exemplo:
```
Você: Monte um plano de estudos para essa semana
JARVIS: [plano com sessões de 45-90min, priorizando provas próximas,
distribuindo tópicos do dataset, com momentos de revisão]
```

#### Gerador de Exercícios *(Funcionalidade de Aprendizado #1)*
Gera questões de múltipla escolha (a/b/c/d) sobre um tema, com gabarito e justificativas, a partir dos materiais.

- Filtro de similaridade mínima (0.35): se o tema não está nos materiais, o sistema avisa em vez de inventar.
- Não-interativo (você pede N questões e recebe tudo de uma vez).

#### Quiz Interativo *(Funcionalidade de Aprendizado #2 — Interativa)*
Modo dedicado de **active recall**: o sistema gera perguntas, faz uma de cada vez, avalia a resposta e dá feedback. No final, mostra estatísticas e indica questões para revisar.

- Aceita respostas como letra (`b`) ou em **texto livre** — neste caso o Gemma faz **avaliação semântica** (CORRETA / PARCIAL / INCORRETA).
- Mantém estado entre turnos sem passar pelo tool calling normal.

---

## Tool Calling — 10 ferramentas

| #  | Ferramenta              | Propósito                                                |
|----|-------------------------|----------------------------------------------------------|
| 1  | `consultar_agenda`      | Consultar eventos da agenda                              |
| 2  | `adicionar_evento`      | Adicionar evento à agenda                                |
| 3  | `listar_tarefas`        | Listar tarefas (filtros: pendentes/concluídas/todas)     |
| 4  | `adicionar_tarefa`      | Criar nova tarefa                                        |
| 5  | `concluir_tarefa`       | Marcar tarefa como concluída                             |
| 6  | `remover_tarefa`        | Remover tarefa                                           |
| 7  | `buscar_material_rag`   | Buscar resposta nos materiais (RAG)                      |
| 8  | `responder_diretamente` | Saudações, perguntas sem necessidade de fonte            |
| 9  | `planejar_estudos`      | Plano de estudos personalizado 🆕                        |
| 10 | `gerar_exercicios`      | Questões de múltipla escolha sobre um tema 🆕            |
| 11 | `sugerir_quiz`          | Orienta o usuário a iniciar o quiz interativo 🆕         |

**Características:**
- Decisão feita pela **LLM**, não por lógica fixa.
- Todas as chamadas são logadas em `logs/tool_calls.log`.

---

## Instalação

### Pré-requisitos
- Python 3.10 ou superior
- ~1 GB de espaço em disco (modelo de embeddings + PyTorch)
- Conexão à internet (1ª execução baixa o modelo de embeddings)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/victorvalenzuela04/jarvis-academico-trab2.git
cd jarvis-academico-trab2

# 2. Crie um ambiente virtual
python -m venv venv

# 3. Ative o ambiente
# Linux/macOS:
source venv/bin/activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1

# 4. Instale as dependências
pip install -r requirements.txt
```

> ⚠️ A primeira execução baixa ~500 MB (PyTorch + modelo de embeddings).

Para instruções detalhadas (incluindo problemas comuns no Windows), veja [TUTORIAL.md](TUTORIAL.md).

---

## ▶️ Como rodar

```bash
python main.py
```

Na primeira execução:
1. Constrói o índice vetorial a partir dos documentos em `data/`.
2. Baixa o modelo de embeddings (apenas na 1ª vez).
3. Apresenta o prompt `Você:` para interação.

### Comandos especiais

| Comando         | Função                                                  |
|-----------------|---------------------------------------------------------|
| `/sair`         | Encerra o programa                                      |
| `/reindex`      | Reconstrói o índice (após adicionar arquivos em data/)  |
| `/debug`        | Mostra detalhes da última chamada (JSON cru)            |
| `/quiz <tema>`  | Inicia um quiz interativo sobre um tema 🆕              |
| `/sair-quiz`    | Encerra o quiz em andamento (apenas dentro do modo quiz) |
| `/ajuda`        | Reexibe o banner inicial                                |

### Exemplos de uso

```
# Consulta de conteúdo (RAG)
Você: O que é regressão logística?
JARVIS: A regressão logística é um modelo estatístico... [usa buscar_material_rag]

# Agenda
Você: Adicione uma prova de Cálculo dia 2026-06-05 às 14:00
JARVIS: Ok, adicionei... [usa adicionar_evento]

# Tarefas
Você: Adicione uma tarefa: revisar slides, prazo 2026-05-30
JARVIS: Tarefa adicionada... [usa adicionar_tarefa]

# Planejamento (NOVO)
Você: Monte um plano de estudos para essa semana
JARVIS: ## Plano de Estudos... [usa planejar_estudos]

# Exercícios (NOVO)
Você: Gere 3 exercícios sobre tabelas hash
JARVIS: Questão 1: ... a) ... b) ... [usa gerar_exercicios]

# Quiz interativo (NOVO)
Você: /quiz recursão
JARVIS: Pergunta 1/5: ...
        Sua resposta: b
        ✓ Correto! ...
```

---

## Estrutura do projeto

```
jarvis-academico-trab2/
├── main.py                     # CLI + modo quiz
├── requirements.txt
├── README.md                   # Este arquivo
├── TUTORIAL.md                 # Tutorial detalhado de instalação
├── AVALIACAO.md                # Avaliação com 12 perguntas 
├── ERROS.md                    # Análise de 3 falhas + 1 resolvida 
├── .gitignore
│
├── src/                        # Código-fonte
│   ├── config.py               # Configurações centralizadas
│   ├── llm_client.py           # Cliente do Gemma 12B
│   ├── rag.py                  # RAG: chunking, embeddings, busca
│   ├── agenda.py               # CRUD da agenda
│   ├── tarefas.py              # CRUD das tarefas
│   ├── tools.py                # Catálogo + dispatcher de ferramentas
│   ├── jarvis.py               # Cérebro do agente
│   ├── planejador.py           # Planejador de estudos 
│   ├── exercicios.py           # Gerador de exercícios 
│   └── quiz.py                 # Quiz interativo 
│
├── data/                       # Dataset acadêmico (10 documentos)
│   ├── README.md               # Origem, tipo, limitações, chunking
│   └── 01..10_*.md             # Conteúdo acadêmico em português
│
├── tests/                      # Testes unitários (14 testes)
│   └── test_basico.py
│
├── storage/                    # Estado persistente (JSON, gerado em runtime)
├── index/                      # Índice vetorial do RAG (gerado em runtime)
└── logs/                       # Logs de tool calling (gerado em runtime)
```

---

## Dataset

10 documentos acadêmicos em português abordando temas de Computação. O mesmo dataset do Trabalho 1, totalmente coberto pelas funcionalidades do Trabalho 2.

Detalhes (origem, tipo de conteúdo, limitações, estratégia de chunking) em [`data/README.md`](data/README.md).

---

## Engenharia de software

- **Organização modular**: cada arquivo em `src/` tem uma única responsabilidade.
- **Configuração centralizada**: tudo em `src/config.py`.
- **Testes unitários**: 14 testes em `tests/test_basico.py` cobrindo agenda, tarefas, chunking, contrato das ferramentas e parser do quiz.
- **Logging estruturado**: `logs/tool_calls.log` registra cada chamada.
- **Tratamento de erros**: `try/except` em `tools.py` impede que falha em ferramenta derrube o agente.
- **Imports preguiçosos**: bibliotecas pesadas (sentence-transformers, numpy) só carregam quando usadas.

Rodar os testes:
```bash
python -m unittest discover tests
```

---

## Avaliação e Análise Crítica

Conforme exigência do enunciado:

- **[AVALIACAO.md](AVALIACAO.md)** — Avaliação sistemática do sistema com 12 perguntas (8 corretas, 2 parciais, 2 incorretas), incluindo documentos recuperados, classificação e análise de cada caso.

- **[ERROS.md](ERROS.md)** — Análise crítica de 3 falhas identificadas (com causa raiz, impacto e propostas de solução) mais 1 falha bônus identificada e corrigida durante o desenvolvimento.

---

## IAs utilizadas no desenvolvimento

- **Claude** — usado para:
  - Auxiliar na arquitetura
  - Sugestões de melhorias estruturais
  - Auxílio na documentação com markdown para melhorar visual e escrita (README, TUTORIAL, AVALIACAO, ERROS)

Todo o código foi revisado e testado por mim antes da entrega.

---

## Autor

- Victor Valenzuela de Alcântara Ferreira

Disciplina de Inteligência Artificial — Sistemas de Informação — UFMS.
