import gym
import random

from base_agent import BaseAgent

class RandomAgentWithRules(BaseAgent):


    def __init__(self, action_space, recordFile=None):
        super().__init__(action_space, recordFile)

    def act(self, observation, reward, done):
        
        if done:
            super().recordAction(None, reward, done, None)
            return None

        valids = observation['validMoves']
        valids = list(map(lambda y: y.tolist(), list(filter(lambda x: sum(x)>0, valids))))

        chosen = random.choice(valids)

        action = { "from_location": chosen[0:2], "to_location": chosen[2:4] }
        
        super().recordAction(observation, reward, done, action)        

        return action
 
    def save(self):
        if (not self.recordFile is None):
           text_file = open(self.recordFile, "w")
           text_file.write('\n'.join(self.record))
           text_file.close()


     
