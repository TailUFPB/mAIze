import torch
import random
import numpy as np
from collections import deque
from game import Rat_Game
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0

        self.epsilon = 0   # randomness
        self.gamma = 0.9   # discount rate

        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(6, 256, 4) 
        self.trainer = QTrainer(self.model, LR, self.gamma) 

    def get_state(self, game):
        x = game.player.x
        y = game.player.y

        goal_left = x > game.grid.goal_x
        goal_right = x < game.grid.goal_x

        goal_up = y > game.grid.goal_y
        goal_down = y < game.grid.goal_y

        state  = [x, y, goal_left, goal_right, goal_up, goal_down]
        #print(state)

        return np.array(state, dtype = int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, done = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0,3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []

    total_score = 0
    record = 0

    agent = Agent()
    game = Rat_Game()

    while True:
        old_state = agent.get_state(game)

        final_move = agent.get_action(old_state)

        
        reward, done, score = game.game_step(final_move)
        new_state = agent.get_state(game)

        # short memory 
        agent.train_short_memory(old_state, final_move, reward, new_state, done)

        # remember
        agent.remember(old_state, final_move, reward, new_state, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save()
            
            print("Game", agent.n_games)
            print("Score:", score)
            print("Record:", record)
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == "__main__":
    train()