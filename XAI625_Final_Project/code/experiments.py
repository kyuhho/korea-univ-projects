import random
import matplotlib.pyplot as plt
from game import TicTacToe
from mcts import MCTS

class RandomPlayer:
    def get_move(self, game):
        moves = game.get_valid_moves()
        return random.choice(moves) if moves else None

def play_match(initial_move, mcts_sims):
    """
    Plays one game.
    initial_move: (r, c) tuple. The FIRST move made in the game by MCTS.
    """
    game = TicTacToe()
    mcts = MCTS()
    random_player = RandomPlayer()
    
    # Force initial move (Player 1 / MCTS)
    game.make_move(initial_move[0], initial_move[1])
    
    # Continue game
    while not game.game_over:
        if game.current_player == 1:
            # MCTS Turn
            move = mcts.search(game, mcts_sims)
            game.make_move(move[0], move[1])
        else:
            # Random Turn (Player -1)
            move = random_player.get_move(game)
            if move:
                game.make_move(move[0], move[1])
            else:
                pass
            
    # Check result for Player 1 (MCTS)
    # game.winner: 1 (X), -1 (O), 0 (Draw)
    return 1 if game.winner == 1 else 0

def run_experiments():
    # Setup
    simulations_list = [10, 50, 100, 200, 500] 
    GAMES_PER_CONFIG = 50 
    
    initial_moves = [(r, c) for r in range(3) for c in range(3)]
    
    # Store results: results[move] = [win_rate_sim10, win_rate_sim50, ...]
    results = {move: [] for move in initial_moves}
    
    print(f"Running experiments... ({len(simulations_list)} sim levels, {len(initial_moves)} moves, {GAMES_PER_CONFIG} games each)")
    
    for sim_count in simulations_list:
        print(f"  Simulations: {sim_count}")
        for move in initial_moves:
            wins = 0
            for _ in range(GAMES_PER_CONFIG):
                wins += play_match(move, sim_count)
            win_rate = wins / GAMES_PER_CONFIG
            results[move].append(win_rate)
            # print(f"    Move {move}: {win_rate:.2f}")

    # Plotting
    plt.figure(figsize=(10, 6))
    
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*']
    
    for idx, move in enumerate(initial_moves):
        plt.plot(simulations_list, results[move], label=f"Start {move}", marker=markers[idx])
        
    plt.xlabel("Number of MCTS Simulations", fontsize=14)
    plt.ylabel("Average Win Rate (Player X)", fontsize=14)
    # Calculate dynamic lower bound for y-axis
    # logic: floor(min_val / 0.05) * 0.05
    all_dates = [val for sublist in results.values() for val in sublist]
    min_val = min(all_dates) if all_dates else 0
    y_min = int(min_val / 0.05) * 0.05
    
    plt.ylim(y_min, 1.05)
    plt.legend(fontsize=12)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.grid(True)
    
    output_file = "experiment_results.png"
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    run_experiments()
