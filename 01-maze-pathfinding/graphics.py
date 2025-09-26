import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap, BoundaryNorm


delay = 0.1

# Define colors
free_cell_color = (0.75,0.75,0.75)
block_cell_color = 'blue'
searching_cell_color = 'lightgreen'
path_color = 'red'
start_goal_color = 'red'
colors = [block_cell_color, free_cell_color, searching_cell_color, path_color, start_goal_color]

bounds = [-0.5, 0.5, 13, 100, 150, 200, 255]
cmap = ListedColormap(colors)
norm = BoundaryNorm(bounds, cmap.N + 1)

def initialize_plot(maze_numeric, algorithm):
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(2, 3, height_ratios=[1, 1], width_ratios=[1, 1, 0.05])

    ax1 = plt.subplot(gs[0, 1])
    ax2 = plt.subplot(gs[0, 0])
    ax3 = plt.subplot(gs[1, :2])

    ax1.set_title("Maze")
    ax2.set_title(f"{algorithm.upper()} Search")
    ax3.set_title(f"{algorithm.upper()} Final Path")

    ax1.imshow(maze_numeric, cmap=cmap, norm=norm)
    ax1.set_xticks([]), ax1.set_yticks([])
    
    return fig, ax1, ax2, ax3


def update_visualization(pathMap, ax, title):
    ax.clear()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.imshow(pathMap, cmap=cmap, norm=norm)
    ax.set_title(title)
    plt.pause(delay)


def reconstruct_path(came_from, current, pathMap, ax3, title, start, goal):
    """
    Reconstructs the path from the goal to the start.
    Ensures the path is shown sequentially, one step at a time.
    """
    final_path = [current]
    while current in came_from and came_from[current] is not None:
        current = came_from[current]
        final_path.append(current)

    final_path = final_path[::-1]  # Reverse to get correct order

    for x, y in final_path:
        pathMap[x, y] = 200  # Reveal path step-by-step in red

        ax3.clear()
        ax3.set_xticks([])
        ax3.set_yticks([])
        ax3.imshow(pathMap, cmap=cmap, norm=norm)
        ax3.set_title(title)
        plt.pause(delay)  
    return final_path



def display_final_result(algorithm, result, expanded, elapsed):
    metrics_text = (f"Algorithm: {algorithm.upper()}\n"
                    f"Expanded Nodes: {expanded}\n"
                    f"Time: {elapsed:.4f} seconds")
    plt.figtext(0.75, 0.1, metrics_text, fontsize=12,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    plt.show()
