"""Regras do jogo da velha.

Tabuleiro: lista (ou tupla) de 9 posições, índices 0..8 (casas 1..9 na tela).
    X = 1, O = -1, vazio = 0   (convenção da aula)

O estado do jogo é verificado por código (ifs), não por um classificador
como no T1.
"""

X = 1
O = -1
VAZIO = 0

LINHAS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # linhas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colunas
    (0, 4, 8), (2, 4, 6),             # diagonais
)

TEM_JOGO = "Tem jogo"
X_VENCEU = "X venceu"
O_VENCEU = "O venceu"
EMPATE = "Empate"


def novo_tabuleiro():
    return [VAZIO] * 9


def casas_livres(tab):
    return [i for i in range(9) if tab[i] == VAZIO]


def jogada_valida(tab, casa):
    return 0 <= casa < 9 and tab[casa] == VAZIO


def vencedor(tab):
    """Retorna X, O ou 0 (ninguém completou uma linha)."""
    for a, b, c in LINHAS:
        if tab[a] != VAZIO and tab[a] == tab[b] == tab[c]:
            return tab[a]
    return 0


def estado(tab):
    v = vencedor(tab)
    if v == X:
        return X_VENCEU
    if v == O:
        return O_VENCEU
    if VAZIO not in tab:
        return EMPATE
    return TEM_JOGO


def fim_de_jogo(tab):
    return estado(tab) != TEM_JOGO


def simbolo(valor):
    return {X: "X", O: "O"}.get(valor, " ")
