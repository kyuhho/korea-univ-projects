import matplotlib.pyplot as plt
from game import TicTacToe
from mcts import MCTS, Node
import random

def get_filtered_children(node, current_depth):
    """
    Returns filtered children based on pruning logic:
    - Root's children (depth 0 transitions to depth 1): Show ALL
    - Deeper levels: Show only Top 3 visited
    """
    sorted_children = sorted(node.children, key=lambda c: c.visits, reverse=True)
    if current_depth == 0:
        return sorted_children
    return sorted_children[:2]

def get_tree_width(node, max_depth, current_depth=0):
    if current_depth >= max_depth:
        return 1
    
    children_to_show = get_filtered_children(node, current_depth)
    if not children_to_show:
        return 1
    
    width = 0
    for child in children_to_show:
        width += get_tree_width(child, max_depth, current_depth + 1)
    return width

def plot_mcts_tree(node, x, y, width, max_depth, current_depth=0, ax=None):
    if current_depth > max_depth:
        return

    # Draw the current node
    move_str = f"M:{node.move}" if node.move else "Root"
    info = f"{move_str}\nN={node.visits}\nQ={node.q_value:.2f}"
    
    # Node visual parameters
    bbox_props = dict(boxstyle="round,pad=0.3", fc="lightblue", ec="black", lw=1)
    ax.text(x, y, info, ha="center", va="center", size=8, bbox=bbox_props, zorder=10)

    if current_depth == max_depth or not node.children:
        return

    # Use same filtering logic
    children_to_show = get_filtered_children(node, current_depth)
    
    # Calculate widths of children subtrees to allocate space
    child_widths = [get_tree_width(child, max_depth, current_depth + 1) for child in children_to_show]
    total_width = sum(child_widths)
    
    # Calculate starting x for the first child
    current_x = x - total_width / 2.0
    
    for i, child in enumerate(children_to_show):
        w = child_widths[i]
        # Center of the child's allocated segment
        child_x = current_x + w / 2.0
        child_y = y - 1.0  # Move down by 1 unit
        
        # Draw edge
        ax.plot([x, child_x], [y, child_y], 'k-', lw=1, zorder=1)
        
        # Recursively plot child
        plot_mcts_tree(child, child_x, child_y, w, max_depth, current_depth + 1, ax)
        
        current_x += w

def visualize_mcts_tree(root, max_depth=2, filename="mcts_tree.png"):
    # Determine tree width for aspect ratio
    total_width = get_tree_width(root, max_depth)
    
    # Figure setup
    # Width: correlated with tree width, Height: correlated with depth
    fig_width = max(8, total_width * 0.6)
    fig_height = (max_depth + 1) * 0.8
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Root at (0, 0), initial width = total_width
    plot_mcts_tree(root, 0, 0, total_width, max_depth, current_depth=0, ax=ax)
    
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Visualization saved to {filename}")
    plt.close()

def main():
    print("Generating MCTS search tree...")
    game = TicTacToe()
    mcts = MCTS()
    
    root_state = game.clone()
    root = Node(root_state)
    
    n_sims = 500
    print(f"Running {n_sims} simulations...")
    for _ in range(n_sims):
        node = mcts.select(root)
        if not node.state.game_over:
            if not node.is_fully_expanded():
                node = mcts.expand(node)
        result = mcts.simulate(node)
        mcts.backpropagate(node, result)
        
    print("Simulations complete.")
    
    depth_to_visualize = 2
    print(f"Creating visualization for top {depth_to_visualize} levels...")
    visualize_mcts_tree(root, max_depth=depth_to_visualize)

if __name__ == "__main__":
    main()
