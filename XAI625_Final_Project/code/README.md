# Tic-Tac-Toe with Monte Carlo Tree Search (MCTS)

This project implements a Tic-Tac-Toe agent using the Monte Carlo Tree Search (MCTS) algorithm. It includes features for playing against the AI, visualizing the search tree, and running experiments to analyze performance.

## Installation

1.  Create and activate a python environment (recommended):
    ```bash
    conda create -n rl python=3.9
    conda activate rl
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Play against the AI
Play a CLI-based game against the MCTS agent.
```bash
python play.py
```
- You can choose to play first (X) or second (O).
- You can set the number of MCTS simulations (difficulty).

### 2. Visualize the MCTS Tree
Generate a visualization of the MCTS decision-making process.
```bash
python visualize.py
```
- Generates `mcts_tree.png`.
- Shows the search tree up to depth 2 (configurable).
- Displays Visit Count (N) and Q-Value (Q) for each node.

### 3. Run Experiments
Analyze the agent's win rate against a random opponent across different simulation counts.
```bash
python experiments.py
```
- Generates `experiment_results.png`.
- Plots win rates for different initial moves.
- Simulation counts: 50, 100, 250, 500.

## Project Structure
- `game.py`: Tic-Tac-Toe game logic.
- `mcts.py`: MCTS algorithm implementation.
- `play.py`: Main script for playing the game.
- `visualize.py`: Script for tree visualization using Matplotlib.
- `experiments.py`: Script for performance analysis.
