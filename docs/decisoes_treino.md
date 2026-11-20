# Decisões de treino

## Problema
O Minimax sempre escolhia a mesma casa nos empates, então o Difícil jogava
sempre a mesma partida. No fim do treino, a rede só via 2 partidas e as
decorou. Contra o Minimax do treino, empatava 100%; contra um adversário
que varia, perdia 70%.

## O que mudamos
1. **Desempate aleatório no Minimax:** entre casas igualmente boas, sorteia
   uma. Continua sendo Minimax: toda jogada escolhida é ótima.
2. **Partidas variadas até o fim:** as fases vão de 70% Médio / 30% Difícil
   para 50/50 e depois 30/70.
3. **Aptidão:** média de 20 partidas por geração, alternando quem começa.
   Por partida: +10 por jogada válida, +10 por jogada ótima segundo o
   Minimax, vitória +50, empate +30. Jogada inválida vale −20 e encerra a
   partida.
4. **Parâmetros:** população 200, elitismo 4, até 2000 gerações.
5. **Parada:** limite de gerações ou convergência, quando a média móvel
   (10 gerações) da melhor aptidão passa 300 gerações sem melhorar.
6. **Acurácia:** % de jogadas válidas, % de jogadas ótimas e
   vitórias/empates/derrotas.

Topologia (9-9-9), pesos em [−1, 1], mutação por troca e torneio de 2
continuam como na aula.

## Resultado
O modelo escolhido (FIEL_EB) não perde em 52% das partidas contra o
Difícil, e em 55% contra o Médio. Testamos também rede maior, mutação
gaussiana e outras variações, e não fez muita diferença. Os números estão
em [variantes.md](variantes.md).

## Para as considerações finais
- **Positivo:** achamos e corrigimos o sobreajuste sem alterar o Minimax e
  sem sair do que foi visto em aula.
- **Negativo:** sem backpropagation, o AG aprende devagar, e a rede ainda
  perde para o Difícil em quase metade das partidas.
