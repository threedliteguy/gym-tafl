import gym
import random


class RandomAgentWithRules(object):


    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        #print(observation['pieces'])
        valids = observation['validMoves']
        valids = list(map(lambda y: y.tolist(), list(filter(lambda x: sum(x)>0, valids))))
        #print('validMoves=',valids)

        chosen = random.choice(valids)

        action = { "from_location": chosen[0:2], "to_location": chosen[2:4] }
        
        return action

