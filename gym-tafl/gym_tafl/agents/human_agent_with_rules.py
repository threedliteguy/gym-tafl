import sys
import gym
import random
from base_agent import BaseAgent


class HumanAgentWithRules(BaseAgent):

    def __init__(self, action_space, recordFile=None):
        super().__init__(action_space, recordFile)


    def act(self, observation, reward, done):
        
        if done: 
            return

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
        
        super().recordAction(observation, reward, done, action)

        return action

