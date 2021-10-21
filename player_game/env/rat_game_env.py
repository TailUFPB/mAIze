from random import choice
import gym
import pygame
from player import Player
from grid import Grid
from utils import load_image
from time import sleep

pygame.init()
font = pygame.font.SysFont('arial', 25)

rat_up = load_image("spr_rat_up.png")
rat_down = load_image("spr_rat_down.png")
rat_left = load_image("spr_rat_left.png")
rat_right = load_image("spr_rat_right.png")

human_rat_up = load_image("spr_human_rat_up.png", res=(64, 64))
human_rat_down = load_image("spr_human_rat_down.png", res=(64, 64))
human_rat_left = load_image("spr_human_rat_left.png", res=(64, 64))
human_rat_right = load_image("spr_human_rat_right.png", res=(64, 64))

floor_img = load_image("spr_floor_normal.png", res=(50, 50))
wall_img = load_image("spr_tile_middle.png", res=(50, 50))
goal_img = load_image("spr_floor_goal.png", res=(50, 50))
cheese_img = load_image("spr_cheese.png", res=(50, 50))


class Rat_Game(gym.Env):
    def __init__(self):
        self.iteration = -1
        self.curr_step = -1
        self._reset()
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Rar_Game_Env")
        self.clock = pygame.time.Clock()

    def step(self, action):
        if self.maze.done or self.curr_step >= 50:
            self._reset()

        self.curr_step += 1
        self._take_action(action)
        self.maze.update()

        reward = self._get_reward()
        ob = self._get_state()
        return ob, reward, self.agent.got_cheese

    def _reset(self):
        self.agent = Player(0, 0, "Agent")
        self.maze = Grid(self.agent, n_cols=10, n_rows=10)
        
        self.iteration += 1
        self.curr_step = 0

    def _render(self, mode='human', close=False):
        rect_width = 500//10
        rect_height = 500//10

        for x in range(0, 10):
            for y in range(0, 10):
                # Posicao
                rect = pygame.Rect(
                    x * rect_width,  y * rect_height, rect_width, rect_height)

                # Chao
                self.screen.blit(floor_img, rect)

                # Objetivo
                if self.maze.grid[x][y] == 2:
                    self.screen.blit(goal_img, rect)

                # Parede
                elif self.maze.grid[x][y] == 3:
                    self.screen.blit(wall_img, rect)
                # Queijo
                elif self.maze.grid[x][y] == 4:
                    self.screen.blit(cheese_img, rect)

                if self.maze.grid[x][y] == 10:
                    if self.agent.direction == "Up":
                        self.screen.blit(
                            human_rat_up, rect)
                    elif self.agent.direction == "Down":
                        self.screen.blit(
                            human_rat_down, rect)
                    elif self.agent.direction == "Right":
                        self.screen.blit(
                            human_rat_right, rect)
                    else:
                        self.screen.blit(
                            human_rat_left, rect)

        self.clock.tick(10)
        pygame.display.update()

    def _get_state(self):
        return self.maze.grid

    def _take_action(self, action):
        self.agent.got_cheese = False
        self.agent.move(action, self.maze)

    def _get_reward(self):
        return self.agent.got_cheese


if __name__ == "__main__":
    env = Rat_Game()

    while True:
        env.step(choice(["Right", "Up", "Left", "Down"]))
        if env.iteration % 200 == 0:
            env._render()
            sleep(0.01)
