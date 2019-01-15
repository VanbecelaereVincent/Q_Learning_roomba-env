import roomba_env
import gym
from DQN import DQN
import numpy as np
import time



env = gym.make("roomba-v0")

enemy = "enemy"
friendly = "friendly"

ACTIONS = ["F", "B", "L","R", "S"]


dqn_solver_friendly = DQN()
dqn_solver_enemy = DQN()

state_enemy, state_friendly = env.reset()

print(state_enemy)
print(state_friendly)

reward_friendly = 0.0
reward_enemy = 0.0



for i in range(1,100000000000001):

    done = False

    #done ook meegeven?

    initial_input_enemy = []

    initial_input_enemy.append(state_enemy)
    initial_input_enemy.append(state_friendly)
    initial_input_enemy.append(reward_enemy)

    initial_input_friendly = []

    initial_input_friendly.append(state_enemy)
    initial_input_friendly.append(state_friendly)
    initial_input_friendly.append(reward_friendly)

    input_array_enemy = np.asarray(initial_input_enemy)

    input_array_friendly = np.asarray(initial_input_friendly)

    step = 0

    while done == False:

        if(step %2 ==0):


            action = dqn_solver_enemy.act(input_array_enemy)

            action_code = ACTIONS[action]

            state_next_enemy, state_friendly, reward_enemy, reward_friendly, done, info_enemy, info_friendly = env.step(action_code, enemy)

            env.render()

            input_next_enemy = []
            input_next_enemy.append(state_next_enemy)
            input_next_enemy.append(state_friendly)
            input_next_enemy.append(reward_enemy)

            input_array_next_enemy = np.asarray(input_next_enemy)
            print(input_array_next_enemy)

            dqn_solver_enemy.remember(input_array_enemy, action, reward_enemy, input_array_next_enemy, done)

            input_array_enemy = input_array_next_enemy

            print("Game: " + str(i) + ", exploration: " + str(dqn_solver_enemy.exploration_rate) + ", score: " + str("nog niet geimplementeerd"))


            dqn_solver_enemy.experience_replay()


        else:
            pass
            #
            #
            # action = dqn_solver_enemy.act(input_array_friendly)
            #
            # action_code = ACTIONS[action]
            #
            # state_enemy, state_next_friendly, reward_enemy, reward_friendly, done, info_enemy, info_friendly = env.step(
            #     action_code, friendly)
            #
            # env.render()
            #
            # input_next_friendly = []
            # input_next_friendly.append(state_next_friendly)
            # input_next_friendly.append(state_enemy)
            # input_next_friendly.append(reward_friendly)
            #
            # input_array_next_friendly = np.asarray(input_next_friendly)
            #
            # dqn_solver_friendly.remember(input_array_friendly, action, reward_enemy, input_array_next_friendly, done)
            #
            # input_array_friendly = input_array_next_friendly
            #
            # print("Game: " + str(i) + ", exploration: " + str(dqn_solver_enemy.exploration_rate) + ", score: " + str(
            #     "nog niet geimplementeerd"))
            #
            # dqn_solver_friendly.experience_replay()

        time.sleep(0.1)
        step +=1
        print(step)

    env.reset()
    env.render()
    time.sleep(3)
