import sys
import gym
import random


class HumanAgentWithRules(object):

    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):

        print(observation['pieces'])
        valids = observation['validMoves']
        valids = list(map(lambda y: y.tolist(), list(filter(lambda x: sum(x)>0, valids))))
        print('validMoves=',valids)
        
        action = None
        while True:
            move = input("Enter move as x1,y1,x2,y2: ")
            try:
               move = list(map(lambda x: int(x.strip()), move.split(',')))
            except:
               print("Invalid input.", sys.exc_info()[0])

            if move in valids: break
            print("Invalid move.")
                                                    
        action = { "from_location": move[0:2], "to_location": move[2:4] }
        
        return action

