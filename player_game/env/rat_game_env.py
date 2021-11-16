from os import stat
from random import choice
import gym
import pygame
from player import Player
from grid import Grid
from utils import load_image
from time import sleep
import numpy as np
import math
import pickle
import time
import plot

pygame.init()
font = pygame.font.SysFont("arial", 25)

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

        self.reward_ahead = False

    def step(self, action):

        self.curr_step += 1
        self._take_action(action)
        self.maze.update()

        reward = self._get_reward()
        ob = self._get_state()
        return ob, reward, self.maze.done

    def _reset(self):
        self.agent = Player(0, 0, "Agent")
        self.maze = Grid(self.agent, n_cols=10, n_rows=10)

        self.iteration += 1
        self.curr_step = 0

        return self._get_state()

    def _render(self, mode="human", close=False):
        rect_width = 500 // 10
        rect_height = 500 // 10

        for x in range(0, 10):
            for y in range(0, 10):
                # Posicao
                rect = pygame.Rect(
                    x * rect_width, y * rect_height, rect_width, rect_height
                )

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
                        self.screen.blit(human_rat_up, rect)
                    elif self.agent.direction == "Down":
                        self.screen.blit(human_rat_down, rect)
                    elif self.agent.direction == "Right":
                        self.screen.blit(human_rat_right, rect)
                    else:
                        self.screen.blit(human_rat_left, rect)

        self.clock.tick(1000)
        pygame.display.update()

    def _get_state(self):
        # [0 , 0 , 0,  0]
        # [0 , 3 , 0,  0]
        # [0 , ^ , 0 , 0]
        # [0 , 0 , 0,  0]

        # (2, 1) -> (1,1) + (0,1) -> [0,0]

        # Retornar linha reta
        state = []

        current_x = self.agent.x
        current_y = self.agent.y
        state.append(current_x)
        state.append(current_y)

        if self.maze.is_valid_position(current_x + 1, current_y):
            state.append(self.maze.grid[current_x + 1, current_y])
        else:
            state.append(3)

        if self.maze.is_valid_position(current_x - 1, current_y):
            state.append(self.maze.grid[current_x - 1, current_y])
        else:
            state.append(3)
        
        if self.maze.is_valid_position(current_x, current_y + 1):
            state.append(self.maze.grid[current_x, current_y + 1])
        else:
            state.append(3)
            
        if self.maze.is_valid_position(current_x, current_y - 1):
            state.append(self.maze.grid[current_x, current_y - 1])
        else:
            state.append(3)


        if self.agent.direction == "Up":
            current_x -= 2

            if self.maze.is_valid_position(current_x, current_y):
                state.append(self.maze.grid[current_x, current_y])
            else:
                state.append(3)

        if self.agent.direction == "Down":
            current_x += 2
            if self.maze.is_valid_position(current_x, current_y):
                state.append(self.maze.grid[current_x, current_y])
            else:
                state.append(3)

        if self.agent.direction == "Right":
            current_y += 2
            if self.maze.is_valid_position(current_x, current_y):
                state.append(self.maze.grid[current_x, current_y])
            else:
                state.append(3)

        if self.agent.direction == "Left":
            current_y -= 2
            if self.maze.is_valid_position(current_x, current_y):
                state.append(self.maze.grid[current_x, current_y])
            else:
                state.append(3)

        return state  # (self.agent.x, self.agent.y)

    def _take_action(self, action):
        # print(action)
        self.agent.got_cheese = False
        directions = ["Up", "Down", "Left", "Right"]
        self.agent.move(directions[action], self.maze)

    def _get_reward(self):
        #reward = 1
        reward = -0.01

        if self.reward_ahead:
            reward += 0.01
            self.reward_ahead = False

        if self.maze.done:
            reward += 5

        elif self.agent.eaten_cheese:
            reward += 1

        return reward


EPISODES = 10000
RENDER_EPISODE = 200
EPSILON_MINIMUM = 0.001
DECAY = np.prod((10, 10), dtype=float) / 3
LEARNING_RATE_MINIMUM = 0.2
DISCOUNT = 0.99


class Maze_agent:
    def __init__(self):
        self.env = Rat_Game()
        self.maze_size = tuple([10, 10])
        self.state_bounds = list(zip([0, 0], [10, 10]))
        self.number_actions = 4
        self.number_blocks = 5
        self.vision = (
            self.number_blocks,
            self.number_blocks,
            self.number_blocks,
            self.number_blocks,
            self.number_blocks,
        )
        self.Q = np.zeros(
            self.maze_size + self.vision + (self.number_actions,), dtype=float
        )  # FIX #ERRO NO Q
        self.epsilon = 1
        self.learning_rate = 1
        self.decay = DECAY
        self.discount = DISCOUNT
        self.all_rewards = []
        self.mean_rewards = []

    def discretize_state(self, state) -> tuple:  # FIX
        return tuple(state)

    def decide_action(self, state) -> int:

        if np.random.random() < self.epsilon:
            action = choice(list(range(4)))  # self.env.action_space.sample()
        else:
            #print(f"State: {state}")
            #print(f"Q[state]: {self.Q[state]}")
            action = int(np.argmax(self.Q[state]))

        return action

    def update_q(self, current_state, action, reward, next_state):  # FIX

        self.Q[tuple(current_state) + (action,)] = self.Q[tuple(current_state) + (action,)] + self.learning_rate * (reward+ self.discount * np.max(self.Q[tuple(next_state)])- self.Q[tuple(current_state) + (action,)]
        )

    def update_learning_rate(self, episode) -> float:
        learning_rate = min(1, 1 - math.log10((episode + 1) / DECAY))
        learning_rate = max(learning_rate, LEARNING_RATE_MINIMUM)

        return learning_rate

    def update_epsilon(self, episode) -> float:
        epsilon = min(1, 1 - math.log10((episode + 1) / DECAY))
        epsilon = max(epsilon, EPSILON_MINIMUM)

        return epsilon

    def train(self):
        for episode in range(EPISODES):
            current_state = self.env._reset()
            current_state = self.discretize_state(current_state)

            done = False

            rewards = 0

            moves = 0

            while not done:

                if episode % RENDER_EPISODE == 0:
                    #self.save_model("model/model.pickle")
                    self.env._render()
                    time.sleep(0.02)

                action = self.decide_action(current_state)

                next_state, reward, done = self.env.step(action)
                next_state = self.discretize_state(next_state)

                self.update_q(current_state, action, reward, next_state)

                current_state = next_state
                rewards += reward

                moves += 1

                #if moves >= 1000:
                    #done = True
            
            if(episode > 200):
                self.epsilon = self.update_epsilon(episode - 200)
                self.learning_rate = self.update_learning_rate(episode - 200)

            self.all_rewards.append(rewards)
            mean_reward = sum(self.all_rewards) / (episode + 1)
            self.mean_rewards.append(mean_reward)
            plot.plot(self.all_rewards, self.mean_rewards, self.epsilon)

        self.env.close()

    def save_model(self, path):
        with open(path, "wb") as model:
            pickle.dump(self.Q, model)

    def load_model(self, path) -> pickle:
        with open(path, "rb") as model:
            return pickle.load(model)


if __name__ == "__main__":
    agent = Maze_agent()
    agent.train()
