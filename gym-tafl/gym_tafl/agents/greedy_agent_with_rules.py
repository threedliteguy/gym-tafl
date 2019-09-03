import gym
import random

from base_agent import BaseAgent

class GreedyAgentWithRules(BaseAgent):


    def __init__(self, action_space, recordFile=None):
        super().__init__(action_space, recordFile)

    def act(self, observation, reward, done):
        
        if done:
            super().recordAction(None, reward, done, None)
            return None

        valids = observation['validMoves']
        valids = list(map(lambda y: y.tolist(), list(filter(lambda x: sum(x)>0, valids))))

        pieces = observation['pieces']
        size=len(pieces)
        chosen = None

        caps = []
        for valid in valids:
            p = pieces[valid[1]][valid[0]]
            x = valid[2]
            y = valid[3]

            if p==2 and ( (x==0 and y==0) or (x==0 and y==size-1) or (x==size-1 and y==0) or (x==size-1 and y==size-1) ):
                    chosen=valid
                    break

            for dx in [-1,1]:
              try:
                  if pieces[y][x+dx]*p<0 and pieces[y][x+dx+dx]*p>0: 
                      caps.append(valid)
                      if pieces[y][x+dx]==2:
                          chosen=valid
              except:
                  pass

            for dy in [-1,1]:
              try:
                  if pieces[y+dy][x]*p<0 and pieces[y+dy+dy][x]*p>0: 
                      caps.append(valid)
                      if pieces[y+dy][x]==2:
                          chosen=valid
              except:
                  pass
             
    
        if chosen==None and len(caps)>0: chosen = random.choice(caps)
        if chosen==None: chosen = random.choice(valids)

        action = { "from_location": chosen[0:2], "to_location": chosen[2:4] }
        
        super().recordAction(observation, reward, done, action)        

        return action
 


     
