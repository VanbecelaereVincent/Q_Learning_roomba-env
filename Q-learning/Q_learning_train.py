import gym
import roomba_env
import numpy as np
import pandas as pd
from random import choice
import time

num_states = 11*11
num_actions = 5

FORWARD = 0
BACKWARDS = 1
LEFT = 2
RIGHT = 3
STAY = 4

actions = ['F', 'B', 'L', 'R', 'S']

def egreedy_policy(q_values, state_enemy, state_friendly, agent, epsilon=0.1):

    actions = env.legal_actions(agent)

    if np.random.random() < epsilon:
        # print(choice(actions))
        return choice(actions)
    else:
        # print("--------------------")
        # print("hier")

        highest_q_action = np.argmax(q_values[state_enemy][state_friendly])

        if(highest_q_action not in actions):
            print("was niet in actions")
            return choice(actions)

        else:
            return highest_q_action


def q_learning(env, render, agent_to_train, num_episodes=500, exploration_rate=0.2,
               learning_rate=0.5, gamma=0.9):
    q_values_enemy = np.zeros((num_states,num_states, num_actions))
    q_values_friendly = np.zeros((num_states, num_states, num_actions))

    ep_rewards_enemy = []
    ep_rewards_friendly = []

    if(agent_to_train == "enemy"):
        for _ in range(num_episodes):
            state_enemy, state_friendly = env.reset()
            print("Episode nmbr: {0}".format(_))

            done = False

            reward_sum_enemy = 0
            reward_sum_friendly = 0

            index = 0



            while not done:

                # ENEMY
                if (index % 2 == 0):
                    # print("enemy")
                    # Choose action
                    action = egreedy_policy(q_values_enemy, state_enemy, state_friendly, "enemy", exploration_rate)
                    action_id = actions[action]
                    # print(action_id)
                    # Do the action
                    next_state_enemy, reward_enemy, state_friendly, done, info = env.step(action_id, "enemy", render)
                    reward_sum_enemy += reward_enemy
                    # Update q_values
                    td_target = reward_enemy + 0.9 * np.max(q_values_enemy[next_state_enemy][state_friendly])
                    td_error = td_target - q_values_enemy[state_enemy][state_friendly][action]
                    q_values_enemy[state_enemy][state_friendly][action] += learning_rate * td_error
                    # Update state
                    state_enemy = next_state_enemy

                # FRIENDLY
                else:
                    legal = env.legal_actions("friendly")
                    action = choice(legal)
                    # Do the action
                    action_id = actions[action]
                    next_state_friendly, reward_friendly, state_enemy, done, info = env.step(action_id, "friendly",
                                                                                             render)

                    # Update state and action
                    state_friendly = next_state_friendly

                index += 1
                # print(q_values_enemy)
            ep_rewards_enemy.append(reward_sum_enemy)
            ep_rewards_friendly.append(reward_sum_friendly)

        return ep_rewards_enemy, q_values_enemy

    elif(agent_to_train == "friendly"):

        for _ in range(num_episodes):
            state_enemy, state_friendly = env.reset()
            print("Episode nmbr: {0}".format(_))
            done = False

            reward_sum_enemy = 0
            reward_sum_friendly = 0

            index = 0



            while not done:

                # ENEMY
                if (index % 2 == 0):

                    legal = env.legal_actions("enemy")
                    action = choice(legal)
                    # Do the action
                    action_id = actions[action]
                    next_state_enemy, reward_friendly, state_friendly, done, info = env.step(action_id, "enemy", render)

                    # Update state and action
                    state_enemy = next_state_enemy

                # FRIENDLY
                else:
                    # print("friendly")
                    # Choose action
                    action = egreedy_policy(q_values_friendly, state_enemy, state_friendly, "friendly",
                                            exploration_rate)
                    # Do the action
                    action_id = actions[action]
                    # print(action_id)
                    next_state_friendly, reward_friendly, state_enemy, done, info = env.step(action_id, "friendly",
                                                                                             render)
                    reward_sum_friendly += reward_friendly
                    # Update q_values
                    td_target = reward_friendly + 0.9 * np.max(q_values_friendly[state_enemy][next_state_friendly])
                    td_error = td_target - q_values_friendly[state_enemy][state_friendly][action]
                    q_values_friendly[state_enemy][state_friendly][action] += learning_rate * td_error
                    # Update state
                    state_friendly = next_state_friendly

                index += 1
                # print(q_values_enemy)
            ep_rewards_enemy.append(reward_sum_enemy)
            ep_rewards_friendly.append(reward_sum_friendly)

        return ep_rewards_friendly, q_values_friendly

    else:
        pass


def write_to_file(numpy_array, file_name):


    with open(file_name, 'w') as outfile:

        outfile.write('# Array shape: {0}\n'.format(numpy_array.shape))


        for data_slice in numpy_array:

            np.savetxt(outfile, data_slice, fmt='%-7.2f')


            outfile.write('# New slice\n')


def read_file(filename):
    new_data = np.loadtxt(filename)
    new_data = new_data.reshape((121, 121, 5))
    return new_data



#TRAINEN

env = gym.make('roomba-v0')
#
q_learning_rewards_enemy, q_values_enemy = q_learning(env, False, "enemy", 2000000, gamma=0.9, learning_rate=.8)
q_learning_rewards_friendly, q_values_friendly = q_learning(env, False, "friendly", 2000000, gamma=0.0, learning_rate=.8)

write_to_file(q_values_enemy, 'Q_enemy10_meer_episodes.txt')
write_to_file(q_values_friendly, 'Q_friendly10_meer_episodes.txt')

#
# np.savetxt("Q_rewards_enemy.csv", np.asarray(q_learning_rewards_enemy), delimiter=",")
# np.savetxt("Q_rewards_friendly.csv", np.asarray(q_learning_rewards_friendly), delimiter=",")



env.close()





