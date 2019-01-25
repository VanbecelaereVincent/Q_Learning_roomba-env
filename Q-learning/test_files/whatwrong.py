import gym
import roomba_env


env =gym.make("roomba-v0")


actions = env.legal_actions("friendly")
print(actions)


env.step("B", "friendly", True)
import time


env.close()

import numpy as np

def read_file(filename):
    new_data = np.loadtxt(filename)
    new_data = new_data.reshape((121, 121, 5))
    return new_data


q_values_enemy = read_file("Q_enemy.txt")
q_values_friendly = read_file("Q_friendly.txt")


print(q_values_friendly[39][6])