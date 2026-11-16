"""Rede neural MLP 9-9-9 com bias (só propagação).

Cromossomo de 180 pesos:
    0..89    camada oculta, cada neurônio = [bias, w1..w9]
    90..179  camada de saída, cada neurônio = [bias, w1..w9]

Entrada: 1 = peça da rede, -1 = peça do adversário, 0 = vazio.
"""

import json
import math
from pathlib import Path

import config

N_ENTRADAS = config.N_ENTRADAS
N_SAIDAS = config.N_SAIDAS


def _logistica(v):
    if v >= 0:
        return 1.0 / (1.0 + math.exp(-v))
    e = math.exp(v)  # evita overflow com v muito negativo
    return e / (1.0 + e)


ATIVACOES = {
    "tanh": math.tanh,
    "logistica": _logistica,
    "relu": lambda v: v if v > 0 else 0.0,
    "linear": lambda v: v,
}


def n_genes(n_ocultos=config.N_OCULTOS):
    """Quantidade de pesos da rede (180 com 9 ocultos)."""
    return n_ocultos * (N_ENTRADAS + 1) + N_SAIDAS * (n_ocultos + 1)


class Rede:
    def __init__(self, pesos, n_ocultos=config.N_OCULTOS,
                 ativacao_oculta=config.ATIVACAO_OCULTA,
                 ativacao_saida=config.ATIVACAO_SAIDA):
        esperado = n_genes(n_ocultos)
        if len(pesos) != esperado:
            raise ValueError(
                f"esperava {esperado} pesos para {n_ocultos} ocultos, "
                f"recebi {len(pesos)}")
        self.n_ocultos = n_ocultos
        self.ativacao_oculta = ativacao_oculta
        self.ativacao_saida = ativacao_saida
        self._f_oculta = ATIVACOES[ativacao_oculta]
        self._f_saida = ATIVACOES[ativacao_saida]

        # separa o cromossomo nas duas camadas (ideia da versaoDiferente)
        tam_oculto = N_ENTRADAS + 1
        self.oculta = [list(pesos[j * tam_oculto:(j + 1) * tam_oculto])
                       for j in range(n_ocultos)]
        inicio = n_ocultos * tam_oculto
        tam_saida = n_ocultos + 1
        self.saida = [list(pesos[inicio + k * tam_saida:
                                 inicio + (k + 1) * tam_saida])
                      for k in range(N_SAIDAS)]

    @staticmethod
    def _camada(entrada, neuronios, f):
        # v = bias + soma(entrada * peso);  y = f(v)
        saidas = []
        for w in neuronios:
            v = w[0]
            for p, wi in zip(entrada, w[1:]):
                v += p * wi
            saidas.append(f(v))
        return saidas

    def propagar(self, entrada):
        """Calcula a camada oculta e depois a de saída (9 valores)."""
        ocultos = self._camada(entrada, self.oculta, self._f_oculta)
        return self._camada(ocultos, self.saida, self._f_saida)

    def jogada(self, tab, meu_simbolo):
        """Casa com a maior saída. Pode ser casa ocupada (jogada inválida)."""
        entrada = [v * meu_simbolo for v in tab]  # ponto de vista da rede
        saidas = self.propagar(entrada)
        return max(range(N_SAIDAS), key=saidas.__getitem__)


def salvar_pesos(pesos, caminho=config.ARQUIVO_MELHOR_MODELO,
                 n_ocultos=config.N_OCULTOS, **info):
    """Salva os pesos e a topologia em JSON."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    dados = {
        "n_entradas": N_ENTRADAS,
        "n_ocultos": n_ocultos,
        "n_saidas": N_SAIDAS,
        "ativacao_oculta": config.ATIVACAO_OCULTA,
        "ativacao_saida": config.ATIVACAO_SAIDA,
        **info,
        "pesos": list(pesos),
    }
    caminho.write_text(json.dumps(dados, indent=2), encoding="utf-8")


def carregar_pesos(caminho=config.ARQUIVO_MELHOR_MODELO):
    """Lê o JSON salvo."""
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def carregar_rede(caminho=config.ARQUIVO_MELHOR_MODELO):
    """Lê o JSON e já devolve a Rede pronta."""
    dados = carregar_pesos(caminho)
    return Rede(dados["pesos"], dados["n_ocultos"],
                dados["ativacao_oculta"], dados["ativacao_saida"])
