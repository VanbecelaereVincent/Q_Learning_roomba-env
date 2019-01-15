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

def egreedy_policy_play(q_values, state_enemy, state_friendly, agent, epsilon=0.1):

    print("------------Agent:{0}------------".format(agent))
    actions = env.legal_actions(agent)
    print(actions)

    if np.random.random() < epsilon:

        return choice(actions)
    else:


        y = q_values[state_enemy][state_friendly]

        print("Q_values: {0}".format(y))
        # highest_q_action = np.where((np.array(y) != 0).any(axis=0))[0].max()
        # print(highest_q_action)
        non_zero_indices = np.nonzero(y)
        k = np.argmax(y[non_zero_indices])
        original_indice = non_zero_indices[0][k]
        highest_q_action = original_indice
        print("gekozen actie: {0}".format(highest_q_action))

        if(highest_q_action not in actions):
            print("dit kan niet maar gebeurt toch")
            print("----------------------------")

            return choice(actions)

        else:
            print("----------------------------")
            return highest_q_action


def q_learning(env, render, num_episodes=500, exploration_rate=0.1,
               learning_rate=0.5, gamma=0.9):
    q_values_enemy = np.zeros((num_states,num_states, num_actions))
    q_values_friendly = np.zeros((num_states, num_states, num_actions))

    ep_rewards_enemy = []
    ep_rewards_friendly = []

    for _ in range(num_episodes):
        state_enemy, state_friendly = env.reset()
        print("Episode nmbr: {0}".format(_))
        done = False

        reward_sum_enemy = 0
        reward_sum_friendly = 0

        index = 0

        #volgens mij krijgt er nog steeds maar één van de twee de +- 100 binnen, nog eens goed bekijken morgen!
        #als hij dit niet meegeeft: gaat groen nooit leren dat rood op hem wil stappen
        #en gaat rood nooit leren dat groen de overkant wil halen

        #de afstand tot rood meegeven aan groen?
        #en waarom niet de afstand van groen tot de eindmeet aan rood?

        while not done:


            #ENEMY
            if(index%2 == 0):
                # print("enemy")
                # Choose action
                action = egreedy_policy(q_values_enemy, state_enemy, state_friendly, "enemy", exploration_rate,)
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

            #FRIENDLY
            else:
                # print("friendly")
                # Choose action
                action = egreedy_policy(q_values_friendly, state_enemy, state_friendly, "friendly", exploration_rate)
                # Do the action
                action_id = actions[action]
                # print(action_id)
                next_state_friendly, reward_friendly, state_enemy, done, info = env.step(action_id, "friendly", render)
                reward_sum_friendly += reward_friendly
                # Update q_values
                td_target = reward_friendly + 0.9 * np.max(q_values_friendly[state_enemy][next_state_friendly])
                td_error = td_target - q_values_friendly[state_enemy][state_friendly][action]
                q_values_friendly[state_enemy][state_friendly][action] += learning_rate * td_error
                # Update state
                state_friendly = next_state_friendly

            index +=1
            # print(q_values_enemy)
        ep_rewards_enemy.append(reward_sum_enemy)
        ep_rewards_friendly.append(reward_sum_friendly)


    return ep_rewards_enemy, q_values_enemy, ep_rewards_friendly, q_values_friendly

def write_to_file(numpy_array, file_name):

    # Write the array to disk
    with open(file_name, 'w') as outfile:
        # I'm writing a header here just for the sake of readability
        # Any line starting with "#" will be ignored by numpy.loadtxt
        outfile.write('# Array shape: {0}\n'.format(numpy_array.shape))

        # Iterating through a ndimensional array produces slices along
        # the last axis. This is equivalent to data[i,:,:] in this case
        for data_slice in numpy_array:
            # The formatting string indicates that I'm writing out
            # the values in left-justified columns 7 characters in width
            # with 2 decimal places.
            np.savetxt(outfile, data_slice, fmt='%-7.2f')

            # Writing out a break to indicate different slices...
            outfile.write('# New slice\n')


def read_file(filename):
    new_data = np.loadtxt(filename)
    new_data = new_data.reshape((121, 121, 5))
    return new_data


# # SPELEN
# # deze functie kan ik dan veranderen zotdat je zelf kan kiezen of je de enemy wil zijn of de friendly en ook eens gewoon tonen hoe ze spelen tegen elkaar
def play(q_values_enemy, q_values_friendly, render):
    # env = gym.make('roomba-v0')
    state_enemy, state_friendly = env.reset()
    print(state_enemy, state_friendly)
    done = False

    index = 0

    while not done:

        if(index %2 == 0):


            # Select action
            action = egreedy_policy_play(q_values_enemy, state_enemy, state_friendly, "enemy", 0.0)
            # Do the action
            action_id = actions[action]
            next_state_enemy, reward_enemy, state_friendly, done, info = env.step(action_id, "enemy", render)

            # Update state and action
            state_enemy = next_state_enemy

        else:

            # Select action
            action = egreedy_policy_play(q_values_friendly, state_enemy, state_friendly, "friendly", 0.0)
            # Do the action
            action_id = actions[action]
            next_state_friendly, reward_friendly, state_enemy, done, info = env.step(action_id, "friendly", render)

            # Update state and action
            state_friendly = next_state_friendly

        index +=1

    env.close()

#TRAINEN

env = gym.make('roomba-v0')
#
# q_learning_rewards_enemy, q_values_enemy, q_learning_rewards_friendly, q_values_friendly = q_learning(env, False, 5000000, gamma=0.9, learning_rate=1)
#
# write_to_file(q_values_enemy, 'Q_enemy2.txt')
# write_to_file(q_values_friendly, 'Q_friendly2.txt')

#
# np.savetxt("Q_enemy.csv", q_values_enemy, delimiter=",")
# np.savetxt("Q_friendly.csv", q_values_friendly, delimiter=",")
#
# np.savetxt("Q_rewards_enemy.csv", np.asarray(q_learning_rewards_enemy), delimiter=",")
# np.savetxt("Q_rewards_friendly.csv", np.asarray(q_learning_rewards_friendly), delimiter=",")

# q_values_enemy = read_file("Q_enemy.txt")
# q_values_friendly = read_file("Q_friendly.txt")
#
# play(q_values_enemy, q_values_friendly, render=True)


env.close()

#mss eens gewoon gestoord lang laten runnen maar wel iedere keer mijn Q values opslaan (na zoveel tijd nen save van die waarden)!
#en meerdere reward functies maken en laten runnen bv
# da gaat wa vlotter werken zijn



