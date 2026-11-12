"""Front end do T2 (terminal), reaproveitado do T1.

O tabuleiro do T1 continua. Saiu a IA que classificava o estado do jogo
(agora jogo.estado() decide com ifs) e o jogador aleatório virou o Minimax.

Modos:
    1. Humano x Minimax       (pronto)
    2. Aprendizagem (rede x Minimax, AG passo a passo)   (etapa 6)
    3. Humano x Rede treinada (com acurácia)             (etapa 6)

Rodar da pasta do projeto:  python3 frontend/front.py
"""

import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from jogo import (  # noqa: E402
    EMPATE, O, TEM_JOGO, X, estado, jogada_valida, novo_tabuleiro, simbolo,
)
from minimax import DIFICIL, MEDIO, jogada_minimax  # noqa: E402

NOME_MODO = {MEDIO: "Médio (50% Minimax)", DIFICIL: "Difícil (100% Minimax)"}


def configurar_terminal():
    for fluxo in (sys.stdout, sys.stdin):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8", errors="replace")


def perguntar(texto, opcoes):
    while True:
        resposta = input(f"  {texto} ").strip().lower()
        if resposta in opcoes:
            return resposta
        print(f"  Escolha uma destas opções: {', '.join(opcoes)}.")


# ---------------------------------------------------------------- desenho

def marca(tab, indice):
    return simbolo(tab[indice]) if tab[indice] else str(indice + 1)


def placar(v, e, d):
    total = v + e + d
    if total == 0:
        return "Placar: nenhuma partida ainda."
    return f"Placar (você): {v} vitória(s), {e} empate(s), {d} derrota(s)."


def desenhar(tab, cabecalho, feedback, texto_placar):
    casas = [marca(tab, i) for i in range(9)]
    print()
    print("  Jogo da velha")
    for linha in cabecalho:
        print(f"  {linha}")
    print()
    for inicio in (0, 3, 6):
        a, b, c = casas[inicio:inicio + 3]
        print(f"   {a} | {b} | {c} ")
        if inicio < 6:
            print("  ---+---+---")
    print()
    for linha in feedback:
        print(f"  {linha}")
    print(f"  {texto_placar}")
    print()


def pedir_casa(tab):
    while True:
        texto = input("  Casa (1-9) ou q para sair: ").strip().lower()
        if texto == "q":
            return None
        if texto not in list("123456789"):
            print("  Escolha um número de 1 a 9.")
            continue
        casa = int(texto) - 1
        if not jogada_valida(tab, casa):
            print("  Essa casa já está ocupada.")
            continue
        return casa


# ------------------------------------------------------ humano x minimax

def partida_humano_minimax(modo, humano_comeca, pontos, rng):
    """Quem começa joga de X. Retorna o resultado do ponto de vista do
    humano ("vitoria", "empate", "derrota") ou None se saiu."""
    tab = novo_tabuleiro()
    humano = X if humano_comeca else O
    maquina = -humano
    cabecalho = [
        f"Você é {simbolo(humano)}     Minimax é {simbolo(maquina)}",
        f"Modo: {NOME_MODO[modo]}",
    ]
    vez = X
    feedback = ["Você começa. Escolha uma casa." if humano_comeca
                else "O Minimax começa."]
    desenhar(tab, cabecalho, feedback, placar(*pontos))

    while estado(tab) == TEM_JOGO:
        if vez == humano:
            casa = pedir_casa(tab)
            if casa is None:
                return None
            texto = f"Você jogou na casa {casa + 1}."
        else:
            casa = jogada_minimax(tab, maquina, modo, rng)
            texto = f"Minimax jogou na casa {casa + 1}."
        tab[casa] = vez
        vez = -vez
        if vez == humano or estado(tab) != TEM_JOGO:
            desenhar(tab, cabecalho, [texto], placar(*pontos))

    final = estado(tab)
    if final == EMPATE:
        resultado = "empate"
    elif (final == "X venceu") == (humano == X):
        resultado = "vitoria"
    else:
        resultado = "derrota"
    print(f"  Fim de jogo: {final}.")
    return resultado


def modo_humano_minimax():
    print()
    print("  Modo do Minimax")
    print("  1. Médio (50% Minimax, 50% aleatório)")
    print("  2. Difícil (sempre Minimax)")
    modo = MEDIO if perguntar("Modo (1-2):", ["1", "2"]) == "1" else DIFICIL

    rng = random.Random()
    pontos = [0, 0, 0]  # vitórias, empates, derrotas do humano
    humano_comeca = perguntar("Você começa? (s/n):", ["s", "n"]) == "s"
    indice = {"vitoria": 0, "empate": 1, "derrota": 2}

    while True:
        resultado = partida_humano_minimax(modo, humano_comeca, pontos, rng)
        if resultado is None:
            break
        pontos[indice[resultado]] += 1
        print(f"  {placar(*pontos)}")
        if perguntar("Outra partida? (s/n):", ["s", "n"]) != "s":
            break
        humano_comeca = not humano_comeca  # alterna quem começa
    print()
    print(f"  {placar(*pontos)}")


# ------------------------------------------------- modos ainda a fazer

def modo_aprendizagem():
    # TODO (etapa 6): chamar ag.treinar(ao_fim_da_geracao=...) mostrando
    # geração, fase, tabela da população, partida do melhor; Enter = próximo
    # passo, "r" = rodar direto.
    print("\n  Modo aprendizagem ainda não implementado (etapas 3-6).")


def modo_humano_rede():
    # TODO (etapa 6): carregar modelos/melhor_rede.json, jogar contra a rede
    # e mostrar a acurácia (% de jogadas válidas + placar).
    print("\n  Modo humano x rede ainda não implementado (etapas 3-6).")


MENU = (
    ("1", "Humano x Minimax", modo_humano_minimax),
    ("2", "Aprendizagem: rede x Minimax (AG)", modo_aprendizagem),
    ("3", "Humano x Rede treinada", modo_humano_rede),
)


def main():
    configurar_terminal()
    while True:
        print()
        print("  T2 - Jogo da velha: RN + AG + Minimax")
        for chave, nome, _ in MENU:
            print(f"  {chave}. {nome}")
        print("  q. Sair")
        escolha = perguntar("Opção:", [m[0] for m in MENU] + ["q"])
        if escolha == "q":
            break
        dict((c, f) for c, _, f in MENU)[escolha]()


if __name__ == "__main__":
    main()
