"""Funções prontas para o front end: inferência da rede, Minimax, estado do
jogo, treino e acurácia. O front só precisa importar este módulo.

Tabuleiro: lista de 9 valores (X = 1, O = -1, vazio = 0), índices 0..8.

Exemplo:
    import ia
    tab = ia.novo_tabuleiro()
    if not ia.modelo_existe():
        ia.treinar()                        # só treina se não houver modelo
    j = ia.jogada_rede(tab, ia.X)           # {"casa": 4, "valida": True, ...}
    tab[j["casa"]] = ia.X
    tab[ia.jogada_minimax(tab, ia.O, ia.DIFICIL)] = ia.O
    ia.estado_jogo(tab)                     # "Tem jogo"

O modelo é lido do JSON uma vez e fica em memória; o treino salva o novo
modelo no arquivo e já troca o da memória.
"""

import random
from pathlib import Path

import algoritmoGenetico
import config
from jogo import (  # noqa: F401  (reexportados para o front)
    EMPATE, O, O_VENCEU, TEM_JOGO, VAZIO, X, X_VENCEU, casas_livres, estado,
    fim_de_jogo, jogada_valida, novo_tabuleiro, vencedor,
)
from minimax import DIFICIL, MEDIO, jogadas_otimas  # noqa: F401
from minimax import jogada_minimax as _jogada_minimax
from redeMlp import N_SAIDAS, carregar_rede

_modelos = {}  # caminho resolvido -> Rede


def _caminho(caminho):
    return Path(caminho or config.ARQUIVO_MELHOR_MODELO).resolve()


# ------------------------------------------------------------- modelo

def modelo_existe(caminho=None):
    """True se já existe um modelo salvo (não precisa treinar)."""
    return _caminho(caminho).is_file()


def carregar_modelo(caminho=None, recarregar=False):
    """Devolve a Rede salva. Lê o arquivo só na primeira vez.

    Lança FileNotFoundError se não houver modelo (chame treinar() antes).
    """
    chave = _caminho(caminho)
    if recarregar or chave not in _modelos:
        if not chave.is_file():
            raise FileNotFoundError(
                f"nenhum modelo em {chave}; rode ia.treinar() primeiro")
        _modelos[chave] = carregar_rede(chave)
    return _modelos[chave]


def treinar(ao_fim_da_geracao=None, populacao=None, geracoes=None,
            seed=None, caminho=None, caminho_log=config.ARQUIVO_LOG):
    """Roda o AG, salva o melhor modelo e já o deixa carregado.

    `ao_fim_da_geracao(info)` é chamada a cada geração com geracao, fase,
    populacao, aptidoes, melhor, media, pior, indice_melhor e sem_melhora.
    Se devolver False, o treino para (o melhor até ali é salvo).
    Devolve pesos, aptidao, fase, geracao e motivo da parada.
    """
    chave = _caminho(caminho)
    rng = random.Random(config.SEED if seed is None else seed)
    resultado = algoritmoGenetico.treinar(
        rng, ao_fim_da_geracao, n=populacao, max_geracoes=geracoes,
        caminho_log=caminho_log, caminho_modelo=str(chave))
    carregar_modelo(chave, recarregar=True)
    return resultado


# ---------------------------------------------------------- jogadas

def jogada_rede(tab, simbolo, rede=None, corrigir=True):
    """Jogada da rede para o jogador `simbolo` (X ou O).

    Devolve um dict:
        casa      casa a jogar (0..8)
        escolhida casa que a rede escolheu de fato (maior saída)
        valida    se a escolhida estava livre
        saidas    as 9 saídas da rede (para mostrar no front, se quiser)

    Com corrigir=True (padrão), se a rede escolher casa ocupada, `casa` é a
    casa livre com maior saída, para a partida continuar; a jogada inválida
    deve ser contada como erro na acurácia. Com corrigir=False, `casa` é
    sempre a escolhida (pode estar ocupada).
    """
    rede = rede or carregar_modelo()
    saidas = rede.propagar([v * simbolo for v in tab])
    escolhida = max(range(N_SAIDAS), key=saidas.__getitem__)
    valida = jogada_valida(tab, escolhida)
    casa = escolhida
    if not valida and corrigir:
        casa = max(casas_livres(tab), key=saidas.__getitem__)
    return {"casa": casa, "escolhida": escolhida, "valida": valida,
            "saidas": saidas}


def jogada_minimax(tab, simbolo, modo=DIFICIL, rng=None):
    """Jogada do Minimax ("medio" ou "dificil") para o jogador `simbolo`."""
    return _jogada_minimax(tab, simbolo, modo, rng or random)


def estado_jogo(tab):
    """"Tem jogo", "X venceu", "O venceu" ou "Empate"."""
    return estado(tab)


def resultado_para(tab, simbolo):
    """"vitoria", "empate" ou "derrota" para `simbolo`; None se tem jogo."""
    final = estado(tab)
    if final == TEM_JOGO:
        return None
    if final == EMPATE:
        return "empate"
    return "vitoria" if (final == X_VENCEU) == (simbolo == X) else "derrota"


# ---------------------------------------------------------- acurácia

class Acuracia:
    """Acumula a acurácia da rede ao longo de várias partidas.

    Uso no front (modo humano x rede):
        acc = ia.Acuracia()
        j = ia.jogada_rede(tab, simbolo_rede)
        acc.registrar_jogada(tab, simbolo_rede, j["escolhida"])  # ANTES de jogar
        ...
        acc.registrar_resultado(ia.resultado_para(tab, simbolo_rede))
        acc.resumo()

    Métricas:
        validas  % de jogadas da rede em casa livre
        otimas   % de jogadas que mantêm o melhor resultado possível
                 (segundo o Minimax); jogada inválida conta como não ótima
        vitorias / empates / derrotas da rede, e % de partidas sem derrota
    """

    def __init__(self):
        self.jogadas = 0
        self.validas = 0
        self.otimas = 0
        self.resultados = {"vitoria": 0, "empate": 0, "derrota": 0}

    def registrar_jogada(self, tab, simbolo, casa):
        """Registra a casa escolhida pela rede no tabuleiro antes da jogada.

        Devolve {"valida": bool, "otima": bool}.
        """
        valida = jogada_valida(tab, casa)
        otima = valida and casa in jogadas_otimas(tab, simbolo)
        self.jogadas += 1
        self.validas += valida
        self.otimas += otima
        return {"valida": valida, "otima": otima}

    def registrar_resultado(self, resultado):
        """resultado: "vitoria", "empate" ou "derrota" (visão da rede)."""
        if resultado is not None:
            self.resultados[resultado] += 1

    def resumo(self):
        partidas = sum(self.resultados.values())

        def pct(parte, total):
            return 100.0 * parte / total if total else 0.0

        return {
            "jogadas": self.jogadas,
            "validas": self.validas,
            "otimas": self.otimas,
            "pct_validas": pct(self.validas, self.jogadas),
            "pct_otimas": pct(self.otimas, self.jogadas),
            "partidas": partidas,
            **self.resultados,
            "pct_sem_derrota": pct(partidas - self.resultados["derrota"],
                                   partidas),
        }


def acuracia_contra_minimax(modo=MEDIO, partidas=100, rede=None, seed=0):
    """Joga a rede contra o Minimax e devolve Acuracia.resumo().

    Alterna quem começa. Jogadas inválidas são corrigidas (casa livre com
    maior saída) para a partida ir até o fim. Útil para o relatório.
    """
    rede = rede or carregar_modelo()
    rng = random.Random(seed)
    acc = Acuracia()
    for i in range(partidas):
        tab = novo_tabuleiro()
        simbolo_rede = X if i % 2 == 0 else O
        vez = X
        while not fim_de_jogo(tab):
            if vez == simbolo_rede:
                j = jogada_rede(tab, simbolo_rede, rede)
                acc.registrar_jogada(tab, simbolo_rede, j["escolhida"])
                casa = j["casa"]
            else:
                casa = jogada_minimax(tab, vez, modo, rng)
            tab[casa] = vez
            vez = -vez
        acc.registrar_resultado(resultado_para(tab, simbolo_rede))
    return acc.resumo()
