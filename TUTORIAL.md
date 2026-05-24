# TUTORIAL — Como rodar o JARVIS Acadêmico do zero

Este guia assume que você nunca rodou um projeto Python na sua máquina.
Cada passo está explicado, e no final tem um capítulo de problemas
comuns. Leia com calma.

---

## 1. Instalar o Python (se ainda não tiver)

Abra o terminal e digite:

```bash
python --version
```

Se aparecer algo como `Python 3.10.12` (ou qualquer versão 3.10+),
você já tem. Se der erro, instale o Python:

- **Windows**: vá em https://www.python.org/downloads/ e baixe o
  instalador. **Marque a opção "Add Python to PATH"** antes de
  clicar em Install.
- **Linux (Ubuntu)**: `sudo apt update && sudo apt install python3 python3-pip python3-venv`
- **macOS**: instale via Homebrew → `brew install python`

Confirme:
```bash
python --version   # ou python3 --version
pip --version      # ou pip3 --version
```

---

## 2. Baixar o projeto e abrir uma pasta

1. Descompacte o `.zip` que você recebeu para uma pasta tipo
   `C:\Projetos\jarvis-academico` (Windows) ou
   `~/Projetos/jarvis-academico` (Linux/macOS).
2. Abra um terminal **dentro dessa pasta**:
   - Windows: dentro do Explorer, clique na barra de endereço e
     digite `cmd` (ou `powershell`) e tecle Enter.
   - Linux/macOS: `cd ~/Projetos/jarvis-academico`

Para conferir que você está no lugar certo, rode:
```bash
ls          # Linux/macOS
dir         # Windows
```
Você deve ver `main.py`, `requirements.txt`, `src/`, `data/`, etc.

---

## 3. Criar um ambiente virtual (recomendado)

Um "ambiente virtual" (venv) é uma caixinha isolada onde instalamos
as bibliotecas do projeto, sem bagunçar o Python do sistema. Crie:

```bash
python -m venv venv
```

Ative o ambiente:
- **Windows (cmd)**: `venv\Scripts\activate`
- **Windows (PowerShell)**: `venv\Scripts\Activate.ps1`
  (se der erro de execução, rode antes:
  `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`)
- **Linux/macOS**: `source venv/bin/activate`

Você saberá que está ativo porque o prompt do terminal fica com
`(venv)` no começo. Se quiser sair: `deactivate`.

---

## 4. Instalar as dependências

Com o ambiente ativado:

```bash
pip install -r requirements.txt
```

Isso instala:
- `openai` → cliente para falar com o Gemma 12B
- `sentence-transformers` → modelo que gera os embeddings (essa
  primeira instalação pode levar alguns minutos e baixar uns 500 MB,
  porque ele traz o PyTorch junto)
- `numpy` → cálculos com vetores (similaridade do cosseno)
- `pypdf` → leitura de arquivos PDF

Se ficar muito tempo "preso", não cancele — o `sentence-transformers`
é grande. Aguarde.

---

## 5. Rodar os testes (validação rápida)

Antes de partir pra usar o sistema, confirme que está tudo no lugar:

```bash
python -m unittest discover tests
```

Você deve ver `OK` no final, com 8 testes passando. Se algum falhar,
veja a seção 9 (Problemas comuns).

---

## 6. Rodar o JARVIS

```bash
python main.py
```

O que acontece na primeira execução:

1. Como ainda não há índice de RAG, o sistema vai detectar e construir.
2. Ele lê os 10 documentos em `data/`, divide em chunks e gera os
   embeddings. Isso pode demorar um pouco (1ª vez baixa o modelo de
   embeddings ~200 MB; nas próximas vezes é rápido).
3. Depois aparece o banner do JARVIS e o prompt `Você: `.

A partir daí, você pode conversar. Exemplos:

```
Você: O que é regressão logística?
Você: Quem inventou o método da multiplicação de Knuth?
Você: Tenho prova essa semana?
Você: Adicione uma aula de Estruturas de Dados dia 2026-06-10 às 14:00
Você: Adicione tarefa "Terminar relatório do trabalho" com prazo 2026-05-30
Você: Liste minhas tarefas pendentes
Você: Marque a tarefa 1 como concluída
```

### Comandos especiais (durante a execução):

- `/sair` → encerra o programa
- `/reindex` → reconstrói o índice (use depois de adicionar arquivos
  novos em `data/`)
- `/debug` → mostra detalhes da última chamada (ferramenta usada,
  argumentos, saída completa) — útil para o vídeo de explicação
- `/ajuda` → mostra o banner novamente

---

## 7. Adicionar mais materiais ao RAG

1. Coloque os arquivos `.txt`, `.md` ou `.pdf` na pasta `data/`.
2. Rode o JARVIS e digite `/reindex` no prompt, ou apague a pasta
   `index/` antes de iniciar.

---

## 8. Conferir os logs de Tool Calling (obrigatório no enunciado)

Cada chamada de ferramenta é registrada em `logs/tool_calls.log`. Para
ver:

```bash
# Linux/macOS
cat logs/tool_calls.log

# Windows
type logs\tool_calls.log
```

Cada linha tem timestamp, ferramenta chamada, argumentos passados e
um resumo da saída. **Esse arquivo é uma das provas para o professor
de que o sistema está fazendo tool calling de verdade.**

---

## 9. Problemas comuns

**"ModuleNotFoundError: No module named 'openai'"**
→ Você esqueceu de ativar o `venv` antes de rodar o `pip install`,
ou está usando outro terminal. Ative o venv e rode `pip install -r
requirements.txt` de novo.

**O download do sentence-transformers trava ou demora muito**
→ A primeira execução baixa ~500 MB. Em conexões lentas, demora.
Aguarde sem cancelar. Se realmente travar, rode:
`pip install --upgrade sentence-transformers`.

**"SSL: CERTIFICATE_VERIFY_FAILED" no Windows**
→ Atualize o `certifi`: `pip install --upgrade certifi`.

**"openai.AuthenticationError" ou "401"**
→ A chave do Gemma fornecida pelo professor expirou ou está errada.
Confirme em `src/config.py` o valor de `GEMMA_API_KEY`.

**"openai.APIConnectionError"**
→ Seu computador não está conseguindo acessar `https://llm.liaufms.org`.
Verifique sua conexão, ou se está numa rede com firewall.

**A resposta do JARVIS vem em formato JSON bruto**
→ Significa que a LLM ignorou a instrução de "responda em texto natural".
Pode acontecer ocasionalmente com Gemma. Tente reformular a pergunta.
Você pode usar `/debug` para ver o que aconteceu.

**Ele responde "não encontrei materiais relevantes"**
→ A pergunta pode ter sido enviada para `buscar_material_rag` mas
o tema não está no dataset. Adicione mais documentos em `data/` e
rode `/reindex`.

**Erros de codificação (acentos errados) no Windows**
→ No PowerShell, rode antes: `chcp 65001` para forçar UTF-8.

---