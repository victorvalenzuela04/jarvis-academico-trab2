"""
Testes básicos do JARVIS Acadêmico.

Foco: validar a lógica que NÃO depende de rede (agenda, tarefas,
chunking). Os módulos que falam com o LLM são testados manualmente
durante o uso normal --> não rodamos chamadas pagas em testes
automatizados.

Como rodar:
    cd jarvis-academico
    python -m unittest discover tests
"""
import os
import sys
import shutil
import tempfile
import unittest

# Permitir importar src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAgenda(unittest.TestCase):
    """Testes do módulo agenda."""

    def setUp(self):
        # Usa um diretório temporário para não bagunçar o storage real
        self.tmp = tempfile.mkdtemp()
        from src import config
        self._original = config.AGENDA_FILE
        config.AGENDA_FILE = os.path.join(self.tmp, "agenda.json")

    def tearDown(self):
        from src import config
        config.AGENDA_FILE = self._original
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_adicionar_e_consultar(self):
        from src import agenda
        evento = agenda.adicionar_evento(
            titulo="Prova de Cálculo", data="2099-12-31",
            hora="14:00", tipo="prova",
        )
        self.assertEqual(evento["titulo"], "Prova de Cálculo")
        self.assertIsInstance(evento["id"], int)

        encontrados = agenda.consultar_agenda(periodo="2099-12-31")
        self.assertEqual(len(encontrados), 1)
        self.assertEqual(encontrados[0]["titulo"], "Prova de Cálculo")

    def test_consulta_dia_vazio(self):
        from src import agenda
        resultado = agenda.consultar_agenda(periodo="2000-01-01")
        self.assertEqual(resultado, [])


class TestTarefas(unittest.TestCase):
    """Testes do módulo tarefas."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        from src import config
        self._original = config.TAREFAS_FILE
        config.TAREFAS_FILE = os.path.join(self.tmp, "tarefas.json")

    def tearDown(self):
        from src import config
        config.TAREFAS_FILE = self._original
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_ciclo_completo(self):
        from src import tarefas
        t = tarefas.adicionar_tarefa("Estudar para a prova", prioridade="alta")
        self.assertFalse(t["concluida"])

        pendentes = tarefas.listar_tarefas("pendentes")
        self.assertEqual(len(pendentes), 1)

        concluida = tarefas.concluir_tarefa(t["id"])
        self.assertTrue(concluida["concluida"])

        self.assertEqual(len(tarefas.listar_tarefas("pendentes")), 0)
        self.assertEqual(len(tarefas.listar_tarefas("concluidas")), 1)

    def test_remover(self):
        from src import tarefas
        t = tarefas.adicionar_tarefa("Tarefa para remover")
        self.assertTrue(tarefas.remover_tarefa(t["id"]))
        self.assertFalse(tarefas.remover_tarefa(99999))


class TestChunking(unittest.TestCase):
    """Testes da estratégia de chunking."""

    def test_chunks_pequenos_juntos(self):
        from src import rag
        texto = "Parágrafo um.\n\nParágrafo dois.\n\nParágrafo três."
        chunks = rag.dividir_em_chunks(texto, chunk_size=500, overlap=50)
        # Todos cabem em um único chunk
        self.assertEqual(len(chunks), 1)
        self.assertIn("Parágrafo um.", chunks[0])
        self.assertIn("Parágrafo três.", chunks[0])

    def test_paragrafo_gigante_quebra_em_pedacos(self):
        from src import rag
        texto = "A" * 1500  # bem maior que chunk_size
        chunks = rag.dividir_em_chunks(texto, chunk_size=500, overlap=50)
        self.assertGreater(len(chunks), 1)
        for c in chunks:
            self.assertLessEqual(len(c), 500)

    def test_filtro_de_arquivos_indexaveis(self):
        from src import rag
        # README é meta-documentação, não deve ser indexado
        self.assertFalse(rag._eh_indexavel("README.md"))
        self.assertFalse(rag._eh_indexavel("readme.md"))
        # Arquivos ocultos não devem ser indexados
        self.assertFalse(rag._eh_indexavel(".gitkeep"))
        # Extensões não suportadas
        self.assertFalse(rag._eh_indexavel("foto.png"))
        # Arquivos válidos sim
        self.assertTrue(rag._eh_indexavel("01_regressao.md"))
        self.assertTrue(rag._eh_indexavel("notas.txt"))
        self.assertTrue(rag._eh_indexavel("apostila.pdf"))


class TestTools(unittest.TestCase):
    """Garantia mínima sobre o catálogo de ferramentas."""

    def test_tem_pelo_menos_cinco_ferramentas(self):
        from src import tools
        self.assertGreaterEqual(len(tools.FERRAMENTAS), 5)

    def test_ferramentas_obrigatorias_existem(self):
        from src import tools
        nomes = {f["nome"] for f in tools.FERRAMENTAS}
        obrigatorias = {
            "consultar_agenda", "listar_tarefas",
            "adicionar_tarefa", "concluir_tarefa",
            "buscar_material_rag",
        }
        self.assertTrue(obrigatorias.issubset(nomes),
                        f"Faltam ferramentas: {obrigatorias - nomes}")


if __name__ == "__main__":
    unittest.main()
