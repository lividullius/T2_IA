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
- **Treino a treino, o resultado varia bastante**, porque a aptidão é
  medida em partidas aleatórias.
