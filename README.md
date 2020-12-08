# NotPacMan

**Número da Lista**: 6<br>
**Conteúdo da Disciplina**: Final<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 17/0129411  |  Guilherme Mendes Pereira |
| 17/0163571  |  Murilo Loiola Dantas |

## Sobre 
NotPacMan é um jogo multiplayer local competitivo inspirado no jogo PacMan. No NotPacMan, dois jogadores se encontram dentro de um labirinto. Existem duas condições de vitória: comer o jogador adversário ou entregar o valor necessário no depósito. Para cumprir qualquer uma das condições, é necessário acumular pontos comendo as frutas que aparecem pelo labirinto.

O projeto utiliza os algoritmos Dijkstra, Par de Pontos Mais Próximos e Knapsack. 
* O Dijkstra é utilizado para assegurar uma distância mínima entre os pontos inciais (jogador1, jogador2 e saída).
* O Par de Pontos Mais Próximos é utilizado para detectar colisão entre os jogadores e as frutas.
* O Knapsack é utilizado para otimizar a combinação de frutas que são guardadas no inventário de cada jogador. Caso o jogador colida com uma fruta, o Knapsack irá decidir se vale ou não a pena descartar uma ou mais frutas que o jogador possui para pegar a nova fruta, sempre maximizando o valor.

## Screenshots
Adicione 3 ou mais screenshots do projeto em funcionamento.

## Instalação 
**Linguagem**: Python<br>
**Pré-requisitos**: [Python](https://www.python.org/downloads/), [pygame](https://www.pygame.org/wiki/GettingStarted) e [pip](https://packaging.python.org/tutorials/installing-packages/).<br>
**Execução do projeto** <br>

* Clone o repositório:
```bash
git clone https://github.com/projeto-de-algoritmos/Final_NotPacMan.git
```
* Acesse o repositório e instale as bibliotecas necessárias:
```bash
cd Final_NotPacMan/
pip3 install -r requirements.txt
```
* Execute o NotPacMan e divirta-se:
```bash
python3 src/game.py
```

## Uso 

### Vídeo explicativo
[Video](https://github.com/projeto-de-algoritmos/Final_NotPacMan/blob/master/video_explicativo.mp4)

* Jogador1 - pacman amarelo.
* Jogador2 - pacman azul.
* Depósito - baú.

* Clique com o botão esquerdo do mouse em *Start*
* Controle o jogador1 com as teclas ←, ↑, →,  ↓ do teclado.
* Controle o jogador2 com as teclas W, S, A, D do teclado.
* Pegue as frutas passando por elas.
* Deposite suas frutas passand pelo depósito.
* Clique em *Restart* para jogar novamente.
* Clique em *Quit* para encerrar o jogo.

## Outros 
**Importante**: para comer o jogador adversário, é necessário ter mais pontos em si (não no depósito) do que o jogador adversário.



