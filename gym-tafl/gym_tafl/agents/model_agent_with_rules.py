import gym
import random

import torch
from base_agent import BaseAgent
from gym_tafl.train.train import FFNet, Loader

class ModelAgentWithRules(BaseAgent):


    def __init__(self, modelfile, action_space, recordFile=None):
        super().__init__(action_space, recordFile)
        self.modelfile=modelfile
        self.piece_cats=[-1,0,1,2]
        self.loader = Loader()
        self.action_cats=None
        self.model=None

    def act(self, observation, reward, done):
        
        if done:
            super().recordAction(None, reward, done, None)
            return None

        valids = observation['validMoves']
        valids = list(map(lambda y: y.tolist(), list(filter(lambda x: sum(x)>0, valids))))

        chosen = self.selectUsingModel(observation['pieces'], observation['playerToMove'], valids)

        action = { "from_location": chosen[0:2], "to_location": chosen[2:4] }
        
        super().recordAction(observation, reward, done, action)        

        return action
 

    def selectUsingModel(self, pieces, playerToMove, valids):

       print(pieces)

       if self.action_cats == None:
           self.size = len(pieces)
           self.action_cats=[]
           for i in range(self.size): self.action_cats.append(i)

       best_reward = -10000
       best_index = -1
       obs_encoded = self.loader.encode_cats(self.piece_cats,pieces.ravel())
       obs_encoded = obs_encoded + [float(playerToMove)]
       for i,valid in enumerate(valids):
          x = obs_encoded + self.loader.encode_cats(self.action_cats, valid) 
          if self.model == None:
             input_row_length = len(x) 
             print('input_row_length',input_row_length)
             self.model = FFNet(input_row_length, self.modelfile)    
             self.model.load()
             self.model.eval()
          x = torch.tensor(x)
          y = self.model(x)
          
          #Print relative weights it has for moves
          #print(valid,y[0].item())
          
          if y > best_reward: 
              best_reward = y
              best_index = i

       return valids[best_index]       


