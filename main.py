"""
main.py
-------
Interface de linha de comando do JARVIS Acadêmico.
Execute com:  python main.py
"""
import os
import sys
import json

# Garante que o pacote src é encontrado quando rodamos `python main.py`
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src import jarvis, rag, config, quiz


def banner() -> None:
    print("=" * 64)
    print("        JARVIS ACADÊMICO  —  Assistente Inteligente")
    print("=" * 64)
    print("Digite sua pergunta normalmente.\n")
    print("Comandos especiais:")
    print("  /sair        - encerra o programa")
    print("  /reindex     - reconstroi o índice de materiais (RAG)")
    print("  /debug       - mostra detalhes da última chamada de ferramenta")
    print("  /quiz <tema> - inicia um quiz interativo sobre um tema")
    print("  /ajuda       - mostra esta ajuda novamente")
    print()


# =============================== MODO QUIZ ===============================
def executar_quiz(tema: str, n_perguntas: int = 5) -> None:
    """
    Loop interativo do quiz. Gera N perguntas, faz uma de cada vez,
    avalia cada resposta, e ao final mostra estatísticas.
    """
    print(f"\n[quiz] Gerando {n_perguntas} perguntas sobre '{tema}'...")
    resultado = quiz.gerar_perguntas(tema, n_perguntas)

    if "erro" in resultado:
        print(f"[quiz] {resultado['erro']}")
        return

    perguntas = resultado["perguntas"]
    print(f"[quiz] {len(perguntas)} perguntas prontas. Vamos lá!\n")
    print("Dica: você pode responder com a letra (a, b, c, d) ou com texto livre.")
    print("Digite '/sair-quiz' a qualquer momento para encerrar.\n")

    respostas: list[dict] = []

    for i, pergunta in enumerate(perguntas, start=1):
        print("─" * 60)
        print(f"Pergunta {i}/{len(perguntas)}: {pergunta['enunciado']}\n")
        for letra in ("a", "b", "c", "d"):
            print(f"  {letra}) {pergunta['alternativas'][letra]}")
        print()

        try:
            resposta = input("Sua resposta: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[quiz] Encerrado pelo usuário.")
            break

        if resposta.lower() == "/sair-quiz":
            print("[quiz] Encerrado pelo usuário.")
            break

        if not resposta:
            print("[quiz] Resposta vazia — pulando para a próxima.\n")
            respostas.append({"acertou": False, "parcial": False,
                              "feedback": "Não respondida.", "metodo": "vazio"})
            continue

        avaliacao = quiz.avaliar_resposta(pergunta, resposta)
        respostas.append(avaliacao)
        print(f"\n{avaliacao['feedback']}\n")

    if respostas:
        print()
        print(quiz.gerar_sumario(perguntas, respostas))


# =============================== LOOP PRINCIPAL ===============================
def main() -> None:
    banner()

    # Garante que o índice exista
    if not os.path.exists(config.INDEX_FILE):
        print("[init] Nenhum índice encontrado. Construindo agora...")
        rag.construir_indice()
        print()
    else:
        rag.carregar_indice()

    historico: list = []
    ultima: dict | None = None

    while True:
        try:
            entrada = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            return

        if not entrada:
            continue

        # Comandos especiais
        if entrada == "/sair":
            print("Até logo!")
            return
        if entrada == "/ajuda":
            banner()
            continue
        if entrada == "/reindex":
            rag.construir_indice()
            continue
        if entrada == "/debug":
            if ultima:
                print(json.dumps(ultima, ensure_ascii=False, indent=2, default=str))
            else:
                print("Nenhuma chamada ainda.")
            continue

        # /quiz <tema>  → entra no modo quiz
        if entrada.lower().startswith("/quiz"):
            tema = entrada[len("/quiz"):].strip()
            if not tema:
                try:
                    tema = input("Sobre qual tema? ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    continue
            if tema:
                executar_quiz(tema)
            continue

        # Pipeline do agente (caso default)
        try:
            resultado = jarvis.processar(entrada, historico)
            ultima = resultado
            print(f"\nJARVIS: {resultado['resposta']}")
            print(f"   [ferramenta utilizada: {resultado['ferramenta']}]")

            historico.append({"role": "user",      "content": entrada})
            historico.append({"role": "assistant", "content": resultado["resposta"]})
            # Mantém o histórico curto para não estourar o contexto
            if len(historico) > 10:
                historico = historico[-10:]
        except Exception as e:
            print(f"\n[erro] {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
