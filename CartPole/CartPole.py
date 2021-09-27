import gym
import numpy as np
import math
import time
import pickle
from plot import plot
from numpy.core.fromnumeric import argmax

EPISODES = 1000
RENDER_EPISODE = EPISODES / 20

EPSILON_MIN = 0.01
DECAY = 25
LEARNING_RATE_MIN =  0.1
DISCOUNT = 1

class Cart_agent:

    def __init__(self):
        self.env = gym.make("CartPole-v1")
        self.Q = {}
        self.epsilon = EPSILON_MIN
        self.learning_rate = LEARNING_RATE_MIN
        self.decay = DECAY
        self.discount = DISCOUNT
        self.number_actions = self.env.action_space.n
        self.all_rewards = []
        self.mean_rewards = []
        self.upper_bounds = [self.env.observation_space.high[0], 0.5, self.env.observation_space.high[2], math.radians(50) / 1.]
        self.lower_bounds = [self.env.observation_space.low[0], -0.5, self.env.observation_space.low[2], -math.radians(50) / 1.]
        self.buckets = (3, 3, 6, 6)

    def discretize_state(self, state) -> tuple:
        """
        Método usado para arredondar estados similares para um mesmo estado
        não exigindo muito poder computacional
        Inputs:
            state -> tupla contendo o estado atual do ambiente
        Outputs: 
            estado arredondado
        """
        discretized = list()
        for i in range(len(state)):
            scaling = ((state[i] + abs(self.lower_bounds[i])) / (self.upper_bounds[i] - self.lower_bounds[i]))
            new_state = int(round((self.buckets[i] - 1) * scaling))
            new_state = min(self.buckets[i] - 1, max(0, new_state))
            discretized.append(new_state)
        
        return tuple(discretized)

    def decide_action(self, state) -> int:
        """
        Método usado para decisão da ação
        Inputs:
            state -> tupla contendo o estado atual do ambiente
        Outputs:
            action -> inteiro que determina ação do agente
        """
        if state not in self.Q.keys():
            self.Q[state] = [0] * self.number_actions
        
        if np.random.random() < self.epsilon:
            action = self.env.action_space.sample()
        else:
            action = argmax(self.Q[state])
            
        return action
    
    def update_q(self, current_state, action, reward, next_state):
        """
        Método para atualizar o valor de Q baseado na equação de bellman
        Inputs:
            current_state -> tupla contendo o estado atual do ambiente
            action -> inteiro que determina ação do agente
            reward -> float contendo valor escalar de recompensa
            next_state -> tupla contendo o estado futuro do ambiente
        """
        if current_state not in self.Q.keys():
            self.Q[current_state] = [0] * self.number_actions
        if next_state not in self.Q.keys():
            self.Q[next_state] = [0] * self.number_actions
        
        self.Q[current_state][action] = self.Q[current_state][action] + self.learning_rate * (reward + self.discount * np.max(self.Q[next_state]) - self.Q[current_state][action])
        
    
    def update_learning_rate(self, episode) -> float:
        """
        Método para atualizar o valor do learning_rate
        Inputs:
            episode -> inteiro correspondente ao episódio atual
        Outputs:
            float com valor do learning rate
        """
        learning_rate = min(1, 1 - math.log10((episode + 1) / DECAY))
        learning_rate = max(learning_rate, LEARNING_RATE_MIN)
        
        return learning_rate
    
    def update_epsilon(self, episode) -> float:
        """
        Método para atualizar o valor do epsilon
        Inputs:
            episode -> inteiro correspondente ao episódio atual
        Outputs:
            float com valor do epsilon
        """
        epsilon = min(1, 1 - math.log10((episode + 1) / DECAY))
        epsilon = max(epsilon, EPSILON_MIN)

        return epsilon
    
    def train(self):
        """
        Método utilizado para treinar o ambiente
        """
        for episode in range(EPISODES):
            current_state = self.env.reset()
            current_state = self.discretize_state(current_state)

            done = False
            
            rewards = 0
            
            while not done:

                if episode % RENDER_EPISODE == 0:
                    self.save_model("model/model.pickle")
                    self.env.render()
                    time.sleep(0.01)

                action = self.decide_action(current_state)

                next_state, reward, done, _ = self.env.step(action)
                next_state = self.discretize_state(next_state)

                self.update_q(current_state, action, reward, next_state)

                current_state = next_state
                rewards += reward

            self.epsilon = self.update_epsilon(episode)
            self.learning_rate = self.update_learning_rate(episode)

            self.all_rewards.append(rewards)
            mean_reward = (sum(self.all_rewards) / (episode + 1))
            self.mean_rewards.append(mean_reward)

            plot(self.all_rewards, self.mean_rewards, self.epsilon)
        
        self.env.close()


    def save_model(self, path):
        """
        Método para salvar o modelo

        Inputs: 
            path: Caminho onde o arquivo deve ser salvo
        """
        with open(path, 'wb') as model:
            pickle.dump(self.Q, model)
    
    def load_model(self, path) -> pickle:
        """
        Método para carregar o modelo

        Inputs: 
            path: Caminho que contem o modelo
        Outputs:
            Modelo carregado
        """
        with open(path, 'rb') as model:
           return pickle.load(model)

           
if __name__ == "__main__":
    agent = Cart_agent()
    agent.train()

    
    

