import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


colors = ["blue", (0.75,0.75,0.75)]
cmap = mcolors.ListedColormap(colors)
delay = 0.005

class PrimsMaze:
    def __init__(self, size=25, show_maze=True):
        self.size = (size // 2) * 2 + 1
        self.show_maze = show_maze
        self.walls_list = []
        self.grid = np.full((self.size, self.size), -50, dtype=int)
        for i in range(self.size // 2 + 1):
            for j in range(self.size // 2 + 1):
                self.grid[i * 2, j * 2] = -1
        self.maze = np.zeros((self.size, self.size), dtype=bool)
        

    def is_valid(self, curr, dx, dy):
        x, y = curr
        return 0 <= x + dx < self.size and 0 <= y + dy < self.size

    def add_neighbors(self, curr):
        nearby = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for dx, dy in nearby:
            if self.is_valid(curr, dx, dy):
                self.walls_list.append((curr[0] + dx, curr[1] + dy))

    def create_maze(self, start):
        start = ((start[0] // 2) * 2, (start[1] // 2) * 2)
        self.grid[start[0], start[1]] = 1
        self.add_neighbors(start)
        
        
        while len(self.walls_list):
            ind = np.random.randint(0, len(self.walls_list))
            wall_x, wall_y = self.walls_list[ind]
            
            if self.is_valid((wall_x, wall_y), -1, 0) and self.is_valid((wall_x, wall_y), 1, 0):
                top = (wall_x - 1, wall_y)
                bottom = (wall_x + 1, wall_y)
                if self.grid[top] == 1 and self.grid[bottom] == -1:
                    self.grid[wall_x, wall_y] = 1
                    self.grid[bottom] = 1
                    self.add_neighbors(bottom)
                elif self.grid[top] == -1 and self.grid[bottom] == 1:
                    self.grid[wall_x, wall_y] = 1
                    self.grid[top] = 1
                    self.add_neighbors(top)
                self.walls_list.remove((wall_x, wall_y))
            
            if self.is_valid((wall_x, wall_y), 0, 1) and self.is_valid((wall_x, wall_y), 0, -1):
                left = (wall_x, wall_y - 1)
                right = (wall_x, wall_y + 1)
                if self.grid[left] == 1 and self.grid[right] == -1:
                    self.grid[wall_x, wall_y] = 1
                    self.grid[right] = 1
                    self.add_neighbors(right)
                elif self.grid[left] == -1 and self.grid[right] == 1:
                    self.grid[wall_x, wall_y] = 1
                    self.grid[left] = 1
                    self.add_neighbors(left)
                self.walls_list.remove((wall_x, wall_y))
            
            if self.show_maze:
                plt.figure(1)
                plt.clf()
                plt.imshow(self.grid, cmap, interpolation='nearest')
                plt.title('Generating Maze ...')
                plt.pause(delay)
                
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row, col] == 1:
                    self.maze[row, col] = True

        print("Random maze has been generated")
        if self.show_maze:
            plt.pause(2)
            plt.close()

        return self.maze


if __name__ == "__main__":
    colors = ["blue", "white"]
    cmap = mcolors.ListedColormap(colors)
    size = int(input("Enter size of maze (example: 10):- "))
    start = (0, 0)
    obj = PrimsMaze(size)
    maze = obj.create_maze(start).tolist()
    plt.figure(figsize=(10, 5))
    plt.imshow(maze, cmap=cmap, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.title("Final Maze")
    plt.show()

