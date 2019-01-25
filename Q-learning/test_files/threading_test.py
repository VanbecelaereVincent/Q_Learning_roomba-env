import threading
import gym
import roomba_env
import time


class Agent(threading.Thread):

    def __init__(self, step, agent):

        threading.Thread.__init__(self)
        self.step = step
        self.agent = agent



    def run(self):
        # Get lock to synchronize threads
        print("{0} started".format(self.agent))

        #globale variabele, threads hadden niet altijd allebij door dat het spel gedaan was (bij het botsen)
        global done

        for i in range(1,100):

            time.sleep(1)

            done = False

            #enemy krijgt reward van - 100 niet


            while done == False:
                action = env.action_space_sample(self.agent)
                print("-----------------{0}------------".format(self.agent))
                print("chosen action: {}".format(action))

                state, reward, done, info = env.step(action, self.agent)
                print("info: {0}".format(info))
                print("Reward: {0}".format(reward))
                time.sleep(0.1)
            print("---------------------RESET: {0}----------------------------".format(self.agent))
            env.reset()
            print("-----------------------------NEW GAME: {0}-----------------------------".format(i))


if __name__ == "__main__":

    try:

        lock = threading.Lock()

        threads = []

        env = gym.make('roomba-v0')


        print(env.action_space())


        thread_enemy = Agent("F", "enemy")
        threads.append(thread_enemy)

        thread_friendly = Agent("F", "friendly")
        threads.append(thread_friendly)

        # thread_renderer = Renderer("renderer", env)
        # threads.append(thread_renderer)

        for thread in threads:
            thread.start()


        #probleem was hier dat ik voor één of andere reden vanuit een subthread mijn env niet kon renderen (oproepen env.render() gaf error)
        #dus maar zo opgelost dat zolang de agents aan het rijden zijn (en dus de threads alive zijn) ik render

        #op de achtergrond doet hij het wel nog pixel per pixel, maar ik check daar nog niet voor botsingen

        #zou het eigenlijk echt moeten kunnen renderen vanuit de thread

        while threads[0].isAlive() or threads[1].isAlive():
            env.render()

        for thread in threads:
            thread.join()


        #altijd een close nodig of je krijgt een error bij het renderen
        env.close()

    except Exception as ex:

        print(ex)

    finally:

        print("bye")