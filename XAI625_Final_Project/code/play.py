import sys
from game import TicTacToe
from mcts import MCTS

def main():
    print("Tic-Tac-Toe MCTS")
    try:
        n_sims = int(input("Enter number of MCTS simulations per move (default 1000): ") or "1000")
    except ValueError:
        n_sims = 1000
    print(f"Using {n_sims} simulations.")

    choice = input("Do you want to play first? (y/n): ").lower()
    human_first = choice == 'y'

    game = TicTacToe()
    mcts = MCTS()

    while not game.game_over:
        game.print_board()
        
        # Player 1 is X (Computer). Player -1 is O (Human/Opponent).
        # But in our game logic: 1 is X, -1 is O.
        # If Human is first, Human should be Player 1?
        # The prompt says: "If the computer wins, reward +1."
        # Usually Computer is Agent. 
        # Let's map: 
        #   If Human plays first, Human is X (1), Computer is O (-1).
        #   If Computer plays first, Computer is X (1), Human is O (-1).
        #   But our MCTS is hardcoded to maximize +1 (Computer).
        #   So if Computer is -1 (O), it should still maximize Computer's win.
        #   If Computer is O (-1):
        #       Win means winner == -1.
        #       Our game.get_result() returns: 1 if winner==1, -1 if winner==-1.
        #       If Computer is O, Computer's +1 reward corresponds to game result -1.
        #       This means our MCTS `get_result` needs to align with who is "Computer".
        #
        #   Wait, `game.py` rewards are hardcoded: 1 for X, -1 for O.
        #   And `mcts.py` accumulates these raw results.
        #   And `mcts.select` assumes: Player 1 maximizes, Player -1 minimizes.
        #   So Player 1 WANTS +1 (Game 1). Player -1 WANTS -1 (Game -1).
        #   This is consistent!
        #   So:
        #       - If Computer is X (1): It tries to get +1. (Max) -> Correct.
        #       - If Computer is O (-1): It tries to get -1. (Min)
        #           - But `mcts.select` says "If current_player == -1 (Opponent's Turn... wait)".
        #           - `mcts.select` check: `if node.state.current_player == 1`.
        #           - This logic hardcodes: Player 1 is Max, Player -1 is Min.
        #           - So as long as Computer plays ACCORDING TO ITS ROLE, it works.
        #           - If Computer is O (-1): It is playing on "current_player == -1" turns.
        #           - On these turns, `select` does `min(Q - U)`.
        #           - So it searches for moves that minimize Q (lead to -1).
        #           - This is CORRECT for O! O wants -1.
        #   So we don't need to change MCTS. We just need to assign roles correctly.
        
        # Mapping: 1 = X, -1 = O.
        # Turn starts with 1.
        
        turn_player = game.current_player
        
        is_human_turn = False
        if human_first:
            if turn_player == 1: is_human_turn = True
        else:
            if turn_player == -1: is_human_turn = True
            
        if is_human_turn:
            print("Your turn (row col): ", end="")
            try:
                inp = input().split()
                if not inp: continue
                r, c = map(int, inp)
                game.make_move(r, c)
            except Exception as e:
                print(f"Invalid input: {e}")
        else:
            print("Computer is thinking...")
            best_move = mcts.search(game, n_sims)
            game.make_move(best_move[0], best_move[1])
            print(f"Computer played: {best_move}")

    game.print_board()
    if game.winner == 0:
        print("Draw!")
    elif game.winner == 1:
        # 1 is X.
        if human_first: print("You Win!") # Human X
        else: print("Computer Wins!") # Computer X
    else:
        # -1 is O.
        if human_first: print("Computer Wins!") # Computer O
        else: print("You Win!") # Human O

if __name__ == "__main__":
    main()
