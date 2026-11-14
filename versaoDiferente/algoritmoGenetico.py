import random
import numpy as np
from mlp import MLP
from minimax import verificarVencedor, jogadasDisponiveis, melhorJogada

tamPopulacao = 100
qtdElite = 2
tamTorneio = 3
taxaMutacao = 0.01

redeReferencia = MLP()
qtGenes = len(redeReferencia.obterParametros())

#Gera um individuo com 199 parametros aleatorios
def gerarIndividuo():
    individuo = np.random.uniform(-1, 1, qtGenes)

    return individuo

# Gera a populacao inicial
def gerarPopulacao():
    populacao = []
    for i in range(tamPopulacao):
        individuo = gerarIndividuo()
        populacao.append(individuo)

    return populacao

#Partida entre a MLP e o Minimax
def jogarPartida(rede, modo, jogadorRede, jogadorInicial):
    tabuleiro = [""] * 9
    if jogadorRede == "X":
        jogadorMinimax = "O"
    else:
        jogadorMinimax = "X"

    jogadorAtual = jogadorInicial
    while verificarVencedor(tabuleiro) is None:
        if jogadorAtual == jogadorRede: #Vez da rede neural
            jogada = rede.indicarJogada(tabuleiro)

            if tabuleiro[jogada] != "": #Verifica se não foi escolhida uma posição ocupada pela rede
                return "Jogada Inválida!"

        else: #Vez do minimax
            if modo == "medio" and random.random() < 0.5:
                jogada = random.choice(jogadasDisponiveis(tabuleiro))
            else:
                jogada = melhorJogada(tabuleiro, jogadorMinimax)

        tabuleiro[jogada] = jogadorAtual
        resultado = verificarVencedor(tabuleiro)

        if resultado is not None:
            return resultado
        
        if jogadorAtual == "X":
            jogadorAtual = "O"
        else:
            jogadorAtual = "X"



def avaliarIndividuo(individuo):
    rede = MLP()

    # Transfere os parametros do individuo para a rede
    rede.definirParametros(individuo)

    fitness = 0

    # Avalia o individuo em 20 partidas
    for i in range(20):

        # Define o modo de dificuldade
        if i < 10:
            modo = "medio"
        else:
            modo = "dificil"

        # Alterna entre a rede jogar como X e O
        if (i // 2) % 2 == 0:
            jogadorRede = "X"
        else:
            jogadorRede = "O"

        # Alterna quem começa a partida
        if i % 2 == 0:
            jogadorInicial = "X"
        else:
            jogadorInicial = "O"

        resultado = jogarPartida(
            rede,
            modo,
            jogadorRede,
            jogadorInicial
        )

        # Calcula a pontuacao da partida
        if resultado == "Empate":
            fitness += 5
        elif resultado == "Jogada Inválida!":
            fitness -= 10
        elif resultado == jogadorRede:
            fitness += 10
        else:
            fitness -= 5

    return fitness


# Seleciona um individuo atraves de um torneio
def selecaoTorneio(populacao, fitness):
    participantes = random.sample(range(len(populacao)), tamTorneio)
    melhorParticipante = participantes[0]
    for indice in participantes:
        if fitness[indice] > fitness[melhorParticipante]:
            melhorParticipante = indice

    return populacao[melhorParticipante]


#Retorna os melhores individuos da populacao
def selecionarElite(populacao, fitness):
    indicesOrdenados = np.argsort(fitness)[::-1]
    elite = []

    for i in range(qtdElite):
        elite.append(populacao[indicesOrdenados[i]].copy())

    return elite


#Cruzamento entre dois individuos
def crossover(pai1, pai2):
    alfa = np.random.uniform(0, 1, qtGenes)
    filho1 = alfa * pai1 + (1 - alfa) * pai2
    filho2 = alfa * pai2 + (1 - alfa) * pai1
    return filho1, filho2


#Faz a mutação de um individuo
def mutacao(individuo):
    individuo = individuo.copy()
    for i in range(len(individuo)):
        if random.random() < taxaMutacao:
            individuo[i] += np.random.normal(0, 0.1)
    return individuo


if __name__ == "__main__":

    populacao = gerarPopulacao()

    fitness = []

    for individuo in populacao:
        nota = avaliarIndividuo(individuo)
        fitness.append(nota)

    elite = selecionarElite(populacao, fitness)
    selecionado = selecaoTorneio(populacao, fitness)

    print("Melhor fitness:", max(fitness))
    print("Pior fitness:", min(fitness))
    print("Quantidade de individuos na elite:", len(elite))
    print("Genes do individuo selecionado:", len(selecionado))

    pai1 = selecaoTorneio(populacao, fitness)
    pai2 = selecaoTorneio(populacao, fitness)

    filho1, filho2 = crossover(pai1, pai2)

    print("Genes do filho 1:", len(filho1))
    print("Genes do filho 2:", len(filho2))
    print("Valores reais:", np.issubdtype(filho1.dtype, np.floating))

    filhoMutado = mutacao(filho1)

    print("Genes do filho mutado:", len(filhoMutado))
    print("Filho sofreu alteracoes:", not np.array_equal(filho1, filhoMutado))
