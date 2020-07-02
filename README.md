<!-- # AZUL
This repository contains a framework to support policy learning for the boardgame AZUL, published by Plan B Games. The purpose of this framework is to allow students to implement algorithms for learning AI players for the game and evaluate the performance of these players against human/other AI players. 

Students making use of the framework will need to create a Player subclass for their AI player that selects moves on the basis of a learned policy, and write code to learn their policy on the basis of repeated simulations of the game.

Some information about the game:
- https://en.wikipedia.org/wiki/Azul_(board_game)
- https://www.ultraboardgames.com/azul/game-rules.php
- https://boardgamegeek.com/boardgame/230802/azul
- https://www.planbgames.com/en/news/azul-c16.html -->

# MCTS Agent

This repository contains a working agent in 1v1 Azul game under the dir ```players/myPlayer.py```. The agent implements ```Monte Carlo Tree Search Algorithm``` with improvements to derive the best move based on a given game state. The agent beats the baseline agents namely ```players/naive_player.py``` and ```players/random_player.py```. 

**Challenges of MCTS agent designing and improvements**
- Random roll-out
Usually the roll-out policy in MCTS is randomly selecting a move. The downside is that it might derive an inaccurate result that leads to the wrong estimation of the value of a move. To improve this, in the roll-out stage, our algorithm sorts the available move list by the number to floor line ascending and number to pattern line descending of a move and then the next player to move chooses the first move in the sorted list, which has the highest number to pattern line while the lowest number to floor line.

- Limited simulation times
Since the time limit of each move is 1 second, the simulation times cannot be set too high. The cost is that insufficient simulations cannot precisely reflect the value of a step. To address this, three improvements have been made. First, the number of nodes to be expanded is limited. In other words, the untried moves of a node are reduced. To achieve this, the untried moves list is sorted by number to floor line ascending and number to pattern line descending, which ensures that the front of the list is quality moves. And the size of the move list is reduced to 1/10 of the old one after experiments i.e. we only expand 1/10 of the available moves. Besides, the total moves of the roll-out stage are limited to 3 instead of moving until the end of the round. Since the simulation times are limited, to focus on exploitation, the weight of the exploration part of  UBC is set to 0. Initially, the maximum simulation times were around 200. After being improved, the algorithm can simulate 300 times.






# AZUL GUI

This repository contains a framework to support developing autonomous agents for the boardgame AZUL, published by Plan B Games. The game frame is forked from [Michelle Blom](https://github.com/michelleblom)'s repository, and GUI is developed by [Guang Hu](https://github.com/guanghuhappysf128) and  [Ruihan Zhang](https://github.com/zhangrh93). The code is in Python 3.

Students should be able to use this frame and develop their own agent under the directory players. This framework is able to run AZUL with two agents in a 1v1 game, and GUI will allow user to navigate through recorded game states. In addition, a replay can be saved and played for debug purpose.

Some information about the game:
- https://en.wikipedia.org/wiki/Azul_(board_game)
- https://boardgamegeek.com/boardgame/230802/azul
- https://www.planbgames.com/en/news/azul-c16.html
- https://github.com/michelleblom/AZUL

# Setting up the environment

Python 3 is required, and library tkinter should be installed along with python 3.

The code uses three library that required to be installed: ```numpy```,```func_timeout```,```tqdm```, which can be done with the following command:
```bash
pip install numpy tqdm func_timeout
```
If have both python 2 and python 3 installed, you might need to use following command:
```bash
pip3 install numpy tqdm func_timeout
```

# How to run it?

The code example can be run with command:
```bash
python runner.py
```
, which will run the game with two default players (naive_player). 

A standard example to run the code would be:
```bash
python runner.py -r naive_player -b random_player -s 
```

Other command line option can be viewed with argument: ```-h``` or ```--help```

When a game ends, the GUI will pause to allow user selecting each states on listbox (right side of the window), and it will change accordingly. And replay file will be generated once the GUI window is closed.


**Extra function**
- timeout limit
- timeout warning and fail
- replay system
- GUI displayer (allow switch)
- delay time setting
= 

**class and parameters**

*AdvancedRunner*

Runner with timelimit, timeout warnings, displayer, replay system. It returns a replay file.

*ReplayRunner*

Use replay file to unfold a replay

*GUIGameDisplayer*

GUI game displayer, you coud click items in the list box and use arrow keys to select move.
