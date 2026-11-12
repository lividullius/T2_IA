"""Minimax adaptado com dois modos de jogo.

- Difícil: usa o Minimax em 100% das jogadas.
- Médio:   em cada jogada sorteia; 50% Minimax, 50% casa livre aleatória.

Detalhes:
- Desempate determinístico: entre jogadas de mesmo valor, fica a de menor
  índice. Assim o Difícil sempre joga igual no mesmo tabuleiro, e 1 partida
  basta para avaliar uma rede contra ele.
- Memoização (lru_cache): o jogo da velha tem poucos estados, então cada
  tabuleiro é calculado uma vez só. Isso deixa a avaliação do AG rápida.
- Vitórias mais rápidas (e derrotas mais demoradas) valem mais.

TODO: conferir com a versão do Minimax dada em aula e ajustar nomes, se
preciso, para a apresentação.
"""

import random
from functools import lru_cache

from jogo import casas_livres, vencedor

MEDIO = "medio"
DIFICIL = "dificil"
MODOS = (MEDIO, DIFICIL)
PROB_MINIMAX_MEDIO = 0.5


@lru_cache(maxsize=None)
def _avaliar(tab, vez):
    """Valor do tabuleiro para quem joga agora (`vez`) e a melhor casa.

    tab: tupla de 9 valores. Retorno: (valor, casa). valor > 0 = `vez` ganha.
    """
    livres = casas_livres(tab)
    if vencedor(tab) != 0:
        # quem jogou por último (-vez) venceu; quanto antes, pior para `vez`
        return -(1 + len(livres)), None
    if not livres:
        return 0, None

    melhor_valor, melhor_casa = None, None
    for casa in livres:  # ordem crescente -> desempate pelo menor índice
        filho = tab[:casa] + (vez,) + tab[casa + 1:]
        valor = -_avaliar(filho, -vez)[0]
        if melhor_valor is None or valor > melhor_valor:
            melhor_valor, melhor_casa = valor, casa
    return melhor_valor, melhor_casa


def melhor_jogada_minimax(tab, vez):
    """Casa escolhida pelo Minimax puro para o jogador `vez` (X=1 ou O=-1)."""
    return _avaliar(tuple(tab), vez)[1]


def jogada_minimax(tab, vez, modo=DIFICIL, rng=random):
    """Jogada do Minimax no modo pedido. `rng` permite usar uma seed fixa."""
    if modo not in MODOS:
        raise ValueError(f"modo inválido: {modo!r}")
    if modo == MEDIO and rng.random() >= PROB_MINIMAX_MEDIO:
        return rng.choice(casas_livres(tab))
    return melhor_jogada_minimax(tab, vez)
