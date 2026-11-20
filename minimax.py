"""Minimax adaptado com dois modos de jogo.

- Difícil: usa o Minimax em 100% das jogadas.
- Médio:   em cada jogada sorteia; 50% Minimax, 50% casa livre aleatória.

Detalhes:
- Desempate aleatório: quando várias casas têm o mesmo melhor valor, o
  Minimax sorteia uma delas. Continua sendo Minimax (toda jogada é ótima),
  mas o Difícil não joga sempre a mesma partida; assim a rede não consegue
  só decorar 2 partidas e precisa de várias para ser avaliada.
  `melhor_jogada_minimax` mantém o desempate pelo menor índice (determinístico).
- Memoização (lru_cache): o jogo da velha tem poucos estados, então cada
  tabuleiro é calculado uma vez só. Isso deixa a avaliação do AG rápida.
- Vitórias mais rápidas (e derrotas mais demoradas) valem mais.

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


def melhores_jogadas(tab, vez):
    """Todas as casas com o melhor valor Minimax exato para `vez`
    (inclui preferir vitória mais rápida / derrota mais demorada)."""
    tab = tuple(tab)
    valores = {casa: -_avaliar(tab[:casa] + (vez,) + tab[casa + 1:], -vez)[0]
               for casa in casas_livres(tab)}
    if not valores:
        return []
    melhor = max(valores.values())
    return [casa for casa, valor in valores.items() if valor == melhor]


def jogadas_otimas(tab, vez):
    """Casas que mantêm o melhor resultado possível (vitória, empate ou
    derrota) para `vez`, com jogo perfeito dos dois lados.

    `melhor_jogada_minimax` devolve só a de menor índice; para medir a
    acurácia da rede qualquer jogada que não piora o resultado conta.
    Compara só o resultado (sinal), não a rapidez da vitória.
    """
    tab = tuple(tab)
    valores = {}
    for casa in casas_livres(tab):
        v = -_avaliar(tab[:casa] + (vez,) + tab[casa + 1:], -vez)[0]
        valores[casa] = (v > 0) - (v < 0)
    if not valores:
        return []
    melhor = max(valores.values())
    return [casa for casa, valor in valores.items() if valor == melhor]


def jogada_minimax(tab, vez, modo=DIFICIL, rng=random):
    """Jogada do Minimax no modo pedido. `rng` permite usar uma seed fixa.

    Entre jogadas igualmente boas, sorteia uma (desempate aleatório).
    """
    if modo not in MODOS:
        raise ValueError(f"modo inválido: {modo!r}")
    if modo == MEDIO and rng.random() >= PROB_MINIMAX_MEDIO:
        return rng.choice(casas_livres(tab))
    return rng.choice(melhores_jogadas(tab, vez))
