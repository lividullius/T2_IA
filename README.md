# T2_IA
Aprendizagem por reforço no jogo da velha: uma rede MLP 9-9-9 cujos pesos são
evoluídos por um algoritmo genético (sem backpropagation), tendo o Minimax
(modos Médio e Difícil) como adversário que treina a rede.

Só usa a biblioteca padrão do Python (3.10+).

## Estrutura

```
jogo.py               regras: tabuleiro (X=1, O=-1, vazio=0), vencedor, empate
minimax.py            Minimax com modos Médio (50%) e Difícil (100%)
config.py             parâmetros da rede, do AG e da aptidão
redeMlp.py            MLP 9-9-9 com bias, 180 pesos, só propagação
aptidao.py            partidas rede x Minimax e função de aptidão
algoritmoGenetico.py  população, elitismo, torneio, crossover, mutação, fases
frontend/
  front.py            front do T1 adaptado, menu com os 3 modos
tests/                testes das etapas 1 a 5 (24 testes)
logs/                 CSV por geração (melhor/média/pior aptidão)
modelos/              pesos do melhor indivíduo (melhor_rede.json)
versaoDiferente/      versão alternativa do colega (referência)
```

## Como rodar

```bash
python3 frontend/front.py                      # menu: 1 humano x Minimax, 2 aprendizagem, 3 humano x rede
python3 -m unittest discover tests             # testes
python3 algoritmoGenetico.py --seed 1          # treino sem interface
```

O treino salva o melhor modelo em `modelos/melhor_rede.json` e o log em
`logs/evolucao.csv`. Opções: `--geracoes N`, `--populacao N`, `--seed S`.

## Como funciona

- **Rede:** 9 entradas (1 = peça da rede, -1 = adversário, 0 = vazio),
  9 ocultos (tanh), 9 saídas (logística). A jogada é a saída mais ativada;
  se a casa estiver ocupada, é jogada inválida.
- **Aptidão por partida:** +10 por jogada válida; no fim, vitória +50,
  empate +30, derrota 0, jogada inválida -20 (encerra a partida).
  - Difícil: 2 partidas (rede começa e Minimax começa). Máximo = 150.
  - Médio: média de 30 partidas.
  - Misto: metade Médio, metade Difícil (cada um dividido pelo seu máximo).
- **AG:** população 100 x 180, elitismo 1, torneio de 2, crossover
  aritmético, mutação de 2% dos genes (troca por valor aleatório em [-1, 1]).
- **Fases:** Médio -> Misto -> Difícil. Muda de fase após 60 gerações sem
  melhora (máx. 200 por fase).
- **Parada:** aptidão 150 no Difícil, 100 gerações sem melhora ou 600 gerações.


