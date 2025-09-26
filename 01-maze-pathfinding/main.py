import numpy as np
from collections import defaultdict
from mazeGenerator import PrimsMaze
from algorithm import A_star, bfs, dfs, greedy, iterative_deepening_search
from graphics import initialize_plot, display_final_result

def mat2graph(mat):
    rows, cols = mat.shape
    graph = defaultdict(list)
    for x in range(rows):
        for y in range(cols):
            if mat[x, y] != 0:
                for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and mat[nx, ny] != 0:
                        graph[(x, y)].append((nx, ny))
    return graph


if __name__ == "__main__":
    size = int(input("Enter size of maze/graph: "))
    algorithm = input("Choose an algorithm (A*, BFS, DFS, Greedy, IDS): ").strip().lower()

    print("Generating random maze...")
    obj = PrimsMaze(size, show_maze=True)
    maze_bool = obj.create_maze((0, 0))
    maze_numeric = np.where(maze_bool, 1, 0).astype(np.uint8)

    fig, ax1, ax2, ax3 = initialize_plot(maze_numeric, algorithm)
    
    graph = mat2graph(maze_numeric)
    start = (0, 0)
    destination = (maze_numeric.shape[0] - 1, maze_numeric.shape[1] - 1)
    pathMap = maze_numeric.copy()

    algorithms = {
        "a*": A_star,
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "ids": iterative_deepening_search
    }

    if algorithm in algorithms:
        result, expanded, elapsed = algorithms[algorithm](graph, start, destination, pathMap, ax2, ax3)
        display_final_result(algorithm, result, expanded, elapsed)
    else:
        print("Invalid algorithm selection!")
