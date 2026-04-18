![quixx](https://github.com/user-attachments/assets/e0d8c9f6-bba4-45aa-9e51-dcd5cac358f8)
# Quixx Reinforcement Learning
A custom Gymnasium environment for Quixx (the popular 2–5 player dice game) with three reinforcement learning agents: tabular **Q-Learning**, **Monte Carlo Tree Search (MCTS)**, and **Deep Q-Network (DQN)**. My wife loves this game, and I think (besides one lucky win) I can never quite figure out what the best strategy is. This analysis uses some reinforcement learning and deep learning methods to see if a model can outperform randomness.

## Quixx Rules
Quixx is a dice game where you try to maximize your score before the game abruptly ends. The suggested number of players is 2-5. There are six dice in play, two white dice, and a red, yellow, green, and blue die (W1, W2, R, Y, G, B). Each player is given a card that looks something like this:

|     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Red    | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 |     | 12 | 🔒 |
| Yellow | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 |     | 12 | 🔒 |
| Green  | 12 | 11 | 10 | 9  | 8  | 7  | 6  | 5  | 4  | 3  |     | 2  | 🔒 |
| Blue   | 12 | 11 | 10 | 9  | 8  | 7  | 6  | 5  | 4  | 3  |     | 2  | 🔒 |

Quixx is a stochastic, sequential decision-making game with a massive state space. This project implements a fully functional environment (`quixx_env.py`) and compares three classic RL approaches to discover better strategies than typical human heuristics.

## Files
- `quixx_game.py` — Core game logic and scoring
- `quixx_env.py`  — Gymnasium environment wrapper
- `Quixx Reinforcement Learning Notebook.ipynb` — Full training, evaluation, and analysis notebook
- `Quixx Report` — Six Pager summarizing the methodologies and results
