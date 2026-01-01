import math
import random
from game import TicTacToe

class Node:
    def __init__(self, state: TicTacToe, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move # The move that led to this state
        self.children = []
        self.visits = 0
        self.total_reward = 0 # Global reward (Computer's perspective)

    def is_fully_expanded(self):
        valid_moves = self.state.get_valid_moves()
        return len(self.children) == len(valid_moves)

    @property
    def q_value(self):
        if self.visits == 0:
            return 0
        return self.total_reward / self.visits

class MCTS:
    def __init__(self, exploration_constant=1.414):
        self.C = exploration_constant

    def search(self, root_state: TicTacToe, n_simulations: int):
        root = Node(root_state.clone())
        
        for _ in range(n_simulations):
            node = self.select(root)
            # If the selected node is terminal, we can't expand. 
            # If it's not terminal but not fully expanded, expand it.
            if not node.state.game_over:
                if not node.is_fully_expanded():
                    node = self.expand(node)
            
            result = self.simulate(node)
            self.backpropagate(node, result)
        
        # Determine best move
        # Robust child: most visited
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move

    def select(self, node):
        while not node.state.game_over and node.is_fully_expanded():
            if node.state.current_player == 1:
                # Computer's turn: Maximize Q + U
                node = max(node.children, key=lambda c: self.ucb_score(c, node, maximize=True))
            else:
                # Opponent's turn: Minimize Q - U
                node = min(node.children, key=lambda c: self.ucb_score(c, node, maximize=False))
        return node

    def ucb_score(self, child, parent, maximize):
        if child.visits == 0:
            # Infinite exploration value for unvisited nodes
            # But in our logic, we only select from children. 
            # Expand adds 1 child at a time. SELECT only traverses fully expanded nodes.
            # So this case theoretically shouldn't happen in the loop if logic is correct,
            # but for safety: 
            return float('inf') if maximize else float('-inf')
        
        q = child.q_value
        u = self.C * math.sqrt(math.log(parent.visits) / child.visits)
        
        if maximize:
            return q + u
        else:
            return q - u

    def expand(self, node):
        valid_moves = node.state.get_valid_moves()
        # Find moves that haven't been tried yet
        tried_moves = [child.move for child in node.children]
        untried_moves = [m for m in valid_moves if m not in tried_moves]
        
        if not untried_moves:
            # Should not happen if check was done before calling expand
            return node
        
        move = random.choice(untried_moves)
        next_state = node.state.clone()
        next_state.make_move(move[0], move[1])
        
        child_node = Node(next_state, parent=node, move=move)
        node.children.append(child_node)
        return child_node

    def simulate(self, node):
        current_state = node.state.clone()
        while not current_state.game_over:
            moves = current_state.get_valid_moves()
            if not moves:
                break
            move = random.choice(moves)
            current_state.make_move(move[0], move[1])
        
        return current_state.get_result()

    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.total_reward += result
            node = node.parent
