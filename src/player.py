from grid import Grid
from numpy import array

class Player:
    def __init__(self, grid: Grid):
        self.maze = grid

        self.x = 0
        self.y = 0

        self.score = 0
        self.lives = 3

        self.penalty = -1
        self.reward = 20

    def update_player(self):
        if self.maze.is_goal(self.x, self.y):
            self.score += self.reward
            self.maze.clear_goal(self.x, self.y)
            self.maze.set_random_goal()
        self.maze.grid[self.x][self.y] = 3

    def move_right(self):
        if self.maze.is_valid_position(self.x+1, self.y):
            self.maze.grid[self.x][self.y] = 0
            self.x += 1

        self.score += self.penalty

    def move_left(self):
        if self.maze.is_valid_position(self.x-1, self.y):
            self.maze.grid[self.x][self.y] = 0
            self.x -= 1

        self.score += self.penalty

    def move_down(self):
        if self.maze.is_valid_position(self.x, self.y+1):
            self.maze.grid[self.x][self.y] = 0
            self.y += 1

        self.score += self.penalty

    def move_up(self):
        if self.maze.is_valid_position(self.x, self.y-1):
            self.maze.grid[self.x][self.y] = 0
            self.y -= 1

        self.score += self.penalty