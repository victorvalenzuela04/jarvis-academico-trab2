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

from src import jarvis, rag, config


def banner() -> None:
    print("=" * 64)
    print("        JARVIS ACADÊMICO  —  Assistente Inteligente")
    print("=" * 64)
    print("Digite sua pergunta normalmente.\n")
    print("Comandos especiais:")
    print("  /sair       - encerra o programa")
    print("  /reindex    - reconstroi o índice de materiais (RAG)")
    print("  /debug      - mostra detalhes da última chamada de ferramenta")
    print("  /ajuda      - mostra esta ajuda novamente")
    print()


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

        # Pipeline do agente
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
