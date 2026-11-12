"""Algoritmo genético que evolui os pesos da rede.

População: matriz N x 180 de doubles em [-1, 1]; cada linha é uma rede.
Ciclo por geração:
    1. avaliar cada linha (carregar pesos -> jogar -> gravar aptidão)
    2. elitismo: melhor linha vai para a linha 0 da nova população
    3. torneio: sorteia 2, o melhor é o pai; repete para a mãe
    4. crossover para reais (aritmético ou BLX-alfa)
    5. repete 3-4 até completar N
    6. mutação: sorteia linha (nunca a 0) e coluna, troca por real aleatório
    7. registra melhor/média/pior no log CSV
Fases: Médio -> Misto -> Difícil.
Parada: MAX_GERACOES ou convergência (aptidão ideal ou PACIENCIA sem melhora).
"""

import random

import config


def populacao_inicial(n, n_genes, rng):
    # TODO (etapa 5)
    raise NotImplementedError


def avaliar_populacao(populacao, fase, rng):
    # TODO (etapa 5): devolve a lista de aptidões (coluna ao lado da matriz)
    raise NotImplementedError


def torneio(populacao, aptidoes, rng, k=config.TAMANHO_TORNEIO):
    # TODO (etapa 5)
    raise NotImplementedError


def crossover(pai, mae, rng):
    # TODO (etapa 5): crossover para reais (ver Moodle)
    raise NotImplementedError


def mutacao(populacao, rng, taxa=config.TAXA_MUTACAO):
    # TODO (etapa 5)
    raise NotImplementedError


def proxima_geracao(populacao, aptidoes, rng):
    # TODO (etapa 5): elitismo + torneio + crossover + mutação
    raise NotImplementedError


def treinar(rng=None, ao_fim_da_geracao=None):
    """Loop principal. `ao_fim_da_geracao(info)` é chamado a cada geração
    para o front mostrar o passo a passo (geração, fase, aptidões, melhor)."""
    rng = rng or random.Random(config.SEED)
    # TODO (etapa 5)
    raise NotImplementedError


if __name__ == "__main__":
    treinar()
