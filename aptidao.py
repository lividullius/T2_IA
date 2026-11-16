"""Aptidão: quão bem a rede joga contra o Minimax.

Por partida: +10 por jogada válida, e no fim
vitória +50, empate +30, derrota 0, jogada inválida -20.

Difícil: 2 partidas (rede começa e Minimax começa). Máximo = 150.
Médio:   média de K partidas.
Misto:   metade Médio, metade Difícil.
"""

import config
from jogo import EMPATE, O, TEM_JOGO, X, estado, jogada_valida, novo_tabuleiro
from minimax import DIFICIL, MEDIO, jogada_minimax

MISTO = "misto"
FASES = (MEDIO, MISTO, DIFICIL)


def jogar_partida(rede, modo, rede_comeca, rng):
    """Joga uma partida rede x Minimax. Quem começa é X.

    Devolve: pontos, resultado, jogadas_validas, simbolo_rede e historico.
    """
    tab = novo_tabuleiro()
    simbolo_rede = X if rede_comeca else O
    vez = X
    validas = 0
    historico = []

    while estado(tab) == TEM_JOGO:
        if vez == simbolo_rede:
            casa = rede.jogada(tab, simbolo_rede)
            if not jogada_valida(tab, casa):  # casa ocupada: acaba a partida
                historico.append({"jogador": "rede", "casa": casa,
                                  "valida": False, "tabuleiro": tuple(tab)})
                return _fim(validas, "invalida", simbolo_rede, historico)
            validas += 1
            jogador = "rede"
        else:
            casa = jogada_minimax(tab, -simbolo_rede, modo, rng)
            jogador = "minimax"
        tab[casa] = vez
        historico.append({"jogador": jogador, "casa": casa,
                          "valida": True, "tabuleiro": tuple(tab)})
        vez = -vez

    final = estado(tab)
    if final == EMPATE:
        resultado = "empate"
    elif (final == "X venceu") == (simbolo_rede == X):
        resultado = "vitoria"
    else:
        resultado = "derrota"
    return _fim(validas, resultado, simbolo_rede, historico)


_BONUS = {
    "vitoria": config.BONUS_VITORIA,
    "empate": config.BONUS_EMPATE,
    "derrota": config.BONUS_DERROTA,
    "invalida": config.PENALIDADE_INVALIDA,
}


def _fim(validas, resultado, simbolo_rede, historico):
    return {
        "pontos": validas * config.PONTOS_JOGADA_VALIDA + _BONUS[resultado],
        "resultado": resultado,
        "jogadas_validas": validas,
        "simbolo_rede": simbolo_rede,
        "historico": historico,
    }


def aptidao_dificil(rede, rng):
    """Soma de 2 partidas: rede começa e Minimax começa."""
    return sum(jogar_partida(rede, DIFICIL, comeca, rng)["pontos"]
               for comeca in (True, False))


def aptidao_medio(rede, rng, k=None):
    """Média de k partidas, alternando quem começa."""
    k = k or config.PARTIDAS_MEDIO
    total = sum(jogar_partida(rede, MEDIO, i % 2 == 0, rng)["pontos"]
                for i in range(k))
    return total / k


def aptidao(rede, fase, rng):
    """Aptidão da rede na fase: "medio", "misto" ou "dificil"."""
    if fase == MEDIO:
        return aptidao_medio(rede, rng)
    if fase == DIFICIL:
        return aptidao_dificil(rede, rng)
    if fase == MISTO:
        # cada parte vai para 0..1 e o total volta para a escala 0..150
        medio = aptidao_medio(rede, rng) / config.APTIDAO_MAX_PARTIDA
        dificil = aptidao_dificil(rede, rng) / config.APTIDAO_IDEAL_DIFICIL
        return config.APTIDAO_IDEAL_DIFICIL * (0.5 * medio + 0.5 * dificil)
    raise ValueError(f"fase inválida: {fase!r}")
