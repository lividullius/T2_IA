"""Algoritmo genético que evolui os pesos da rede.

Cada geração: avaliar -> elitismo -> torneio -> crossover -> mutação.
Fases do treino (fração de partidas contra Médio / Difícil):
70/30 -> 50/50 -> 30/70. Muda de fase quando não melhora mais.
Para por convergência (sem melhora na última fase) ou pelo limite de
gerações.

Rodar:  python3 algoritmoGenetico.py [--geracoes N] [--populacao N] [--seed S]
"""

import argparse
import csv
import random
from pathlib import Path

import config
from aptidao import FASES, aptidao, nome_fase
from redeMlp import Rede, n_genes, salvar_pesos


def populacao_inicial(n, n_genes, rng):
    return [[rng.uniform(config.PESO_MIN, config.PESO_MAX)
             for _ in range(n_genes)] for _ in range(n)]


def avaliar_populacao(populacao, fase, rng):
    """Devolve a aptidão de cada indivíduo."""
    # mesma semente para todos: enfrentam as mesmas jogadas aleatórias
    semente = rng.randrange(2 ** 32)
    return [aptidao(Rede(pesos), fase, random.Random(semente))
            for pesos in populacao]


def torneio(populacao, aptidoes, rng, k=None):
    """Sorteia k indivíduos e devolve o melhor (veio da versaoDiferente)."""
    k = k or config.TAMANHO_TORNEIO
    participantes = rng.sample(range(len(populacao)), k)
    vencedor = max(participantes, key=aptidoes.__getitem__)
    return populacao[vencedor]


def crossover(pai, mae, rng, tipo=None, alfa=None):
    """Crossover para reais, devolve dois filhos.

    aritmético (veio da versaoDiferente): mistura pai e mãe com um peso
    sorteado por gene. blx: sorteia cada gene perto dos valores dos pais.
    """
    tipo = tipo or config.CROSSOVER
    alfa = config.BLX_ALFA if alfa is None else alfa
    if tipo == "aritmetico":
        filho1, filho2 = [], []
        for a, b in zip(pai, mae):
            beta = rng.random()
            filho1.append(beta * a + (1 - beta) * b)
            filho2.append(beta * b + (1 - beta) * a)
        return filho1, filho2
    if tipo == "blx":
        def gene(a, b):
            d = abs(a - b)
            valor = rng.uniform(min(a, b) - alfa * d, max(a, b) + alfa * d)
            return min(max(valor, config.PESO_MIN), config.PESO_MAX)
        return ([gene(a, b) for a, b in zip(pai, mae)],
                [gene(a, b) for a, b in zip(pai, mae)])
    raise ValueError(f"crossover inválido: {tipo!r}")


def mutacao(populacao, rng, taxa=None, protegidas=None):
    """Troca genes sorteados por um valor aleatório em [-1, 1].

    A elite (primeiras linhas) nunca muda. Devolve quantas mutações fez.
    """
    taxa = config.TAXA_MUTACAO if taxa is None else taxa
    protegidas = config.ELITISMO if protegidas is None else protegidas
    linhas = len(populacao) - protegidas
    if linhas <= 0:
        return 0
    n_col = len(populacao[0])
    media = taxa * linhas * n_col
    quantidade = int(media) + (1 if rng.random() < media - int(media) else 0)
    for _ in range(quantidade):
        linha = rng.randrange(protegidas, len(populacao))
        coluna = rng.randrange(n_col)
        populacao[linha][coluna] = rng.uniform(config.PESO_MIN,
                                               config.PESO_MAX)
    return quantidade


def proxima_geracao(populacao, aptidoes, rng):
    """Monta a nova população: elitismo + torneio + crossover + mutação."""
    n = len(populacao)
    ordem = sorted(range(n), key=aptidoes.__getitem__, reverse=True)
    nova = [list(populacao[i]) for i in ordem[:config.ELITISMO]]
    while len(nova) < n:
        pai = torneio(populacao, aptidoes, rng)
        mae = torneio(populacao, aptidoes, rng)
        for filho in crossover(pai, mae, rng):
            if len(nova) < n:
                nova.append(filho)
    mutacao(nova, rng)
    return nova


def treinar(rng=None, ao_fim_da_geracao=None,
            n=None, max_geracoes=None, caminho_log=config.ARQUIVO_LOG,
            caminho_modelo=config.ARQUIVO_MELHOR_MODELO):
    """Loop do treino. Salva o melhor modelo e o log CSV.

    `ao_fim_da_geracao(info)` é chamada a cada geração (para o front).
    Se ela devolver False, o treino para.
    """
    rng = rng or random.Random(config.SEED)
    n = n or config.TAMANHO_POPULACAO
    max_geracoes = max_geracoes or config.MAX_GERACOES
    populacao = populacao_inicial(n, n_genes(), rng)
    indice_fase = 0
    melhor_da_fase = float("-inf")
    sem_melhora = 0
    geracoes_na_fase = 0
    ultimas = []  # melhores aptidões recentes (média móvel)
    motivo = "max_geracoes"

    arquivo_log = None
    if caminho_log:
        Path(caminho_log).parent.mkdir(parents=True, exist_ok=True)
        arquivo_log = open(caminho_log, "w", newline="", encoding="utf-8")
        escritor = csv.writer(arquivo_log)
        escritor.writerow(["geracao", "fase", "melhor", "media", "pior"])

    try:
        for geracao in range(1, max_geracoes + 1):
            fase = nome_fase(FASES[indice_fase])
            aptidoes = avaliar_populacao(populacao, FASES[indice_fase], rng)
            indice_melhor = max(range(n), key=aptidoes.__getitem__)
            melhor = aptidoes[indice_melhor]
            media = sum(aptidoes) / n
            pior = min(aptidoes)

            # convergência pela média móvel da melhor aptidão: as partidas
            # são aleatórias, então uma geração com sorte não conta sozinha
            ultimas = (ultimas + [melhor])[-config.JANELA_CONVERGENCIA:]
            tendencia = sum(ultimas) / len(ultimas)
            if tendencia > melhor_da_fase + 1e-9:
                melhor_da_fase = tendencia
                sem_melhora = 0
            else:
                sem_melhora += 1
            geracoes_na_fase += 1

            if arquivo_log:
                escritor.writerow([geracao, fase, f"{melhor:.4f}",
                                   f"{media:.4f}", f"{pior:.4f}"])
                arquivo_log.flush()

            if ao_fim_da_geracao is not None:
                continuar = ao_fim_da_geracao({
                    "geracao": geracao, "fase": fase,
                    "indice_fase": indice_fase,
                    "populacao": populacao, "aptidoes": aptidoes,
                    "melhor": melhor, "media": media, "pior": pior,
                    "indice_melhor": indice_melhor,
                    "sem_melhora": sem_melhora,
                })
                if continuar is False:
                    motivo = "interrompido"
                    break

            # critérios de parada
            ultima_fase = indice_fase == len(FASES) - 1
            if ultima_fase and sem_melhora >= config.PACIENCIA:
                motivo = "convergencia"
                break
            if geracao == max_geracoes:
                break

            if not ultima_fase and (
                    sem_melhora >= config.PACIENCIA_FASE
                    or geracoes_na_fase >= config.MAX_GERACOES_FASE):
                # passa para a próxima fase
                indice_fase += 1
                melhor_da_fase = float("-inf")
                ultimas = []
                sem_melhora = 0
                geracoes_na_fase = 0

            populacao = proxima_geracao(populacao, aptidoes, rng)
    finally:
        if arquivo_log:
            arquivo_log.close()

    resultado = {
        "pesos": list(populacao[indice_melhor]),
        "aptidao": melhor,
        "fase": fase,
        "geracao": geracao,
        "motivo": motivo,
    }
    if caminho_modelo:
        salvar_pesos(resultado["pesos"], caminho_modelo,
                     aptidao=melhor, fase=fase, geracao=geracao)
    return resultado


def _imprimir(info):
    print(f"  ger {info['geracao']:3d}  [{info['fase']}]  "
          f"melhor {info['melhor']:7.2f}  media {info['media']:7.2f}  "
          f"pior {info['pior']:7.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Treina a rede com o AG.")
    parser.add_argument("--geracoes", type=int, default=config.MAX_GERACOES)
    parser.add_argument("--populacao", type=int,
                        default=config.TAMANHO_POPULACAO)
    parser.add_argument("--seed", type=int, default=config.SEED)
    args = parser.parse_args()

    fim = treinar(random.Random(args.seed), _imprimir,
                  n=args.populacao, max_geracoes=args.geracoes)
    print(f"\n  Parou na geração {fim['geracao']} ({fim['motivo']}), "
          f"fase {fim['fase']}, melhor aptidão {fim['aptidao']:.2f}.")
    print(f"  Modelo salvo em {config.ARQUIVO_MELHOR_MODELO}")
    print(f"  Log em {config.ARQUIVO_LOG}")
