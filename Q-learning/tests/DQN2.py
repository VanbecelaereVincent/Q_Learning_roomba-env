import gym
import roomba_env

import time

import random, numpy, math

from keras.models import Sequential
from keras.layers import *
from keras.optimizers import *

class Model:
    def __init__(self, stateCnt, actionCnt):

        self.stateCnt = stateCnt
        self.actionCnt = actionCnt

        self.model = self._createModel()
        # self.model.load_weights("cartpole-basic.h5")

    def _createModel(self):
        self.model = Sequential()
        self.model.add(Dense(24, input_shape=(5,), activation="relu"))
        self.model.add(Dense(24, activation="relu"))
        self.model.add(Dense(5, activation="softmax"))
        self.model.compile(loss="mse", optimizer=Adam(lr=0.00025))

        return self.model

    def train(self, x, y, epoch=1, verbose=0):
        self.model.fit(x, y, batch_size=64, nb_epoch=epoch, verbose=verbose)

    def predict(self, s):
        return self.model.predict(s)

    def predictOne(self, s):
        return self.predict(s.reshape(1, self.stateCnt)).flatten()



class Memory:   # stored as ( s, a, r, s_ )
    samples = []

    def __init__(self, capacity):
        self.capacity = capacity

    def add(self, sample):
        self.samples.append(sample)

        if len(self.samples) > self.capacity:
            self.samples.pop(0)

    def sample(self, n):
        n = min(n, len(self.samples))
        return random.sample(self.samples, n)


MEMORY_CAPACITY = 100000
BATCH_SIZE = 64

GAMMA = 0.99

#exploration rate
MAX_EPSILON = 1
MIN_EPSILON = 0.01

LAMBDA = 0.001  # speed of decay


class Agent:
    steps = 0
    epsilon = MAX_EPSILON

    def __init__(self, stateCnt, actionCnt):
        self.stateCnt = stateCnt
        self.actionCnt = actionCnt

        self.brain = Model(stateCnt, actionCnt)
        self.memory = Memory(MEMORY_CAPACITY)

    def act(self, s):
        if random.random() < self.epsilon:
            return random.randint(0, self.actionCnt - 1)
        else:
            return numpy.argmax(self.brain.predictOne(s))

    def observe(self, sample):  # in (s, a, r, s_) format
        self.memory.add(sample)

        # slowly decrease Epsilon based on our experience
        self.steps += 1
        self.epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * math.exp(-LAMBDA * self.steps)

    def replay(self):
        batch = self.memory.sample(BATCH_SIZE)
        print(batch)
        batchLen = len(batch)

        no_state = numpy.zeros(self.stateCnt)

        states = numpy.array([o for o in batch])
        print(states)
        states_ = numpy.array([no_state if o is None else o for o in batch])
        print(states_)
        p = self.brain.predict(states)
        p_ = self.brain.predict(states_)

        x = numpy.zeros((batchLen, self.stateCnt))
        y = numpy.zeros((batchLen, self.actionCnt))

        for i in range(batchLen):
            o = batch[i]
            print(i)
            s = o[0]
            a = o[1]
            r = o[2]
            s_ = o[3]

            t = p[i]
            print(t)
            if s_ is None:
                t[a] = r
            else:
                t[a] = r + GAMMA * numpy.amax(p_[i])

            x[i] = s
            y[i] = t

        self.brain.train(x, y)





env = gym.make('roomba-v0')

ACTIONS = ["F", "B", "L", "R", "S"]

enemy = "enemy"
reward_enemy = 0.0

friendly = "friendly"
reward_friendly = 0.0

state_enemy, state_friendly = env.reset()


agent_enemy = Agent(5,5)
agent_friendly = Agent(5,5)

for i in range(1,100000000000001):

    done = False

    step = 0

    initial_input_enemy = []

    initial_input_enemy.append(state_enemy[0])
    initial_input_enemy.append(state_enemy[1])
    initial_input_enemy.append(state_friendly[0])
    initial_input_enemy.append(state_friendly[1])
    initial_input_enemy.append(reward_enemy)
    input_array_enemy = np.asarray(initial_input_enemy)

    initial_input_friendly = []

    initial_input_friendly.append(state_enemy[0])
    initial_input_friendly.append(state_enemy[1])
    initial_input_friendly.append(state_friendly[0])
    initial_input_friendly.append(state_friendly[1])
    initial_input_friendly.append(reward_friendly)
    input_array_friendly = np.asarray(initial_input_friendly)

    while done == False:

        if(step %2 ==0):



            action = agent_enemy.act(input_array_enemy)

            action_code = ACTIONS[action]

            state_next_enemy, state_friendly, reward_enemy, reward_friendly, done, info_enemy, info_friendly = env.step(action_code, enemy)

            env.render()

            #klopt dit?!
            agent_enemy.observe([state_next_enemy[0],state_next_enemy[1], state_friendly[0], state_friendly[1], reward_enemy])
            agent_enemy.replay()

            input_next_enemy = []
            input_next_enemy.append(state_next_enemy[0])
            input_next_enemy.append(state_next_enemy[1])
            input_next_enemy.append(state_friendly[0])
            input_next_enemy.append(state_friendly[1])
            input_next_enemy.append(reward_enemy)

            input_array_next_enemy = np.asarray(input_next_enemy)
            print(input_array_next_enemy)


            input_array_enemy = input_array_next_enemy



            # print("Game: " + str(i) + ", exploration: " + str(dqn_solver_enemy.exploration_rate) + ", score: " + str("nog niet geimplementeerd"))


        else:
            action = agent_enemy.act(input_array_friendly)

            action_code = ACTIONS[action]

            state, state_next_friendly, reward_enemy, reward_friendly, done, info_enemy, info_friendly = env.step(
                action_code, friendly)

            env.render()

            agent_enemy.observe((input_array_friendly[0], action, reward_friendly, state_next_friendly))
            agent_enemy.replay()

            input_next_friendly = []
            input_next_friendly.append(state_next_friendly[0])
            input_next_friendly.append(state_next_friendly[1])
            input_next_friendly.append(state_enemy[0])
            input_next_friendly.append(state_enemy[1])
            input_next_friendly.append(reward_friendly)

            input_array_next_friendly = np.asarray(input_next_friendly)

            input_array_friendly = input_array_next_friendly





        time.sleep(0.1)
        step +=1
        print(step)

    env.reset()
    env.render()
    time.sleep(3)




