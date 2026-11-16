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
rede.py        MLP 9-9-9 com bias, 180 pesos, só propagação               [pronto]
aptidao.py     partidas rede x Minimax e função de aptidão                [pronto]
ag.py          população, elitismo, torneio, crossover real, mutação      [pronto]
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
python3 ag.py [--seed 1] [--geracoes N] # treino sem interface (salva modelos/melhor_rede.json)
```

## O que mudou em relação ao T1

- O tabuleiro do terminal continua o mesmo.
- Saiu a IA que classificava o estado do jogo: agora `jogo.estado()` decide
  com ifs a cada jogada.
- O jogador aleatório virou o Minimax (`minimax.jogada_minimax`), e esse é o
  modo humano x Minimax. A cada nova partida alterna quem começa.
- Os modos 2 (aprendizagem) e 3 (humano x rede) entram em cima dessa base.

## Origem do código da rede e do AG

A pasta `versaoDiferente/` tem a versão alternativa (numpy, strings "X"/"O").
Dela vieram para `rede.py` e `ag.py` a montagem/desmontagem do cromossomo, o
torneio e o crossover aritmético por gene. Mudanças ao trazer para cá:
sem máscara de casas ocupadas (jogada inválida é penalizada, como pede o
enunciado), entrada do ponto de vista da rede, uso do `jogo.py`/`minimax.py`
da raiz, mutação trocando o gene por um real aleatório (como na aula) e o loop
de gerações com fases Médio -> Misto -> Difícil.

O modelo salvo em `modelos/melhor_rede.json` foi treinado com `--seed 1` e
empata as 2 partidas contra o Difícil (aptidão 150).
