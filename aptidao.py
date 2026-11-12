"""Função de aptidão: quão bem uma rede joga contra o Minimax.

Por partida (valores em config.py):
    +10 por jogada válida
    fim: vitória +50, empate +30, derrota 0, jogada inválida -20 (encerra)

Difícil: 2 partidas (rede começa / Minimax começa). Máximo = 150.
Médio:   K partidas alternando quem começa; usa a média.
"""

import config
from jogo import novo_tabuleiro, estado, jogada_valida, X, O  # noqa: F401
from minimax import jogada_minimax, MEDIO, DIFICIL  # noqa: F401


def jogar_partida(rede, modo, rede_comeca, rng):
    """Joga uma partida rede x Minimax até o fim.

    Retorna um dict com: pontos, resultado ("vitoria", "empate", "derrota",
    "invalida"), jogadas_validas e o histórico de tabuleiros (para o front).
    """
    # TODO (etapa 4): quem começa joga de X. Controle do fim com estado().
    raise NotImplementedError


def aptidao_dificil(rede, rng):
    # TODO (etapa 4): soma das 2 partidas (rede começa e Minimax começa)
    raise NotImplementedError


def aptidao_medio(rede, rng, k=config.PARTIDAS_MEDIO):
    # TODO (etapa 4): média de k partidas alternando quem começa
    raise NotImplementedError


def aptidao(rede, fase, rng):
    """fase: "medio", "misto" ou "dificil" (ordem dos modos no treino)."""
    # TODO (etapa 4): misto = 0.5*medio + 0.5*dificil, normalizados
    raise NotImplementedError
