"""Rede neural MLP de 2 camadas (só propagação, sem backpropagation).

Topologia: 9 entradas -> N_OCULTOS neurônios (tanh) -> 9 saídas (logística).
Cada neurônio tem bias. Com 9 ocultos: 9*(9+1) + 9*(9+1) = 180 pesos.

Layout do cromossomo (vetor de pesos):
    genes 0 .. 89    camada oculta, neurônio a neurônio: [bias, w1..w9]
    genes 90 .. 179  camada de saída, neurônio a neurônio: [bias, w1..w9]

Neurônio j:  v_j = w_j0 + sum(p_i * w_ji)    y_j = f(v_j)

Entrada da rede (sempre do ponto de vista da rede):
    1 = peça da rede, -1 = peça do adversário, 0 = vazio
"""

import config


class Rede:
    def __init__(self, pesos, n_ocultos=config.N_OCULTOS):
        # TODO (etapa 3): conferir len(pesos) e separar em pesos da oculta
        # e da saída (duas listas/matrizes).
        raise NotImplementedError

    def propagar(self, entrada):
        """Recebe 9 valores e devolve as 9 saídas."""
        # TODO (etapa 3)
        raise NotImplementedError

    def jogada(self, tab, meu_simbolo):
        """Converte o tabuleiro para o ponto de vista da rede e devolve o
        índice da saída mais ativada (argmax). Pode ser casa ocupada: quem
        chama trata como jogada inválida."""
        # TODO (etapa 3): entrada = [v * meu_simbolo for v in tab]
        raise NotImplementedError


def salvar_pesos(pesos, caminho=config.ARQUIVO_MELHOR_MODELO):
    # TODO (etapa 5): salvar em JSON (pesos + topologia + aptidão)
    raise NotImplementedError


def carregar_pesos(caminho=config.ARQUIVO_MELHOR_MODELO):
    # TODO (etapa 6): ler o JSON salvo e devolver a lista de pesos
    raise NotImplementedError
