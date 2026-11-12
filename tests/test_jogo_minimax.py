"""Testes das etapas 1 e 2.  Rodar:  python3 -m unittest discover tests"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from jogo import (  # noqa: E402
    EMPATE, LINHAS, O, O_VENCEU, TEM_JOGO, X, X_VENCEU,
    casas_livres, estado, jogada_valida, novo_tabuleiro,
)
from minimax import DIFICIL, MEDIO, jogada_minimax, melhor_jogada_minimax  # noqa: E402


def partida(jogador_x, jogador_o):
    tab = novo_tabuleiro()
    vez = X
    while estado(tab) == TEM_JOGO:
        casa = (jogador_x if vez == X else jogador_o)(tab, vez)
        assert jogada_valida(tab, casa)
        tab[casa] = vez
        vez = -vez
    return estado(tab)


class TestJogo(unittest.TestCase):
    def test_todas_as_linhas_de_vitoria(self):
        for linha in LINHAS:
            for jogador, esperado in ((X, X_VENCEU), (O, O_VENCEU)):
                tab = novo_tabuleiro()
                for i in linha:
                    tab[i] = jogador
                self.assertEqual(estado(tab), esperado)

    def test_empate(self):
        tab = [X, O, X,
               X, O, O,
               O, X, X]
        self.assertEqual(estado(tab), EMPATE)

    def test_casa_ocupada(self):
        tab = novo_tabuleiro()
        tab[4] = X
        self.assertFalse(jogada_valida(tab, 4))
        self.assertTrue(jogada_valida(tab, 0))
        self.assertNotIn(4, casas_livres(tab))


class TestMinimax(unittest.TestCase):
    def test_completa_vitoria(self):
        tab = [X, X, 0,
               O, O, 0,
               0, 0, 0]
        self.assertEqual(melhor_jogada_minimax(tab, X), 2)
        self.assertEqual(melhor_jogada_minimax(tab, O), 5)

    def test_bloqueia(self):
        tab = [X, X, 0,
               0, O, 0,
               0, 0, 0]
        self.assertEqual(melhor_jogada_minimax(tab, O), 2)

    def test_dificil_contra_dificil_empata(self):
        def dificil(t, v):
            return jogada_minimax(t, v, DIFICIL)
        self.assertEqual(partida(dificil, dificil), EMPATE)

    def test_dificil_nunca_perde_para_aleatorio(self):
        rng = random.Random(0)

        def aleatorio(t, _v):
            return rng.choice(casas_livres(t))

        def dificil(t, v):
            return jogada_minimax(t, v, DIFICIL)

        for i in range(1000):
            if i % 2 == 0:
                self.assertNotEqual(partida(dificil, aleatorio), O_VENCEU)
            else:
                self.assertNotEqual(partida(aleatorio, dificil), X_VENCEU)

    def test_medio_as_vezes_perde_para_dificil(self):
        rng = random.Random(1)

        def medio(t, v):
            return jogada_minimax(t, v, MEDIO, rng)

        def dificil(t, v):
            return jogada_minimax(t, v, DIFICIL)

        resultados = {partida(dificil, medio) for _ in range(200)}
        self.assertIn(X_VENCEU, resultados)
        self.assertNotIn(O_VENCEU, resultados)


if __name__ == "__main__":
    unittest.main()
