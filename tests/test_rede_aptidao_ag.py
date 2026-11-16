"""Testes das etapas 3, 4 e 5.  Rodar:  python3 -m unittest discover tests"""

import math
import random
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import ag  # noqa: E402
import config  # noqa: E402
from aptidao import (  # noqa: E402
    aptidao, aptidao_dificil, aptidao_medio, jogar_partida,
)
from jogo import O, X, casas_livres, novo_tabuleiro  # noqa: E402
from minimax import DIFICIL, MEDIO, melhor_jogada_minimax  # noqa: E402
from rede import Rede, carregar_rede, n_genes, salvar_pesos  # noqa: E402


class PrimeiraLivre:
    """'Rede' de teste que joga sempre na primeira casa livre."""
    def jogada(self, tab, _simbolo):
        return casas_livres(tab)[0]


class Perfeita:
    """'Rede' de teste que joga como o Minimax Difícil."""
    def jogada(self, tab, simbolo):
        return melhor_jogada_minimax(tab, simbolo)


class SempreCasa0:
    def jogada(self, _tab, _simbolo):
        return 0


class TestRede(unittest.TestCase):
    def test_180_pesos(self):
        self.assertEqual(n_genes(9), 180)
        self.assertEqual(config.N_PESOS, 180)
        with self.assertRaises(ValueError):
            Rede([0.0] * 179)

    def test_neuronio_a_mao(self):
        # Oculto j: bias = 0.1*j, w_i = 0.01*i.  Saída k: bias = -0.2, w = 0.05*k.
        pesos = []
        for j in range(9):
            pesos += [0.1 * j] + [0.01 * i for i in range(1, 10)]
        for k in range(9):
            pesos += [-0.2] + [0.05 * k] * 9
        entrada = [1, -1, 0, 0, 1, 0, -1, 0, 1]

        rede = Rede(pesos)
        saidas = rede.propagar(entrada)

        # v_j = w_j0 + sum(p_i * w_ji), y_j = tanh(v_j)
        soma = sum(p * 0.01 * i for i, p in enumerate(entrada, start=1))
        ocultos = [math.tanh(0.1 * j + soma) for j in range(9)]
        for k in range(9):
            v = -0.2 + sum(y * 0.05 * k for y in ocultos)
            self.assertAlmostEqual(saidas[k], 1 / (1 + math.exp(-v)))

    def test_ponto_de_vista_da_rede(self):
        # O mesmo tabuleiro visto pela rede jogando de X ou de O
        # (com as peças trocadas) leva à mesma jogada.
        rng = random.Random(3)
        rede = Rede([rng.uniform(-1, 1) for _ in range(180)])
        tab = [X, O, 0, 0, X, 0, O, 0, 0]
        espelho = [-v for v in tab]
        self.assertEqual(rede.jogada(tab, X), rede.jogada(espelho, O))

    def test_sem_mascara(self):
        # Saída 0 muito ativada: escolhe a casa 0 mesmo ocupada.
        pesos = [0.0] * 90
        for k in range(9):
            pesos += [5.0 if k == 0 else -5.0] + [0.0] * 9
        tab = novo_tabuleiro()
        tab[0] = O
        self.assertEqual(Rede(pesos).jogada(tab, X), 0)

    def test_salvar_e_carregar(self):
        pesos = [random.uniform(-1, 1) for _ in range(180)]
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "rede.json"
            salvar_pesos(pesos, caminho, aptidao=123.0)
            rede = carregar_rede(caminho)
        tab = [X, 0, O, 0, 0, 0, 0, 0, 0]
        self.assertEqual(rede.propagar(tab), Rede(pesos).propagar(tab))


class TestAptidao(unittest.TestCase):
    def test_perfeita_atinge_ideal(self):
        self.assertEqual(aptidao_dificil(Perfeita(), random.Random(0)),
                         config.APTIDAO_IDEAL_DIFICIL)

    def test_invalida_tarde_vale_mais(self):
        # Rede começa: casa 0 é válida na 1ª jogada e inválida na 2ª.
        p = jogar_partida(SempreCasa0(), DIFICIL, True, random.Random(0))
        self.assertEqual(p["resultado"], "invalida")
        self.assertEqual(p["pontos"], 10 - 20)
        self.assertFalse(p["historico"][-1]["valida"])

    def test_aleatoria_pior_que_primeira_livre(self):
        rng = random.Random(7)
        aleatorias = [aptidao_medio(Rede([rng.uniform(-1, 1)
                                          for _ in range(180)]),
                                    random.Random(1))
                      for _ in range(20)]
        primeira = aptidao_medio(PrimeiraLivre(), random.Random(1))
        self.assertGreater(primeira, sum(aleatorias) / len(aleatorias))

    def test_alterna_quem_comeca(self):
        rng = random.Random(0)
        a = jogar_partida(PrimeiraLivre(), MEDIO, True, rng)
        b = jogar_partida(PrimeiraLivre(), MEDIO, False, rng)
        self.assertEqual(a["simbolo_rede"], X)
        self.assertEqual(b["simbolo_rede"], O)
        self.assertEqual(b["historico"][0]["jogador"], "minimax")

    def test_misto_da_ideal_para_perfeita_no_dificil(self):
        valor = aptidao(Perfeita(), "misto", random.Random(0))
        self.assertGreater(valor, 0)
        self.assertLessEqual(valor, config.APTIDAO_IDEAL_DIFICIL)


class TestAG(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(0)
        self.pop = ag.populacao_inicial(10, 180, self.rng)

    def test_populacao(self):
        self.assertEqual(len(self.pop), 10)
        self.assertTrue(all(len(linha) == 180 for linha in self.pop))
        self.assertTrue(all(-1 <= g <= 1 for linha in self.pop for g in linha))

    def test_torneio_com_todos_pega_o_melhor(self):
        aptidoes = list(range(10))
        self.assertIs(ag.torneio(self.pop, aptidoes, self.rng, k=10),
                      self.pop[9])

    def test_crossover(self):
        pai, mae = self.pop[0], self.pop[1]
        for tipo in ("aritmetico", "blx"):
            f1, f2 = ag.crossover(pai, mae, self.rng, tipo)
            self.assertEqual(len(f1), 180)
            self.assertEqual(len(f2), 180)
            self.assertTrue(all(-1 <= g <= 1 for g in f1 + f2))
        f1, _ = ag.crossover(pai, mae, self.rng, "aritmetico")
        for g, a, b in zip(f1, pai, mae):
            self.assertTrue(min(a, b) - 1e-12 <= g <= max(a, b) + 1e-12)

    def test_mutacao_nao_toca_elite(self):
        elite = list(self.pop[0])
        antes = [list(linha) for linha in self.pop]
        feitas = ag.mutacao(self.pop, self.rng, taxa=0.5, protegidas=1)
        self.assertGreater(feitas, 0)
        self.assertEqual(self.pop[0], elite)
        self.assertNotEqual(self.pop[1:], antes[1:])

    def test_elitismo(self):
        aptidoes = [float(i) for i in range(10)]
        nova = ag.proxima_geracao(self.pop, aptidoes, self.rng)
        self.assertEqual(len(nova), 10)
        self.assertEqual(nova[0], self.pop[9])

    def test_treino_curto(self):
        with tempfile.TemporaryDirectory() as pasta:
            log = Path(pasta) / "log.csv"
            modelo = Path(pasta) / "rede.json"
            vistas = []
            fim = ag.treinar(random.Random(1), vistas.append, n=8,
                             max_geracoes=3, caminho_log=log,
                             caminho_modelo=modelo)
            self.assertEqual(len(vistas), 3)
            self.assertEqual(len(log.read_text().splitlines()), 4)
            self.assertTrue(modelo.exists())
            self.assertEqual(len(fim["pesos"]), 180)


if __name__ == "__main__":
    unittest.main()
