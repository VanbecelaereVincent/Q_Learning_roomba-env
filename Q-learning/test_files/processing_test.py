from multiprocessing import Process, Queue
import gym
import roomba_env


def agent(action, roomba, env):

    print("{0} started".format(roomba))

    index = 0
    while index <= 10:

        index += 1
        position = env.step(action, roomba)
        print("------------{0}---------------".format(roomba))
        print(position)

def renderer():

    while True:

        env.render()


if __name__ == "__main__":

    try:

        env = gym.make('roomba-v0')

        q = Queue()
        p_enemy = Process(target=agent, args=("F", "enemy", env))
        p_enemy.start()

        p_friendly = Process(target=agent,args=("F", "friendly", env))
        p_friendly.start()

        p_enemy.join()
        p_friendly.join()

        env.close()

    except Exception as ex:

        print(ex)

    finally:
        #altijd een close nodig of je krijgt een error bij het renderen
        print("bye")