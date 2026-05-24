# JARVIS Acadêmico 

> Assistente pessoal inteligente para estudantes universitários, com **RAG**, **Tool Calling** e LLM **Gemma 12B**.

Trabalho prático da disciplina, **Entrega 1** (Funcionalidades 3.1, 3.2 e 3.3 do enunciado).

---

## Visão geral

O JARVIS Acadêmico é um agente conversacional em Python que ajuda estudantes a:

- Consultar materiais de estudo via **RAG** (Retrieval-Augmented Generation)
- Gerenciar uma **agenda acadêmica** (aulas, provas, trabalhos)
- Gerenciar uma **lista de tarefas** (adicionar, listar, concluir, remover)

A "inteligência" do sistema vem da LLM **Gemma 12B** (acessada via API fornecida pelo professor), que decide autonomamente qual **ferramenta** chamar para cada pergunta do usuário.

---

## Arquitetura

```
┌──────────────────┐    ┌─────────────────────────────────────────┐
│                  │    │              JARVIS (Python)            │
│   Usuário (CLI)  │◀──▶│  ┌────────────────┐  ┌───────────────┐  │
│                  │    │  │   Cérebro      │  │  8 Tools      │  │
└──────────────────┘    │  │  (jarvis.py)   │─▶│  (tools.py)   │  │
                        │  │                │  │               │  │
                        │  │  Decide qual   │  │ consultar_... │  │
                        │  │  ferramenta    │  │ listar_...    │  │
                        │  │  chamar        │  │ adicionar_... │  │
                        │  └────────────────┘  │ buscar_rag    │  │
                        │          │           └───────────────┘  │
                        │          ▼                              │
                        │  ┌────────────────────────────────────┐ │
                        │  │  Gemma 12B  (llm_client.py)        │ │
                        │  └────────────────────────────────────┘ │
                        │          │                              │
                        │          ▼                              │
                        │  ┌──────────┐  ┌──────────┐ ┌─────────┐ │
                        │  │   RAG    │  │  Agenda  │ │ Tarefas │ │
                        │  │ (rag.py) │  │  (JSON)  │ │ (JSON)  │ │
                        │  └──────────┘  └──────────┘ └─────────┘ │
                        └─────────────────────────────────────────┘
```

**Pipeline de uma pergunta:**
1. Usuário digita uma mensagem.
2. `jarvis.py` envia ao LLM com a lista de ferramentas disponíveis.
3. O LLM responde em JSON indicando qual ferramenta usar e com quais argumentos.
4. `tools.py` executa a ferramenta e registra log em `logs/tool_calls.log`.
5. O LLM transforma o resultado bruto em resposta natural ao usuário.

---

## Funcionalidades implementadas (Trabalho 1)

### 3.1 — Consulta a materiais de estudo (RAG) 
- Carregamento automático de `.txt`, `.md` e `.pdf` da pasta `data/`.
- **Chunking inteligente** que preserva parágrafos (~500 caracteres com 50 de sobreposição quando necessário).
- **Embeddings** com `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (modelo open-source multilíngue, roda localmente).
- **Similaridade do cosseno** para recuperar os top-K trechos mais relevantes.
- **Geração aumentada**: o Gemma responde usando apenas os trechos recuperados.

### 3.2 — Agenda acadêmica 
- Adicionar e remover eventos (aulas, provas, trabalhos, reuniões).
- Consultar por "hoje", "amanhã", "semana", "todos" ou data específica.
- Armazenamento em JSON (`storage/agenda.json`).

### 3.3 — Lista de tarefas 
- Adicionar tarefa com prazo e prioridade.
- Listar (pendentes / concluídas / todas).
- Marcar como concluída e remover.
- Armazenamento em JSON (`storage/tarefas.json`).

---

## Tool Calling

O sistema implementa **8 ferramentas** (o enunciado pede no mínimo 5):

| # | Ferramenta              | Propósito                                            |
|---|-------------------------|------------------------------------------------------|
| 1 | `consultar_agenda`      | Consultar eventos da agenda                          |
| 2 | `adicionar_evento`      | Adicionar evento à agenda                            |
| 3 | `listar_tarefas`        | Listar tarefas (filtros: pendentes/concluídas/todas) |
| 4 | `adicionar_tarefa`      | Criar nova tarefa                                    |
| 5 | `concluir_tarefa`       | Marcar tarefa como concluída                         |
| 6 | `remover_tarefa`        | Remover tarefa                                       |
| 7 | `buscar_material_rag`   | Buscar resposta nos materiais de estudo (RAG)        |
| 8 | `responder_diretamente` | Saudações, perguntas gerais sem fonte                |

**Características:**
- Decisão **feita pela LLM**, não por lógica fixa (regex/if-else).
- Todas as chamadas são **logadas** em `logs/tool_calls.log` com timestamp, entrada e saída.

---

## Tecnologias

| Categoria             | Tecnologia                                          |
|-----------------------|-----------------------------------------------------|
| Linguagem             | Python 3.10+                                        |
| LLM                   | Google Gemma 3 12B (via endpoint da LIA-UFMS)       |
| Cliente LLM           | `openai` (compatível com endpoint OpenAI-like)      |
| Embeddings            | `sentence-transformers` (MiniLM-L12 multilíngue)    |
| Vetorização/Busca     | `numpy` (similaridade do cosseno manual)            |
| Leitura de PDFs       | `pypdf`                                             |
| Persistência          | JSON puro (arquivos locais)                         |
| Testes                | `unittest` (padrão da stdlib)                       |

---

## Instalação

### Pré-requisitos
- Python 3.10 ou superior
- ~1 GB de espaço em disco (para o modelo de embeddings + PyTorch)
- Conexão à internet (apenas na 1ª execução, para baixar o modelo)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/jarvis-academico.git
cd jarvis-academico

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

> ⚠️ A primeira execução baixa ~500 MB (PyTorch + modelo de embeddings). Tenha paciência.

Para um tutorial detalhado de instalação (incluindo problemas comuns no Windows), veja [TUTORIAL.md](TUTORIAL.md).

---

## ▶️ Como rodar

```bash
python main.py
```

Na primeira execução, o sistema:
1. Constrói o índice vetorial a partir dos documentos em `data/`.
2. Baixa o modelo de embeddings (apenas na 1ª vez).
3. Apresenta o prompt `Você:` para interação.

### Comandos especiais durante a execução

| Comando      | Função                                       |
|--------------|----------------------------------------------|
| `/sair`      | Encerra o programa                           |
| `/reindex`   | Reconstrói o índice (após adicionar `data/`) |
| `/debug`     | Mostra detalhes da última chamada (JSON cru) |
| `/ajuda`     | Reexibe o banner inicial                     |

### Exemplos de uso

```
Você: O que é regressão logística?
JARVIS: A regressão logística é um modelo estatístico usado para problemas de
classificação binária...
[ferramenta utilizada: buscar_material_rag]

Você: Adicione uma prova de Estruturas de Dados dia 2026-06-05 às 14:00
JARVIS: Ok, adicionei a prova de Estruturas de Dados para o dia 5 de junho de 2026, às 14:00.
[ferramenta utilizada: adicionar_evento]

Você: Liste minhas tarefas pendentes
JARVIS: Aqui estão suas tarefas pendentes: ...
[ferramenta utilizada: listar_tarefas]

Você: O que tenho na agenda essa semana?
JARVIS: Essa semana você tem uma aula de Banco de Dados agendada para o dia 23 de maio às 19:00!
[ferramenta utilizada: consultar_agenda]
```

---

## Estrutura do projeto

```
jarvis-academico/
├── main.py                     # Ponto de entrada (CLI)
├── requirements.txt            # Dependências
├── README.md                   # Este arquivo
├── TUTORIAL.md                 # Tutorial detalhado de instalação
├── .gitignore
│
├── src/                        # Código-fonte
│   ├── config.py               # Configurações centralizadas
│   ├── llm_client.py           # Cliente do Gemma 12B
│   ├── rag.py                  # RAG: chunking, embeddings, busca semântica
│   ├── agenda.py               # CRUD da agenda
│   ├── tarefas.py              # CRUD das tarefas
│   ├── tools.py                # Catálogo e despachante de ferramentas + logging
│   └── jarvis.py               # Cérebro do agente (decisão + execução)
│
├── data/                       # Dataset acadêmico (10 documentos)
│   ├── README.md               # Origem, tipo, limitações, chunking
│   └── 01..10_*.md             # Conteúdo acadêmico em português
│
├── tests/                      # Testes unitários (unittest)
│   └── test_basico.py
│
├── storage/                    # Estado persistente (JSON)
│   ├── agenda.json             # criado automaticamente
│   └── tarefas.json            # criado automaticamente
│
├── index/                      # Índice vetorial do RAG
│   └── indice.pkl              # criado automaticamente
│
└── logs/                       # Logs de tool calling
    └── tool_calls.log          # criado automaticamente
```

---

## Dataset

10 documentos acadêmicos em português abordando temas de Computação:

| Arquivo                          | Tema                              |
|----------------------------------|-----------------------------------|
| `01_regressao_logistica.md`      | Regressão Logística               |
| `02_embeddings.md`               | Embeddings                        |
| `03_listas_encadeadas.md`        | Listas Encadeadas (TAD)           |
| `04_tabelas_hash.md`             | Tabelas Hash e colisões           |
| `05_redes_neurais.md`            | Redes Neurais Artificiais         |
| `06_ordenacao.md`                | Algoritmos de Ordenação           |
| `07_recursao.md`                 | Recursão                          |
| `08_complexidade.md`             | Análise de Complexidade / Big-O   |
| `09_banco_de_dados.md`           | Banco de Dados Relacional         |
| `10_machine_learning.md`         | Introdução ao Machine Learning    |

**Origem, tipo de conteúdo, limitações e estratégia de chunking**: detalhados em [`data/README.md`](data/README.md).

---

## Engenharia de software

- **Organização modular**: cada arquivo em `src/` tem uma responsabilidade clara.
- **Separação de camadas**: persistência (JSON), lógica de negócio (CRUD), agente (LLM + tools), interface (CLI).
- **Configuração centralizada**: todos os parâmetros em `src/config.py`.
- **Testes unitários**: 8 testes em `tests/test_basico.py` cobrindo agenda, tarefas, chunking e contrato das ferramentas.
- **Logging estruturado**: `logs/tool_calls.log` registra cada chamada (timestamp, ferramenta, entrada, saída).
- **Tratamento de erros**: `try/except` em `tools.py` para não quebrar o agente em caso de falha de uma ferramenta.
- **Imports preguiçosos**: bibliotecas pesadas só são importadas quando realmente usadas (permite rodar testes leves sem instalar PyTorch).

Rodar os testes:
```bash
python -m unittest discover tests
```

---

## IAs utilizadas para auxiliar no desenvolvimento

- **Claude** 

Mesmo com o auxílio dessa ferramenta, todo o código foi revisado e testado por mim antes da entrega.

---

## Roadmap -- Trabalho 2 (em desenvolvimento)

- [ ] Funcionalidade 3.4: planejamento de estudos integrado (agenda + tarefas + materiais)
- [ ] 2+ funcionalidades de aprendizado (geração de exercícios, active recall)
- [ ] Avaliação sistemática com 10+ perguntas (corretas / parcialmente / incorretas)
- [ ] Análise de pelo menos 3 falhas (tipo, causa, solução)
- [ ] Diferencial: interface gráfica (a definir)

---

## Autor

- Victor Valenzuela de Alcântara Ferreira

Disciplina de Inteligência Artificial — Sistemas de Informação — UFMS.