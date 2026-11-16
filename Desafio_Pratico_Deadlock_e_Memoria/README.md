# Desafio Prático: Deadlock e Gerenciamento de Memória

Simulador em Python feito para o desafio de Sistemas Operacionais I. Ele junta dois assuntos das aulas: deadlock (aula de impasses em Java) e substituição de páginas com FIFO e LRU (Aula 8, gerenciamento de memória).

Não usa nenhuma biblioteca externa, só o Python 3.

## Como executar

```
python simulador.py
```

O menu tem três opções: deadlock, FIFO e LRU, e anomalia de Belady. Para rodar os testes:

```
python testes.py
```

## Arquivos

- `simulador.py`: menu e leitura dos dados digitados
- `deadlock.py`: processos, recursos, simulação e detecção do ciclo
- `memoria.py`: FIFO, LRU, taxas e análise da anomalia de Belady
- `testes.py`: testes com `unittest`

## Deadlock

Cada processo recebe uma lista de recursos e pede um de cada vez, na ordem da lista. Cada recurso tem uma única instância. A simulação anda em rodadas: se o recurso está livre o processo pega, se não está ele espera. Quando um processo consegue todos os recursos ele termina e libera tudo.

Se uma rodada inteira passa sem ninguém conseguir avançar e ainda sobram processos, o programa monta o grafo de espera (cada processo apontando para quem está com o recurso que ele quer) e procura o ciclo seguindo as setas. Os processos do ciclo são os que estão em deadlock. Quem está esperando por alguém do ciclo mas não faz parte dele aparece separado, como bloqueado.

Os cenários prontos:

1. Deadlock simples: P1 pede R1 e depois R2, P2 pede R2 e depois R1. É o mesmo caso do `DeadlockDemo` da aula.
2. Sem deadlock: os dois pedem R1 antes de R2. É a ideia do `OrderedLocksDemo`, ordem global de recursos.
3. Deadlock com três processos, cada um esperando o próximo.
4. Deadlock entre P1 e P2 com o P3 preso esperando por eles.

As quatro condições de Coffman aparecem no modelo: exclusão mútua (um recurso por vez), posse e espera (o processo segura o que já pegou enquanto espera o outro), não preempção (ninguém tira o recurso de um processo) e espera circular (o ciclo do grafo). O cenário 2 funciona porque a ordem global impede a espera circular.

## FIFO e LRU

A memória é uma lista de frames. Para cada acesso o programa mostra a página, a memória depois do acesso, se foi HIT ou PAGE FAULT e, quando houve substituição, qual página saiu. No final mostra page faults, hits, e as taxas de cada um.

A diferença entre os dois está só no HIT:

- FIFO não mexe na lista quando acontece um HIT. Sai sempre quem entrou primeiro.
- LRU tira a página do lugar e coloca no fim da lista a cada HIT, porque ela acabou de ser usada. Sai quem está há mais tempo sem uso.

Em os dois casos a página que sai é a da posição 0 da lista.

## Anomalia de Belady

O programa roda o algoritmo com 1, 2, 3, até o máximo de frames pedido e monta uma tabela de page faults. Se com mais frames o número de faltas for maior do que com menos frames, ele avisa a anomalia e mostra os dois valores.

Com a sequência `1 2 3 4 1 2 5 1 2 3 4 5`:

| Frames | FIFO | LRU |
|--------|------|-----|
| 1 | 12 | 12 |
| 2 | 12 | 12 |
| 3 | 9 | 10 |
| 4 | 10 | 8 |
| 5 | 5 | 5 |
| 6 | 5 | 5 |

No FIFO, passar de 3 para 4 frames aumentou as faltas de 9 para 10, que é a anomalia. No LRU isso não aconteceu: o número só cai ou fica igual.

## Testes e resultados

São 17 testes e todos passam. Os principais:

- FIFO com 3 frames na sequência de Belady: 9 faltas e 3 hits. Com 4 frames: 10 faltas e 2 hits.
- LRU com 3 frames: 10 faltas e 2 hits. Com 4 frames: 8 faltas e 4 hits.
- Sequência `7 0 1 2 0 3 0 4 2 3 0 3 2` com 3 frames: FIFO 10 faltas, LRU 9 faltas (a mesma da aula).
- Sequência `1 2 1 3` com 2 frames: no LRU fica `[1, 3]` e no FIFO fica `[2, 3]`, o que confirma que o HIT muda a ordem só no LRU.
- Com 1 frame, só acerta quando a mesma página se repete em seguida.
- Anomalia detectada no FIFO e não detectada no LRU nem numa sequência comum.
- Deadlock detectado nos cenários 1, 3 e 4, com os processos certos no ciclo, e nenhum deadlock no cenário 2 nem com um processo sozinho.

## Decisões de implementação

Usei listas do Python para a memória porque foi assim que os algoritmos foram feitos na aula, e fica fácil de ver a ordem de chegada ou de uso. `pop(0)` tira o primeiro e `append` coloca no fim.

Para o deadlock, como cada recurso tem uma instância só e cada processo espera por um recurso de cada vez, cada processo aponta para no máximo um outro. Por isso bastou seguir as setas para achar o ciclo, sem precisar de um algoritmo mais pesado de grafos.

Os algoritmos devolvem os passos em vez de imprimir direto. Assim a mesma função serve para mostrar a execução, para os testes e para a comparação de frames.
