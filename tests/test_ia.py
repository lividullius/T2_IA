"""Testes do módulo ia (funções para o front).  Rodar:  python3 -m unittest discover tests"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import ia  # noqa: E402
from minimax import jogadas_otimas, melhor_jogada_minimax  # noqa: E402
from redeMlp import n_genes, salvar_pesos  # noqa: E402


class TestJogadasOtimas(unittest.TestCase):
    def test_tabuleiro_vazio_todas_empatam(self):
        self.assertEqual(sorted(jogadas_otimas([0] * 9, ia.X)), list(range(9)))

    def test_inclui_a_do_minimax(self):
        tab = [ia.X, 0, 0, 0, ia.O, 0, 0, 0, 0]
        self.assertIn(melhor_jogada_minimax(tab, ia.X), jogadas_otimas(tab, ia.X))

    def test_precisa_bloquear(self):
        # X ameaça 0-1-2; O só não perde bloqueando em 2
        tab = [ia.X, ia.X, 0, 0, ia.O, 0, 0, 0, 0]
        self.assertEqual(jogadas_otimas(tab, ia.O), [2])


class TestModelo(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.caminho = Path(self.pasta.name) / "rede.json"

    def tearDown(self):
        self.pasta.cleanup()

    def test_sem_modelo(self):
        self.assertFalse(ia.modelo_existe(self.caminho))
        with self.assertRaises(FileNotFoundError):
            ia.carregar_modelo(self.caminho)

    def test_carrega_uma_vez(self):
        salvar_pesos([0.1] * n_genes(), self.caminho)
        r1 = ia.carregar_modelo(self.caminho)
        self.assertIs(ia.carregar_modelo(self.caminho), r1)
        self.assertIsNot(ia.carregar_modelo(self.caminho, recarregar=True), r1)

    def test_treinar_salva_e_carrega(self):
        fim = ia.treinar(populacao=4, geracoes=2, seed=1,
                         caminho=self.caminho, caminho_log=None)
        self.assertTrue(ia.modelo_existe(self.caminho))
        self.assertEqual(ia.carregar_modelo(self.caminho).oculta[0],
                         fim["pesos"][:10])


class TestJogadaRede(unittest.TestCase):
    def test_corrige_casa_ocupada(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        caminho = Path(pasta.name) / "rede.json"
        salvar_pesos([0.0] * n_genes(), caminho)  # todas as saídas iguais -> casa 0
        rede = ia.carregar_modelo(caminho)
        tab = [ia.O, 0, 0, 0, 0, 0, 0, 0, 0]
        j = ia.jogada_rede(tab, ia.X, rede)
        self.assertEqual((j["escolhida"], j["valida"], j["casa"]), (0, False, 1))
        j = ia.jogada_rede(tab, ia.X, rede, corrigir=False)
        self.assertEqual(j["casa"], 0)


class TestAcuracia(unittest.TestCase):
    def test_contagem(self):
        acc = ia.Acuracia()
        tab = [ia.X, ia.X, 0, 0, ia.O, 0, 0, 0, 0]
        self.assertEqual(acc.registrar_jogada(tab, ia.O, 2),
                         {"valida": True, "otima": True})
        self.assertEqual(acc.registrar_jogada(tab, ia.O, 5),
                         {"valida": True, "otima": False})
        self.assertEqual(acc.registrar_jogada(tab, ia.O, 0),
                         {"valida": False, "otima": False})
        acc.registrar_resultado("empate")
        acc.registrar_resultado("derrota")
        r = acc.resumo()
        self.assertEqual((r["jogadas"], r["validas"], r["otimas"]), (3, 2, 1))
        self.assertAlmostEqual(r["pct_otimas"], 100 / 3)
        self.assertEqual(r["pct_sem_derrota"], 50.0)

    def test_resultado_para(self):
        tab = [ia.X, ia.X, ia.X, ia.O, ia.O, 0, 0, 0, 0]
        self.assertEqual(ia.resultado_para(tab, ia.X), "vitoria")
        self.assertEqual(ia.resultado_para(tab, ia.O), "derrota")
        self.assertIsNone(ia.resultado_para([0] * 9, ia.X))

    def test_contra_minimax_dificil_nunca_vence(self):
        r = ia.acuracia_contra_minimax(ia.DIFICIL, partidas=4)
        self.assertEqual(r["partidas"], 4)
        self.assertEqual(r["vitoria"], 0)


if __name__ == "__main__":
    unittest.main()
