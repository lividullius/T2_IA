"""Parâmetros do T2 (valores iniciais do plano"""

from pathlib import Path

SEED = 42

# Rede neural (MLP 9-9-9 com bias)
N_ENTRADAS = 9
N_OCULTOS = 9          # configurável para testar outras topologias
N_SAIDAS = 9
N_PESOS = N_OCULTOS * (N_ENTRADAS + 1) + N_SAIDAS * (N_OCULTOS + 1)  # 180
ATIVACAO_OCULTA = "tanh"        # "tanh", "logistica", "relu" ou "linear"
ATIVACAO_SAIDA = "logistica"
PESO_MIN, PESO_MAX = -1.0, 1.0

# Algoritmo genético
TAMANHO_POPULACAO = 200   # N
ELITISMO = 4
TAMANHO_TORNEIO = 2
TAXA_MUTACAO = 0.02       # fração dos genes da população por geração
CROSSOVER = "aritmetico" 
BLX_ALFA = 0.5
MAX_GERACOES = 2000
PACIENCIA = 300           # gerações sem melhora na última fase -> convergência
JANELA_CONVERGENCIA = 10  # média móvel da melhor aptidão (aptidão é ruidosa)
PACIENCIA_FASE = 150      # gerações sem melhora -> passa para a próxima fase
MAX_GERACOES_FASE = 400   # limite de gerações em cada fase, menos a última

# Aptidão
PONTOS_JOGADA_VALIDA = 10
BONUS_VITORIA = 50
BONUS_EMPATE = 30
BONUS_DERROTA = 0
PENALIDADE_INVALIDA = -20
PONTOS_JOGADA_OTIMA = 10     # bônus por jogada ótima segundo o Minimax
INVALIDA_ENCERRA = True      # jogada inválida encerra a partida?
PARTIDAS_POR_AVALIACAO = 20  # partidas de cada rede por geração (Médio + Difícil)

# Fases do treino: fração das partidas contra o Médio (o resto é Difícil).
# Começa 70% Médio / 30% Difícil e termina 30% Médio / 70% Difícil.
FASES = (0.7, 0.5, 0.3)

# Arquivos 
RAIZ = Path(__file__).resolve().parent
PASTA_LOGS = str(RAIZ / "logs")
PASTA_MODELOS = str(RAIZ / "modelos")
ARQUIVO_LOG = str(RAIZ / "logs" / "evolucao.csv")
ARQUIVO_MELHOR_MODELO = str(RAIZ / "modelos" / "melhor_rede.json")
