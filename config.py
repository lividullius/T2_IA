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
TAMANHO_POPULACAO = 100   # N
ELITISMO = 1
TAMANHO_TORNEIO = 2
TAXA_MUTACAO = 0.02       # fração dos genes da população por geração
CROSSOVER = "aritmetico" 
BLX_ALFA = 0.5
MAX_GERACOES = 600
PACIENCIA = 100           # gerações sem melhora na última fase -> convergência
PACIENCIA_FASE = 60       # gerações sem melhora -> passa para a próxima fase
MAX_GERACOES_FASE = 200   # limite de gerações nas fases Médio e Misto

# Aptidão
PONTOS_JOGADA_VALIDA = 10
BONUS_VITORIA = 50
BONUS_EMPATE = 30
BONUS_DERROTA = 0
PENALIDADE_INVALIDA = -20
PARTIDAS_MEDIO = 30       # K partidas no modo Médio (média)
APTIDAO_IDEAL_DIFICIL = 150  # empatar as 2 partidas contra o Difícil
APTIDAO_MAX_PARTIDA = 100    # melhor partida possível (5 jogadas + vitória),
                             # usado para normalizar o Médio na fase Mista

# Arquivos 
RAIZ = Path(__file__).resolve().parent
PASTA_LOGS = str(RAIZ / "logs")
PASTA_MODELOS = str(RAIZ / "modelos")
ARQUIVO_LOG = str(RAIZ / "logs" / "evolucao.csv")
ARQUIVO_MELHOR_MODELO = str(RAIZ / "modelos" / "melhor_rede.json")
