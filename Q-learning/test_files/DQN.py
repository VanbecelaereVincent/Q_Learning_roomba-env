from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import random
import numpy as np
import sys

GAMMA = 0.95
LEARNING_RATE = 0.001

MEMORY_SIZE = sys.maxsize
BATCH_SIZE = 20

EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.01
EXPLORATION_DECAY = 0.995

class DQN():


    #observation space van mij is:
    # positie friendly
    # positie enemy
    # afstand groen tot aan de lijn (?)
    # reward (?)

    def __init__(self):

        self.exploration_rate = EXPLORATION_MAX

        self.memory = deque(maxlen=MEMORY_SIZE)

        self.model = Sequential()
        self.model.add(Dense(24, input_shape=(3,), activation="relu"))
        self.model.add(Dense(24, activation="relu"))
        self.model.add(Dense(5, activation="softmax"))
        self.model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() < self.exploration_rate:
            return random.randrange(5)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def experience_replay(self):

        #mag maar beginnen experience trainen als we effectief een dataset hebben die groter is dan de batchsize
        if len(self.memory) < BATCH_SIZE:
            return

        #batch ophalen uit mijn gespeelde moves
        batch = random.sample(self.memory, BATCH_SIZE)

        print((batch))

        for state, action, reward, state_next, done in batch:
            print(state_next)
            print(state)
            print(action)
            print(reward)
            print(done)
            q_update = reward
            if not done:
                q_update = (reward + GAMMA * np.amax(self.model.predict(state_next)))
            q_values = self.model.predict(np.asarray(state))
            q_values[0][action] = q_update
            self.model.fit(np.asarray(state), q_values, verbose=0)
        self.exploration_rate *= EXPLORATION_DECAY
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)


    def save_model(self):

        pass