# T2_IA
Aprendizagem por reforço no jogo da velha: uma rede MLP 9-9-9 cujos pesos são
evoluídos por um algoritmo genético (sem backpropagation), tendo o Minimax
(modos Médio e Difícil) como adversário que treina a rede.

Só usa a biblioteca padrão do Python (3.10+).

## Estrutura

```
jogo.py        regras: tabuleiro (X=1, O=-1, vazio=0), vencedor, empate  [pronto]
minimax.py     Minimax com modos Médio (50%) e Difícil (100%)             [pronto]
config.py      parâmetros da rede, do AG e da aptidão                     [pronto]
rede.py        MLP 9-9-9 com bias, 180 pesos, só propagação               [etapa 3]
aptidao.py     partidas rede x Minimax e função de aptidão                [etapa 4]
ag.py          população, elitismo, torneio, crossover real, mutação      [etapa 5]
frontend/
  front.py     front do T1 adaptado, menu com os 3 modos                  [modo 1 pronto]
tests/         testes das etapas (python3 -m unittest discover tests)
logs/          CSV por geração (melhor/média/pior aptidão)
modelos/       pesos do melhor indivíduo (melhor_rede.json)
```

## Como rodar

```bash
python3 frontend/front.py               # menu: 1 humano x Minimax, 2 aprendizagem, 3 humano x rede
python3 -m unittest discover tests      # testes
python3 ag.py                           # treino sem interface (quando a etapa 5 estiver pronta)
```

## O que mudou em relação ao T1

- O tabuleiro do terminal continua o mesmo.
- Saiu a IA que classificava o estado do jogo: agora `jogo.estado()` decide
  com ifs a cada jogada.
- O jogador aleatório virou o Minimax (`minimax.jogada_minimax`), e esse é o
  modo humano x Minimax. A cada nova partida alterna quem começa.
- Os modos 2 (aprendizagem) e 3 (humano x rede) entram em cima dessa base.
