import gym
import roomba_env
from xmlrpc.server import SimpleXMLRPCServer

env = gym.make('roomba-v0')

if __name__ == "__main__":


    try:


        with SimpleXMLRPCServer(('', 8080), allow_none=True) as server:
            server.register_introspection_functions()
            server.register_multicall_functions()

            server.register_instance(env)
            server.serve_forever()


    except KeyboardInterrupt:
        print("Bye")
    except Exception as e:
        print(e)
    finally:

        env.close()
