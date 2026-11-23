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
tests/                testes (jogo, Minimax, rede, AG, ia.py)
logs/                 evolucao.csv (melhor/média/pior aptidão por geração)
modelos/              melhor_rede.json (pesos da melhor rede)
```

## Como rodar

Abra o terminal na pasta do projeto (`T2_IA`) e rode:

```bash
python3 frontend/front.py
```

Aparece o menu:

```
1. Humano x Minimax
2. Aprendizagem: rede x Minimax (AG)
3. Humano x Rede treinada
q. Sair
```

### 1. Humano x Minimax
1. Escolha o modo: `1` Médio ou `2` Difícil.
2. Responda se você começa (`s`/`n`). Quem começa joga de X.
3. Na sua vez, digite o número da casa (1 a 9) e Enter:

   ```
    1 | 2 | 3
   ---+---+---
    4 | 5 | 6
   ---+---+---
    7 | 8 | 9
   ```
4. No fim, aparece o placar e a opção de jogar outra partida. `q` sai da partida.

### 2. Aprendizagem (treinar a rede)
1. Se já existir um modelo salvo, pergunta se quer treinar de novo (isso
   sobrescreve `modelos/melhor_rede.json`).
2. Pede população, máximo de gerações e seed. Enter mantém o padrão.
3. **Passo a passo?** Com `s`, para a cada geração:
   Enter = próxima geração, `r` = rodar direto até o fim, `q` = parar.
4. **Mostrar partida do melhor?** Com `s`, desenha a partida da melhor rede
   de cada geração.
5. A cada geração mostra a fase, melhor/média/pior aptidão e a tabela da
   população. No fim, salva o melhor modelo. Ctrl+C também para e salva.

### 3. Humano x Rede treinada
1. Carrega `modelos/melhor_rede.json` (se não existir, oferece treinar).
2. Responda se você começa e jogue digitando as casas, como no modo 1.
3. Se a rede escolher uma casa ocupada, isso conta como erro na acurácia e
   ela joga na melhor casa livre.
4. Mostra o placar e a acurácia da rede (% de jogadas válidas, % de jogadas
   ótimas e vitórias/empates/derrotas).

### Treinar sem o menu

```bash
python3 algoritmoGenetico.py                          # parâmetros do config.py
python3 algoritmoGenetico.py --geracoes 500 --populacao 100 --seed 1
```

Salva o modelo em `modelos/melhor_rede.json` e o log em `logs/evolucao.csv`.

### Testes

```bash
python3 -m unittest discover tests
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

- **Minimax:** o Difícil sempre joga a melhor casa (empates sorteados, para
  as partidas variarem); o Médio joga assim em 50% das vezes e aleatório no resto.
- **Rede:** recebe o tabuleiro (1 = peça dela, −1 = adversário, 0 = vazio) e
  joga na saída mais ativada. Escolher uma casa ocupada é jogada inválida.
- **Aptidão:** média de 20 partidas contra o Minimax (+10 por jogada válida,
  +10 por jogada ótima; vitória +50, empate +30; inválida −20 e fim da partida).
- **AG:** população 200, elitismo 4, torneio de 2, crossover aritmético,
  mutação por troca (2%).
- **Fases (Médio/Difícil):** 70/30 → 50/50 → 30/70.
- **Parada:** convergência (média móvel da melhor aptidão) ou 2000 gerações.

**Resultado:** o modelo salvo não perde em 52% das partidas contra o Difícil
e em 55% contra o Médio.

Detalhes e resultados: [docs/decisoes_treino.md](docs/decisoes_treino.md).
