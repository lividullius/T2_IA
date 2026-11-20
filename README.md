# T2_IA
Jogo da velha com aprendizagem por reforço: um algoritmo genético evolui os
pesos de uma rede MLP (sem backpropagation), e o Minimax é o adversário que
treina a rede. Só usa a biblioteca padrão do Python (3.10+).

## Arquivos

```
jogo.py               regras do jogo (X=1, O=-1, vazio=0)
minimax.py            Minimax nos modos Médio (50%) e Difícil (100%)
redeMlp.py            rede MLP 9-9-9 (só propagação)
aptidao.py            partidas rede x Minimax e cálculo da aptidão
algoritmoGenetico.py  ciclo do AG (elitismo, torneio, crossover, mutação)
config.py             todos os parâmetros
ia.py                 funções prontas para o front
frontend/front.py     menu com os 3 modos
docs/                 decisões de treino e variantes testadas
```

## Como rodar

```bash
python3 frontend/front.py             # menu
python3 algoritmoGenetico.py          # treina e salva modelos/melhor_rede.json
python3 -m unittest discover tests    # testes
```

## Uso no front (`ia.py`)

```python
import ia
if not ia.modelo_existe():
    ia.treinar()                       # só treina se não houver modelo salvo
j = ia.jogada_rede(tab, ia.X)          # j["casa"] = onde jogar, j["valida"] = acertou?
ia.jogada_minimax(tab, ia.O, ia.MEDIO)
ia.estado_jogo(tab)                    # "Tem jogo", "X venceu", "O venceu", "Empate"
acc = ia.Acuracia()                    # registrar_jogada / registrar_resultado / resumo
```

## Como funciona

- **Rede:** recebe o tabuleiro (1 = peça dela, −1 = adversário, 0 = vazio) e
  joga na saída mais ativada. Escolher uma casa ocupada é jogada inválida.
- **Aptidão:** média de 20 partidas contra o Minimax (+10 por jogada válida,
  +10 por jogada ótima; vitória +50, empate +30; inválida −20 e fim da partida).
- **AG:** população 200, elitismo 4, torneio de 2, crossover aritmético,
  mutação por troca (2%).
- **Fases (Médio/Difícil):** 70/30 → 50/50 → 30/70.
- **Parada:** convergência (média móvel da melhor aptidão) ou 2000 gerações.

Detalhes e resultados: [docs/decisoes_treino.md](docs/decisoes_treino.md).
