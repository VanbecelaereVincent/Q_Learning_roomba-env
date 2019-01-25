import time
import xmlrpc.client

RPC_SERVER = ""
RPC_PORT = 8080
AGENT = "friendly"


if __name__ == '__main__':

    try:

        env = xmlrpc.client.ServerProxy("http://{}:{}".format(RPC_SERVER, RPC_PORT))

        for i in range(1, 3):


            done = False

            while done == False:
                # env.render()
                action = env.action_space_sample(AGENT)
                print("-----------------{0}------------".format(AGENT))
                print("chosen action: {}".format(action))

                state, rewad, done, info = env.step(action, AGENT)
                print("info: {0}".format(info))
            print("---------------------RESET: {0}----------------------------".format(AGENT))
            env.reset()


    except KeyboardInterrupt:
        print("Bye")
    except Exception as e:
        print(e)
