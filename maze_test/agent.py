import gym
import gym_maze
import numpy as np
import math
import time
from plot import plot
import pickle

from teste_2 import MAZE_SIZE

EPISODES = 10000
RENDER_EPISODE = 10000
EPSILON_MINIMUM = 0.01
DECAY = 25
LEARNING_RATE_MINIMUM = 0.1
DISCOUNT = 1

class Maze_agent:

    def __init__(self):
        self.env = gym.make("maze-random-10x10-v0")
        self.maze_size = tuple((self.env.observation_space.high + np.ones(self.env.observation_space.shape)).astype(int))
        self.state_bounds = list(zip(self.env.observation_space.low, self.env.observation_space.high))
        self.number_actions = self.env.action_space.n
        self.Q = np.zeros(self.maze_size + (self.number_actions, ), dtype=float)
        self.epsilon = 1
        self.learning_rate = 1
        self.decay = DECAY
        self.discount = DISCOUNT
        self.all_rewards = []
        self.mean_rewards = []
        

    def discretize_state(self, state) -> tuple:
        discretazed_state = []
        for i in range(len(state)):
            if state[i] <= self.state_bounds[i][0]:
                new_state = 0
            elif state[i] >= self.state_bounds[i][1]:
                new_state = MAZE_SIZE[i] - 1
            else:
                new_state = int(round(state[i]))
            discretazed_state.append(new_state)
        return tuple(discretazed_state)

    def decide_action(self, state) -> int:
        
        if np.random.random() < self.epsilon:
            action = self.env.action_space.sample()
        else:
            action = int(np.argmax(self.Q[state]))
            
        return action
    
    def update_q(self, current_state, action, reward, next_state):
        
        self.Q[tuple(current_state) + (action,)] = self.Q[tuple(current_state) + (action,)] + self.learning_rate * (reward + self.discount * np.max(self.Q[tuple(next_state)]) - self.Q[tuple(current_state) + (action,)])
        
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
            current_state = self.env.reset()
            current_state = self.discretize_state(current_state)

            done = False
            
            rewards = 0
            
            # moves = 0

            while not done:

                if episode % RENDER_EPISODE == 0:
                    self.save_model("model/model.pickle")
                    #self.env.render()
                    time.sleep(0.01)

                action = self.decide_action(current_state)

                next_state, reward, done, _ = self.env.step(action)
                next_state = self.discretize_state(next_state)

                self.update_q(current_state, action, reward, next_state)

                current_state = next_state
                rewards += reward

                # moves += 1
            
                # if moves >= 500:
                #     done = True
            
            self.epsilon = self.update_epsilon(episode)
            self.learning_rate = self.update_learning_rate(episode)

            self.all_rewards.append(rewards)
            mean_reward = (sum(self.all_rewards) / (episode + 1))
            self.mean_rewards.append(mean_reward)

            plot(self.all_rewards, self.mean_rewards, self.epsilon)
        
        self.env.close()

    def save_model(self, path):
        with open(path, 'wb') as model:
            pickle.dump(self.Q, model)
    
    def load_model(self, path) -> pickle:
        with open(path, 'rb') as model:
           return pickle.load(model)

           
if __name__ == "__main__":
    maze_agent = Maze_agent()
    maze_agent.train()