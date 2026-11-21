"""Front end do T2 (terminal).

Modos:
    1. Humano x Minimax
    2. Aprendizagem (rede x Minimax, AG passo a passo)
    3. Humano x Rede treinada (com acurácia)

Rodar da pasta do projeto:  python3 frontend/front.py
"""

import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

import ia  # noqa: E402
from aptidao import jogar_partida  # noqa: E402
from jogo import O, TEM_JOGO, X, estado, simbolo  # noqa: E402
from redeMlp import Rede  # noqa: E402

NOME_MODO = {
    ia.MEDIO: "Médio (50% Minimax)",
    ia.DIFICIL: "Difícil (100% Minimax)",
}
TOP_POPULACAO = 10
NOME_RESULTADO = {
    "vitoria": "vitória da rede",
    "empate": "empate",
    "derrota": "vitória do Minimax",
    "invalida": "jogada inválida da rede",
}


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


def pedir_inteiro(texto, minimo, maximo, padrao):
    while True:
        bruto = input(f"  {texto} [{padrao}]: ").strip()
        if not bruto:
            return padrao
        if bruto.isdigit():
            valor = int(bruto)
            if minimo <= valor <= maximo:
                return valor
        print(f"  Digite um inteiro entre {minimo} e {maximo}.")


def marca(tab, indice):
    return simbolo(tab[indice]) if tab[indice] else str(indice + 1)


def placar(v, e, d, quem="você"):
    total = v + e + d
    if total == 0:
        return f"Placar ({quem}): nenhuma partida ainda."
    return (f"Placar ({quem}): {v} vitória(s), {e} empate(s), "
            f"{d} derrota(s).")


def texto_acuracia(resumo):
    return (
        f"Acurácia da rede: {resumo['pct_validas']:.1f}% válidas "
        f"({resumo['validas']}/{resumo['jogadas']}), "
        f"{resumo['pct_otimas']:.1f}% ótimas "
        f"({resumo['otimas']}/{resumo['jogadas']})."
    )


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
    if texto_placar:
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
        if not ia.jogada_valida(tab, casa):
            print("  Essa casa já está ocupada.")
            continue
        return casa


def partida_humano_minimax(modo, humano_comeca, pontos, rng):
    tab = ia.novo_tabuleiro()
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
            casa = ia.jogada_minimax(tab, maquina, modo, rng)
            texto = f"Minimax jogou na casa {casa + 1}."
        tab[casa] = vez
        vez = -vez
        if vez == humano or estado(tab) != TEM_JOGO:
            desenhar(tab, cabecalho, [texto], placar(*pontos))

    resultado = ia.resultado_para(tab, humano)
    print(f"  Fim de jogo: {estado(tab)}.")
    return resultado


def modo_humano_minimax():
    print()
    print("  Modo do Minimax")
    print("  1. Médio (50% Minimax, 50% aleatório)")
    print("  2. Difícil (sempre Minimax)")
    modo = ia.MEDIO if perguntar("Modo (1-2):", ["1", "2"]) == "1" else ia.DIFICIL

    rng = random.Random()
    pontos = [0, 0, 0]
    indice = {"vitoria": 0, "empate": 1, "derrota": 2}

    while True:
        humano_comeca = perguntar("Você começa? (s/n):", ["s", "n"]) == "s"
        resultado = partida_humano_minimax(modo, humano_comeca, pontos, rng)
        if resultado is None:
            break
        pontos[indice[resultado]] += 1
        print(f"  {placar(*pontos)}")
        if perguntar("Outra partida? (s/n):", ["s", "n"]) != "s":
            break
    print()
    print(f"  {placar(*pontos)}")


def mostrar_tabela_populacao(aptidoes, indice_melhor, top=TOP_POPULACAO):
    ordem = sorted(range(len(aptidoes)), key=aptidoes.__getitem__, reverse=True)
    print(f"  Top {min(top, len(ordem))} da população:")
    print("    pos  #    aptidão")
    for pos, i in enumerate(ordem[:top], start=1):
        marca_melhor = " *" if i == indice_melhor else ""
        print(f"    {pos:3d}  {i:3d}  {aptidoes[i]:8.2f}{marca_melhor}")


def mostrar_partida_melhor(info):
    pesos = info["populacao"][info["indice_melhor"]]
    rede = Rede(pesos)
    partida = jogar_partida(rede, ia.DIFICIL, True, random.Random(info["geracao"]))
    tab_final = (list(partida["historico"][-1]["tabuleiro"])
                 if partida["historico"] else ia.novo_tabuleiro())
    cabecalho = [
        f"Partida do melhor (geração {info['geracao']})",
        f"Rede é {simbolo(partida['simbolo_rede'])}     "
        f"Minimax é {simbolo(-partida['simbolo_rede'])}",
    ]
    feedback = [
        f"Resultado: {NOME_RESULTADO.get(partida['resultado'], partida['resultado'])}.",
        f"Pontos da partida: {partida['pontos']:.0f} "
        f"(válidas {partida['jogadas_validas']}, "
        f"ótimas {partida['jogadas_otimas']}, "
        f"inválidas {partida['jogadas_invalidas']}).",
    ]
    desenhar(tab_final, cabecalho, feedback, "")


def modo_aprendizagem():
    print()
    print("  Aprendizagem: AG evoluindo a rede contra o Minimax")
    if ia.modelo_existe():
        print("  Já existe um modelo em modelos/melhor_rede.json.")
        if perguntar("Treinar de novo e sobrescrever? (s/n):", ["s", "n"]) != "s":
            return

    print()
    print("  Parâmetros (Enter mantém o padrão)")
    populacao = pedir_inteiro(
        "Tamanho da população", 4, 500, ia.config.TAMANHO_POPULACAO)
    geracoes = pedir_inteiro(
        "Máximo de gerações", 1, 5000, ia.config.MAX_GERACOES)
    seed = pedir_inteiro("Seed", 0, 2**31 - 1, ia.config.SEED)
    passo = perguntar("Passo a passo? (s/n):", ["s", "n"]) == "s"
    mostrar_partida = perguntar(
        "Mostrar partida do melhor a cada geração? (s/n):", ["s", "n"]) == "s"

    estado_ui = {"correndo": not passo}

    def ao_fim_da_geracao(info):
        print()
        print(f"  Geração {info['geracao']}  [{info['fase']}]  "
              f"sem melhora: {info['sem_melhora']}")
        print(f"  melhor {info['melhor']:.2f}  "
              f"média {info['media']:.2f}  "
              f"pior {info['pior']:.2f}")
        mostrar_tabela_populacao(info["aptidoes"], info["indice_melhor"])
        if mostrar_partida:
            mostrar_partida_melhor(info)

        if estado_ui["correndo"]:
            return True

        while True:
            cmd = input(
                "  Enter = próxima geração | r = rodar direto | q = parar: "
            ).strip().lower()
            if cmd == "":
                return True
            if cmd == "r":
                estado_ui["correndo"] = True
                return True
            if cmd == "q":
                return False
            print("  Use Enter, r ou q.")

    print()
    print("  Treinando... (Ctrl+C salva o melhor até agora e para)")
    fim = ia.treinar(
        ao_fim_da_geracao=ao_fim_da_geracao,
        populacao=populacao,
        geracoes=geracoes,
        seed=seed,
    )
    print()
    print(f"  Parou na geração {fim['geracao']} ({fim['motivo']}), "
          f"fase {fim['fase']}, melhor aptidão {fim['aptidao']:.2f}.")
    print(f"  Modelo salvo em {ia.config.ARQUIVO_MELHOR_MODELO}")


def partida_humano_rede(humano_comeca, pontos, acc):
    tab = ia.novo_tabuleiro()
    humano = X if humano_comeca else O
    rede_simbolo = -humano
    cabecalho = [
        f"Você é {simbolo(humano)}     Rede é {simbolo(rede_simbolo)}",
    ]
    vez = X
    feedback = ["Você começa. Escolha uma casa." if humano_comeca
                else "A rede começa."]
    desenhar(tab, cabecalho, feedback,
             placar(*pontos) + "  " + texto_acuracia(acc.resumo()))

    while estado(tab) == TEM_JOGO:
        if vez == humano:
            casa = pedir_casa(tab)
            if casa is None:
                return None
            texto = f"Você jogou na casa {casa + 1}."
        else:
            jogada = ia.jogada_rede(tab, rede_simbolo)
            acc.registrar_jogada(tab, rede_simbolo, jogada["escolhida"])
            casa = jogada["casa"]
            if jogada["valida"]:
                texto = f"Rede jogou na casa {casa + 1}."
            else:
                texto = (f"Rede escolheu a casa {jogada['escolhida'] + 1} "
                         f"(ocupada); jogou em {casa + 1}.")
        tab[casa] = vez
        vez = -vez
        if vez == humano or estado(tab) != TEM_JOGO:
            desenhar(tab, cabecalho, [texto],
                     placar(*pontos) + "  " + texto_acuracia(acc.resumo()))

    resultado_humano = ia.resultado_para(tab, humano)
    resultado_rede = ia.resultado_para(tab, rede_simbolo)
    acc.registrar_resultado(resultado_rede)
    print(f"  Fim de jogo: {estado(tab)}.")
    print(f"  {texto_acuracia(acc.resumo())}")
    return resultado_humano


def modo_humano_rede():
    print()
    if not ia.modelo_existe():
        print("  Nenhum modelo treinado em modelos/melhor_rede.json.")
        if perguntar("Treinar agora? (s/n):", ["s", "n"]) != "s":
            return
        modo_aprendizagem()
        if not ia.modelo_existe():
            print("  Treino não gerou modelo; voltando ao menu.")
            return
    else:
        ia.carregar_modelo(recarregar=True)

    pontos = [0, 0, 0]
    acc = ia.Acuracia()
    indice = {"vitoria": 0, "empate": 1, "derrota": 2}

    while True:
        humano_comeca = perguntar("Você começa? (s/n):", ["s", "n"]) == "s"
        resultado = partida_humano_rede(humano_comeca, pontos, acc)
        if resultado is None:
            break
        pontos[indice[resultado]] += 1
        print(f"  {placar(*pontos)}")
        if perguntar("Outra partida? (s/n):", ["s", "n"]) != "s":
            break

    resumo = acc.resumo()
    print()
    print(f"  {placar(*pontos)}")
    print(f"  {texto_acuracia(resumo)}")
    if resumo["partidas"]:
        print(f"  Rede: {resumo['vitoria']} vitória(s), "
              f"{resumo['empate']} empate(s), "
              f"{resumo['derrota']} derrota(s) "
              f"({resumo['pct_sem_derrota']:.1f}% sem derrota).")


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
