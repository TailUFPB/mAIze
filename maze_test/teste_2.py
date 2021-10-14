import gym
import numpy as np
import gym_maze

env = gym.make("maze-sample-5x5-v0")

MAZE_SIZE = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
NUM_BUCKETS = MAZE_SIZE 
STATE_BOUNDS = list(zip(env.observation_space.low, env.observation_space.high))

def state_to_bucket(state):
    bucket_indice = []
    for i in range(len(state)):
        if state[i] <= STATE_BOUNDS[i][0]:
            bucket_index = 0
        elif state[i] >= STATE_BOUNDS[i][1]:
            bucket_index = NUM_BUCKETS[i] - 1
        else:
            bucket_index = int(round(state[i]))
        bucket_indice.append(bucket_index)
    return tuple(bucket_indice)

state = env.reset()

print(f"Begining state = {state}")

state = state_to_bucket(state)

print(f"Final state = {state}")