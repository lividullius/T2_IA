"""Parâmetros do T2 (valores iniciais do plano; ajustar e registrar no ppt)."""

SEED = 42

# Rede neural (MLP 9-9-9 com bias)
N_ENTRADAS = 9
N_OCULTOS = 9          # configurável para testar outras topologias
N_SAIDAS = 9
N_PESOS = N_OCULTOS * (N_ENTRADAS + 1) + N_SAIDAS * (N_OCULTOS + 1)  # 180
ATIVACAO_OCULTA = "tanh"
ATIVACAO_SAIDA = "logistica"
PESO_MIN, PESO_MAX = -1.0, 1.0

# Algoritmo genético
TAMANHO_POPULACAO = 100   # N
ELITISMO = 1
TAMANHO_TORNEIO = 2
TAXA_MUTACAO = 0.02       # fração dos genes da população por geração
CROSSOVER = "blx"         # "aritmetico" ou "blx" (conferir o indicado no Moodle)
BLX_ALFA = 0.5
MAX_GERACOES = 300
PACIENCIA = 30            # gerações sem melhora -> convergência

# Aptidão
PONTOS_JOGADA_VALIDA = 10
BONUS_VITORIA = 50
BONUS_EMPATE = 30
BONUS_DERROTA = 0
PENALIDADE_INVALIDA = -20
PARTIDAS_MEDIO = 30       # K partidas no modo Médio (média)
APTIDAO_IDEAL_DIFICIL = 150  # empatar as 2 partidas contra o Difícil

# Arquivos
PASTA_LOGS = "logs"
PASTA_MODELOS = "modelos"
ARQUIVO_MELHOR_MODELO = "modelos/melhor_rede.json"
