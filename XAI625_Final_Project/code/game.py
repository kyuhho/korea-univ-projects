import copy

class TicTacToe:
    def __init__(self):
        # 3x3 board
        # 0: empty, 1: X (Computer), -1: O (Human/Opponent)
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.current_player = 1 # 1 for X, -1 for O
        self.winner = None
        self.game_over = False

    def clone(self):
        """Creates a deep copy of the game state."""
        new_game = TicTacToe()
        new_game.board = copy.deepcopy(self.board)
        new_game.current_player = self.current_player
        new_game.winner = self.winner
        new_game.game_over = self.game_over
        return new_game

    def get_valid_moves(self):
        """Returns a list of (row, col) executable moves."""
        if self.game_over:
            return []
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == 0:
                    moves.append((r, c))
        return moves

    def make_move(self, row, col):
        """Executes a move and updates game state."""
        if self.board[row][col] != 0 or self.game_over:
            raise ValueError(f"Invalid move: ({row}, {col})")
        
        self.board[row][col] = self.current_player
        self.check_status()
        self.current_player *= -1 # Switch turn

    def check_status(self):
        """Checks for win or draw."""
        # Check rows, cols, diagonals
        lines = []
        # Rows
        lines.extend(self.board)
        # Cols
        for c in range(3):
            lines.append([self.board[r][c] for r in range(3)])
        # Diagonals
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2-i] for i in range(3)])

        for line in lines:
            if abs(sum(line)) == 3:
                self.winner = 1 if sum(line) == 3 else -1
                self.game_over = True
                return

        # Check Draw
        is_full = True
        for r in range(3):
            if 0 in self.board[r]:
                is_full = False
                break
        
        if is_full:
            self.game_over = True
            self.winner = 0 # Draw

    def get_result(self):
        """
        Returns the result from the Computer's perspective (Player 1).
        +1 if Computer wins, -1 if Human wins, 0 if Draw.
        Returns None if game is not over.
        """
        if not self.game_over:
            return None
        if self.winner == 1:
            return 1
        elif self.winner == -1:
            return -1
        else:
            return 0
            
    def print_board(self):
        chars = {0: ' ', 1: 'X', -1: 'O'}
        print("---------")
        for r in range(3):
            print("|", end="")
            for c in range(3):
                print(f" {chars[self.board[r][c]]} ", end="")
            print("|")
        print("---------")
