import pygame as pg
from random import randint
from numpy import array


class Grid:
    def __init__(self, n_cols: int, n_rows: int, screen_width: int, screen_height: int):
        self.n_cols = n_cols
        self.n_rows = n_rows

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.rect_width = self.screen_width//self.n_cols
        self.rect_height = self.screen_height//self.n_rows

        self.grid = [[0 for i in range(self.n_cols)] for j in range(n_rows)]
        self.grid[randint(0, n_cols-1)][randint(0, n_rows-1)] = 2

    def draw_grid(self, screen: pg.Surface):
        for x in range(0, self.screen_width, self.rect_width):
            for y in range(0, self.screen_height, self.rect_height):
                rect = pg.Rect(x, y, self.rect_width, self.rect_height)
                if self.grid[x//self.rect_width][y//self.rect_height] == 1:
                    screen.fill((100, 100, 100), rect)

                elif self.grid[x//self.rect_width][y//self.rect_height] == 2:
                    screen.fill((0, 200, 0), rect)

                elif self.grid[x//self.rect_width][y//self.rect_height] == 3:
                    pg.draw.circle(screen, pg.Color("#ab58a8"), [
                                   x+self.rect_width//2, y+self.rect_height//2], 10)
                else:
                    pg.draw.rect(screen, (0, 0, 0), rect, 1)

    def set_obstacle_on_click(self, x: int, y: int):
        self.grid[x//self.rect_width][y//self.rect_height] = 1

    def clear_goal(self, x:int, y:int):
        self.grid[x][y] = 0

    def set_random_goal(self):
        self.grid[randint(0, self.n_cols-1)][randint(0, self.n_rows-1)] = 2

    def is_valid_position(self, x: int, y: int) -> bool:
        if x > self.n_cols-1 or y > self.n_rows-1:
            return False
        elif x < 0 or y < 0:
            return False
        elif self.grid[x][y] == 1:
            return False
        return True

    def is_goal(self, x: int, y: int) -> bool:
        if self.grid[x][y] == 2:
            return True
        else:
            return False