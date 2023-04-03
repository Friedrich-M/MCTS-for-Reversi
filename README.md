# MCTS-for-Reversi


## 1 About it

This experiment is to investigate the effectiveness of the Monte Carlo tree search algorithm in Reversi. **Monte Carlo Tree Search (MCTS)** is a search algorithm used for decision-making in computer games, where the best decision is predicted by randomly simulating the gameplay, and the accuracy of the prediction is gradually improved by continuously repeating the simulation and decision-making. In this experiment, we used the **Roxanne location prioritization strategy**.

<img src="./media/mcts.png" width=90%>


## 2 Project Tree
```
├── ai.py
├── board.py
├── demo.py
├── game.py
├── MCTS.py
├── README.md
├── results
│   ├── _README.md
│   └── tb_results
│       └── README.md
```

## 3 Run
```
python demo.py
```


## 4 *Tensorboard
```
tensorboard --logdir=results/tb_results --port=6006 --bind_all
```