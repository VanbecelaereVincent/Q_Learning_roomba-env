import datetime
from math import sqrt
from logging import log
from random import choice
import random
import gym
import roomba_env

#kan ik die board klassee niet vervangen door mijn environment?
#eens kijken hoe ik dit ga fixen dat ze elk om beurt doen

# class Board(object):
#
#     def __init__(self):
#
#
#         player_enemy = "enemy"
#         player_friendly = "friendly"
#         current_player = ""
#
#         self.state_enemy = []
#         self.state_friendly = []
#
#     def start(self):
#
#         start = {"enemy": [350,350], "friendly": [350,100]}
#
#     def current_player(self, state):
#         # Takes the game state and returns the current player's
#         # number.
#         pass
#
#     def next_state(self, state, play):
#         # Takes the game state, and the move to be applied.
#         # Returns the new game state.
#         pass
#
#     def legal_plays(self, state_history):
#
#         if (self.current_player == "enemy"):
#
#             # makes sure agents can't leave the environment
#
#             if (self.state_enemy[1] == 100 and self.state_enemy[0] != 100 and self.state_enemy[0] != 600):
#                 self.ACTION_ENEMY = ["F", "L", "R", "S"]
#                 self.info_enemy = [self.ACTION_ENEMY, "beneden"]
#                 number = random.randint(0, 3)
#                 return self.ACTION_ENEMY[number]
#
#             elif (self.state_enemy[1] == 600 and self.state_enemy[0] != 100 and self.state_enemy[0] != 600):
#
#                 self.ACTION_ENEMY = ["B", "R", "L", "S"]
#                 self.info_enemy = [self.ACTION_ENEMY, "boven"]
#                 number = random.randint(0, 3)
#                 return self.ACTION_ENEMY[number]
#
#             elif (self.state_enemy[0] == 100 and self.state_enemy[1] != 100 and self.state_enemy[1] != 600):
#                 self.ACTION_ENEMY = ["F", "B", "R", "S"]
#                 self.info_enemy = [self.ACTION_ENEMY, "links"]
#                 number = random.randint(0, 3)
#                 return self.ACTION_ENEMY[number]
#
#             elif (self.state_enemy[0] == 600 and self.state_enemy[1] != 100 and self.state_enemy[1] != 600):
#                 self.ACTION_ENEMY = ["F", "B", "L", "S"]
#                 self.info_enemy = [self.ACTION_ENEMY, "rechts"]
#                 number = random.randint(0, 3)
#                 return self.ACTION_ENEMY[number]
#
#
#             elif (self.state_enemy == [100, 100]):
#
#                 self.ACTION_ENEMY = ["F", "R", "S"]
#                 self.info_enemy = [self.ACTION_ENEMY, "benedenlinks"]
#                 number = random.randint(0, 2)
#                 return self.ACTION_ENEMY[number]
#
#             elif (self.state_enemy == [100, 600]):
#
#                 self.ACTION_ENEMY = ["B", "R", "S"]
#                 self.info_enemy = [self.ACTION_ENEMY, "bovenlinks"]
#                 number = random.randint(0, 2)
#                 return self.ACTION_ENEMY[number]
#
#
#             elif (self.state_enemy == [600, 100]):
#
#                 self.ACTION_ENEMY = ["F", "L", "S"]
#                 self.info_enemy = [self.ACTION_ENEMY, "benedenrechts"]
#                 number = random.randint(0, 2)
#                 return self.ACTION_ENEMY[number]
#
#             elif (self.state_enemy == [600, 600]):
#                 self.ACTION_ENEMY = ["B", "L", "S"]
#                 self.info_enemy = [self.ACTION_ENEMY, "bovenrechts"]
#                 number = random.randint(0, 2)
#                 return self.ACTION_ENEMY[number]
#
#             else:
#                 self.ACTION_ENEMY = ["F", "B", "L", "R", "S"]
#                 self.info_enemy = [self.ACTION_ENEMY, "niet speciaal"]
#                 number = random.randint(0, 4)
#                 return self.ACTION_ENEMY[number]
#
#         if (self.current_player == "friendly"):
#
#             if (self.state_friendly[1] == 100 and self.state_friendly[0] != 100 and self.state_friendly[0] != 600):
#                 self.ACTION_FRIENDLY = ["F", "L", "R", "S"]
#                 self.info_friendly = [self.ACTION_FRIENDLY, "beneden"]
#                 number = random.randint(0, 3)
#                 return self.ACTION_FRIENDLY[number]
#
#             elif (self.state_friendly[1] == 600 and self.state_friendly[0] != 100 and self.state_friendly[0] != 600):
#
#                 self.ACTION_FRIENDLY = ["B", "R", "L", "S"]
#                 self.info_friendly = [self.ACTION_FRIENDLY, "boven"]
#                 number = random.randint(0, 3)
#                 return self.ACTION_FRIENDLY[number]
#
#             elif (self.state_friendly[0] == 100 and self.state_friendly[1] != 100 and self.state_friendly[1] != 600):
#                 self.ACTION_FRIENDLY = ["F", "B", "R", "S"]
#                 self.info_friendly = [self.ACTION_FRIENDLY, "links"]
#                 number = random.randint(0, 3)
#                 return self.ACTION_FRIENDLY[number]
#
#             elif (self.state_friendly[0] == 600 and self.state_friendly[1] != 100 and self.state_friendly[1] != 600):
#                 self.ACTION_FRIENDLY = ["F", "B", "L", "S"]
#                 self.info_friendly = [self.ACTION_FRIENDLY, "rechts"]
#                 number = random.randint(0, 3)
#                 return self.ACTION_FRIENDLY[number]
#
#
#             elif (self.state_friendly == [100, 100]):
#
#                 self.ACTION_FRIENDLY = ["F", "R", "S"]
#                 self.info_friendly = [self.ACTION_FRIENDLY, "benedenlinks"]
#                 number = random.randint(0, 2)
#                 return self.ACTION_FRIENDLY[number]
#
#             elif (self.state_friendly == [100, 600]):
#
#                 self.ACTION_FRIENDLY = ["B", "R", "S"]
#                 self.info_friendly = [self.ACTION_FRIENDLY, "bovenlinks"]
#                 number = random.randint(0, 2)
#                 return self.ACTION_FRIENDLY[number]
#
#
#             elif (self.state_friendly == [600, 100]):
#
#                 self.ACTION_FRIENDLY = ["F", "L", "S"]
#                 self.info_friendly = [self.ACTION_FRIENDLY, "benedenrechts"]
#                 number = random.randint(0, 2)
#                 return self.ACTION_FRIENDLY[number]
#
#             elif (self.state_friendly == [600, 600]):
#                 self.ACTION_FRIENDLY = ["B", "L", "S"]
#                 self.info_friendly = [self.ACTION_FRIENDLY, "bovenrechts"]
#                 number = random.randint(0, 2)
#                 return self.ACTION_FRIENDLY[number]
#
#             else:
#                 self.ACTION_FRIENDLY = ["F", "B", "L", "R", "S"]
#                 self.info_friendly = [self.ACTION_FRIENDLY, "niet speciaal"]
#                 number = random.randint(0, 4)
#                 return self.ACTION_FRIENDLY[number]
#
#     def winner(self, state_history):
#         # Takes a sequence of game states representing the full
#         # game history.  If the game is now won, return the player
#         # number.  If the game is still ongoing, return zero.  If
#         # the game is tied, return a different distinct value, e.g. -1.
#         pass


#hoe sla ik mijn boom op?
#kan ik alletwee mijn roombas tegelijk trainen?
#maak ik ook een versie dat jij tegen de bot kan spelen?

class MonteCarlo(object):
    def __init__(self, env, **kwargs):
        self.env = env
        self.C = kwargs.get('C', 1.4)
        self.states = [[(350,100),(350,350)]]
        self.wins = {}
        self.plays = {}
        self.max_moves = kwargs.get('max_moves', 100)
        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)

    def update(self, state):
        self.states.append(state)

    def get_play(self):

        self.max_depth = 0
        state = self.states[-1]

        #in mijn env ergens ophalen welke speler er aan zet is
        player = self.env.current_player()

        #dit kan ik uit mijn env opvragen
        legal = self.env.legal_plays()

        # Bail out early if there is no real choice to be made.
        if not legal:
            return
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        moves_states = [(p, self.env.step(p)) for p in legal]
        print(moves_states)

        # Display the number of calls of `run_simulation` and the
        # time elapsed.

        print(games, datetime.datetime.utcnow() - begin)

        # Pick the move with the highest percentage of wins.
        percent_wins, move = max(
            (self.wins.get((player, S), 0) /
             self.plays.get((player, S), 1),
             p)
            for p, S in moves_states
        )

        # Display the stats for each possible play.
        for x in sorted(
                ((100 * self.wins.get((player, S), 0) /
                  self.plays.get((player, S), 1),
                  self.wins.get((player, S), 0),
                  self.plays.get((player, S), 0), p)
                 for p, S in moves_states),
                reverse=True
        ):
            print("{3}: {0:.2f}% ({1} / {2})".format(*x))

        print("Maximum depth searched:", self.max_depth)

        return move

    def run_simulation(self):
        # A bit of an optimization here, so we have a local
        # variable lookup instead of an attribute access each loop.
        plays, wins = self.plays, self.wins

        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = self.env.current_player()

        expand = True
        for t in range(1, self.max_moves + 1):
            legal = self.env.legal_plays()

            moves_states = [(p, self.env.step(p)) for p in legal]

            if all(plays.get((player, S)) for p, S in moves_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = log(
                    sum(plays[(player, S)] for p, S in moves_states),"msg")
                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.C * sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                # Otherwise, just make an arbitrary decision.
                move, state = choice(moves_states)

            states_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, state) not in plays:
                expand = False
                plays[(player, state)] = 0
                wins[(player, state)] = 0
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, state))

            player = self.env.current_player()
            winner = self.env.winner()
            if winner:
                break

        for player, state in visited_states:
            if (player, state) not in plays:
                continue
            plays[(player, state)] += 1
            if player == winner:
                wins[(player, state)] += 1




env  = gym.make("roomba-v0")
# print(env.current_player)
# env.reset()
monte = MonteCarlo(env)


for i in range(1,100000):
    monte.get_play()
    env.render()