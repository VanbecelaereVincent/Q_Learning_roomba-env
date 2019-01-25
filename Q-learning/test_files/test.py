import gym
import roomba_env
import time

index = 0

env = gym.make("roomba-v0")

#doen eerst een reset omdat dit de state van de twee roombas teruggeeft
env.reset()


env.render()

enemy = "enemy"
friendly = "friendly"




for i in range(1,1001):

    done = False

    print("-----------------GAME {0} STARTED-----------------".format(i))

    while done == False:


        if(index % 2 == 0):

            print("-----------------FRIENDLY-----------------")

            action = env.action_space_sample(friendly)

            print("Chosen action: {0}".format(action))

            state_friendly, reward_friendly, done, info_friendly = env.step(action, friendly)

            print("Reward: {0}".format(reward_friendly))




        else:

            print("-----------------ENEMY-----------------")

            action = env.action_space_sample(enemy)

            print("Chosen action enemy: {0}".format(action))

            state_enemy, reward_enemy, done, info_enemy = env.step(action, enemy)

            print("Reward enemy: {0}".format(reward_enemy))



        # time.sleep(1)
        index += 1

    print("-----------------GAME {0} ENDED-----------------".format(i))
    env.reset()
    env.render()
    time.sleep(3)


env.close()
