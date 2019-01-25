import numpy as np
import gym
import roomba_env
from random import choice

def read_file(filename):
    new_data = np.loadtxt(filename)
    new_data = new_data.reshape((121, 121, 5))
    return new_data

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

def play(q_values_enemy, q_values_friendly, render, agent_to_play):

    state_enemy, state_friendly = env.reset()
    print(state_enemy, state_friendly)
    done = False

    index = 0

    if(agent_to_play == "enemy"):

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

                legal = env.legal_actions("friendly")
                action = choice(legal)
                # Do the action
                action_id = actions[action]
                next_state_friendly, reward_friendly, state_enemy, done, info = env.step(action_id, "friendly", render)

                # Update state and action
                state_friendly = next_state_friendly

            index +=1

    elif(agent_to_play =="friendly"):

        while not done:

            if (index % 2 == 0):

                legal = env.legal_actions("enemy")
                action = choice(legal)
                # Do the action
                action_id = actions[action]
                next_state_enemy, reward_friendly, state_friendly, done, info = env.step(action_id, "enemy", render)

                # Update state and action
                state_enemy = next_state_enemy

            else:

                # Select action
                action = egreedy_policy_play(q_values_friendly, state_enemy, state_friendly, "friendly", 0.0)
                # Do the action
                action_id = actions[action]
                next_state_friendly, reward_enemy, state_enemy, done, info = env.step(action_id, "friendly", render)

                # Update state and action
                state_friendly = next_state_friendly

            index += 1
    else:

        pass

    env.close()

env = gym.make("roomba-v0")
actions = ["F","B","L","R","S"]

q_values_enemy = read_file("Q_enemy3.txt")
q_values_friendly = read_file("Q_friendly10_meer_episodes.txt")

play(q_values_enemy, q_values_friendly, True, "friendly")

env.close()