# Variantes treinadas

Avaliação: 400 partidas contra cada modo (Minimax com desempate aleatório),
alternando quem começa.
**Válidas** = % de jogadas em casa livre · **Ótimas** = % de jogadas que mantêm
o melhor resultado possível · **Não perde** = % de vitórias + empates.

## Variantes fiéis ao enunciado e à aula

Rede 9-9-9, pesos em [−1, 1], mutação por troca, torneio de 2 e parada por
gerações e por convergência. Todas usam população 200 e elitismo 4.

| Variante | Aptidão | Médio: válidas / ótimas / não perde | Difícil: válidas / ótimas / não perde |
|---|---|---|---|
| Antigo | modelo anterior (Minimax fixo, população 100) | 51% / 44% / 45% | 62% / 59% / 30% |
| base | regras do plano, população 100, elitismo 1 | 67% / 40% / 16% | 86% / 53% / 1% |
| FIEL_E | inválida encerra a partida | 70% / 46% / 23% | 92% / 64% / 2% |
| FIEL_C | inválida só penaliza, a partida continua | 61% / 52% / 57% | 67% / 59% / 50% |
| FIEL_CB | FIEL_C + bônus de +10 por jogada ótima | 70% / 50% / 44% | 78% / 68% / 55% |
| **FIEL_EB (escolhida)** | inválida encerra + bônus de +10 por jogada ótima | **76% / 61% / 55%** | **90% / 81% / 52%** |

## Experimentos com a configuração escolhida

Cada experimento muda **uma coisa** na FIEL_EB e roda com 2 seeds (42 e 1).
Os números são **% de partidas sem derrota**, no formato seed 42 / seed 1.

| Experimento | Contra o Difícil | Contra o Médio | Conclusão |
|---|---|---|---|
| FIEL_EB (referência) | 52% / 50% | 55% / 38% | — |
| Sem fases (só 30/70 desde o início) | 55% / 52% | 41% / 39% | fases quase não mudam o resultado |
| População 100 (em vez de 200) | 51% / 50% | 37% / 35% | parecido, um pouco pior no Médio; treina 35% mais rápido |
| Mutação 1% (em vez de 2%) | 51% / **0%** | 44% / 34% | instável: falhou em uma seed |
| Mutação 5% (em vez de 2%) | **1%** / 50% | 31% / 38% | instável: falhou em uma seed |
| Oculta logística (em vez de tanh) | 14% / 19% | 40% / 38% | **tanh é bem melhor** (entradas em [−1, 1]) |

**Dependência da seed** (FIEL_EB, seeds 42 / 1 / 2 / 3):

| | Seed 42 | Seed 1 | Seed 2 | Seed 3 |
|---|---|---|---|---|
| Contra o Difícil | 52% | 50% | 51% | 30% |
| Contra o Médio | 55% | 38% | 39% | 48% |

3 das 4 seeds chegam a cerca de 50% contra o Difícil. No treino antigo, a
seed 42 parava cedo ("para em 100"), enquanto outras seeds chegavam a 150.

**Por que cerca de 50% contra o Difícil?** Separando por quem começa
(modelo escolhido, 200 partidas de cada):

| | Rede começa | Minimax começa |
|---|---|---|
| Difícil (V / E / D) | 0 / 200 / 0 | 0 / 12 / 188 |
| Médio (V / E / D) | 107 / 54 / 39 | 32 / 19 / 149 |

A rede aprendeu a jogar começando (empata sempre com o Difícil), mas
jogando em segundo ela ainda perde quase sempre.

## Outras que testamos (fogem do que foi visto em aula)

Mudam pelo menos uma destas coisas: 27 ou 18 neurônios ocultos, mutação
gaussiana, pesos em [−3, 3], torneio de 3, ou treino sem parada por
convergência.

| Variante | O que muda | Médio: não perde | Difícil: válidas / ótimas / não perde |
|---|---|---|---|
| ocultos27 | 27 ocultos | 24% | 77% / 46% / 0% |
| gauss | mutação gaussiana | 25% | 85% / 61% / 9% |
| g27 / g27p3 | 27 ocultos + gaussiana (+ pesos [−3, 3]) | 45% / 31% | 92% / 58% / 0% |
| A | 27 ocultos, gaussiana, [−3, 3], torneio 3 | 61% | 94% / 84% / 52% |
| B / C / D | A com outros parâmetros | 30–40% | 88–92% / 56–59% / 0–1% |
| E / F | A + mudanças na aptidão | 48% / 65% | 100% / 60% / 0% · 89% / 80% / 55% |
| G / H | E / F com 9 ocultos | 60% / 49% | 84% / 73% / 53% · 96% / 67% / 2% |
| LONGO | F sem parada por convergência (2000 ger.) | 71% | 91% / 82% / 59% |

## Conclusão

- **Fugir da aula não fez muita diferença.** Contra o Difícil, a melhor
  variante fiel (FIEL_EB) não perde em 52% das partidas; a melhor de todas
  (LONGO), em 59%. Contra o Médio, a diferença é maior (55% contra 71%),
  mas exige topologia, mutação e parada diferentes das pedidas.
- **O que fez diferença:** população maior com elitismo 4, o bônus por
  jogada ótima (o Minimax "ensinando" a cada jogada) e a parada por
  convergência usando média móvel.
- **Treino a treino, o resultado varia**, porque a aptidão é medida em
  partidas aleatórias. Mesmo assim, 3 de 4 seeds chegam ao mesmo nível.
- **Fases, população e ativação:** com ou sem fases dá quase no mesmo;
  população 100 fica perto da 200; tanh é bem melhor que logística na
  camada oculta; mutação de 2% é a mais estável.
- **Ponto fraco que sobra:** jogar em segundo.
