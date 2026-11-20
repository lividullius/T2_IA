"""Aptidão: quão bem a rede joga contra o Minimax.

Por partida: +10 por jogada válida, +PONTOS_JOGADA_OTIMA por jogada ótima
(segundo o Minimax), -20 por jogada inválida; no fim vitória +50,
empate +30, derrota 0.

A aptidão de uma rede numa geração é a média de pontos por partida em
PARTIDAS_POR_AVALIACAO partidas, misturando Médio e Difícil conforme a fase
(ex.: 70% Médio / 30% Difícil). Em cada modo alterna quem começa.
Como o Minimax desempata ao acaso, até o Difícil precisa de várias partidas.
"""

import config
from jogo import (
    EMPATE, O, TEM_JOGO, X, casas_livres, estado, jogada_valida, novo_tabuleiro,
)
from minimax import DIFICIL, MEDIO, jogada_minimax, jogadas_otimas

FASES = config.FASES


def _casa_livre_preferida(rede, tab, simbolo):
    """Casa livre com maior saída da rede (usada após uma jogada inválida)."""
    livres = casas_livres(tab)
    if not hasattr(rede, "propagar"):
        return livres[0]
    saidas = rede.propagar([v * simbolo for v in tab])
    return max(livres, key=saidas.__getitem__)


def jogar_partida(rede, modo, rede_comeca, rng):
    """Joga uma partida rede x Minimax. Quem começa é X.

    Jogada inválida: perde PENALIDADE_INVALIDA. Se INVALIDA_ENCERRA, a
    partida acaba ali; senão a rede joga a casa livre com maior saída e a
    partida continua (cada erro é contado).
    Devolve: pontos, resultado, jogadas_validas, jogadas_invalidas,
    jogadas_otimas, simbolo_rede e historico.
    """
    tab = novo_tabuleiro()
    simbolo_rede = X if rede_comeca else O
    vez = X
    cont = {"validas": 0, "invalidas": 0, "otimas": 0}
    historico = []

    while estado(tab) == TEM_JOGO:
        if vez == simbolo_rede:
            jogador = "rede"
            casa = rede.jogada(tab, simbolo_rede)
            valida = jogada_valida(tab, casa)
            if valida:
                cont["validas"] += 1
                if (config.PONTOS_JOGADA_OTIMA
                        and casa in jogadas_otimas(tab, simbolo_rede)):
                    cont["otimas"] += 1
            else:
                cont["invalidas"] += 1
                historico.append({"jogador": jogador, "casa": casa,
                                  "valida": False, "tabuleiro": tuple(tab)})
                if config.INVALIDA_ENCERRA:
                    return _fim(cont, "invalida", simbolo_rede, historico)
                casa = _casa_livre_preferida(rede, tab, simbolo_rede)
        else:
            jogador = "minimax"
            casa = jogada_minimax(tab, -simbolo_rede, modo, rng)
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
    return _fim(cont, resultado, simbolo_rede, historico)


_BONUS = {
    "vitoria": config.BONUS_VITORIA,
    "empate": config.BONUS_EMPATE,
    "derrota": config.BONUS_DERROTA,
    "invalida": 0,  # a penalidade já entra por jogada inválida
}


def _fim(cont, resultado, simbolo_rede, historico):
    pontos = (cont["validas"] * config.PONTOS_JOGADA_VALIDA
              + cont["otimas"] * config.PONTOS_JOGADA_OTIMA
              + cont["invalidas"] * config.PENALIDADE_INVALIDA
              + _BONUS[resultado])
    return {
        "pontos": pontos,
        "resultado": resultado,
        "jogadas_validas": cont["validas"],
        "jogadas_invalidas": cont["invalidas"],
        "jogadas_otimas": cont["otimas"],
        "simbolo_rede": simbolo_rede,
        "historico": historico,
    }


def _media_partidas(rede, modo, k, rng):
    """Média de pontos em k partidas no modo, alternando quem começa."""
    if k <= 0:
        return 0.0
    return sum(jogar_partida(rede, modo, i % 2 == 0, rng)["pontos"]
               for i in range(k)) / k


def aptidao_dificil(rede, rng, k=None):
    """Média de k partidas contra o Difícil, alternando quem começa."""
    return _media_partidas(rede, DIFICIL, k or config.PARTIDAS_POR_AVALIACAO, rng)


def aptidao_medio(rede, rng, k=None):
    """Média de k partidas contra o Médio, alternando quem começa."""
    return _media_partidas(rede, MEDIO, k or config.PARTIDAS_POR_AVALIACAO, rng)


def fracao_medio(fase):
    """Fase -> fração das partidas contra o Médio ("medio"=1, "dificil"=0)."""
    if fase == MEDIO:
        return 1.0
    if fase == DIFICIL:
        return 0.0
    if isinstance(fase, (int, float)) and 0 <= fase <= 1:
        return float(fase)
    raise ValueError(f"fase inválida: {fase!r}")


def nome_fase(fase):
    """Rótulo para logs e front, ex.: 0.7 -> "M70/D30"."""
    m = round(100 * fracao_medio(fase))
    return f"M{m}/D{100 - m}"


def aptidao(rede, fase, rng, total=None):
    """Média de pontos por partida numa mistura de Médio e Difícil.

    `fase` é a fração das partidas contra o Médio (ex.: 0.7 = 70% Médio e
    30% Difícil); também aceita "medio" ou "dificil". Cada modo alterna
    quem começa. Ex.: 20 partidas com fase 0.7 -> 14 Médio + 6 Difícil.
    """
    total = total or config.PARTIDAS_POR_AVALIACAO
    k_medio = round(total * fracao_medio(fase))
    k_dificil = total - k_medio
    soma = (_media_partidas(rede, MEDIO, k_medio, rng) * k_medio
            + _media_partidas(rede, DIFICIL, k_dificil, rng) * k_dificil)
    return soma / total
