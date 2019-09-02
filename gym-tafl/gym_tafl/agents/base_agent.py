import gym
import random


class BaseAgent():


    def __init__(self, action_space, recordFile=None):
        self.action_space = action_space
        self.recordFile=recordFile
        self.record=[]
        self.time=0

    def recordAction(self, observation, reward, done, action):
        
        if (not self.recordFile is None):
            result = str(reward)  # is for previous action
            if (not done):
               strpieces = ' '.join(str(e) for e in observation['pieces'].ravel())
               arrayaction = action['from_location'] + action['to_location']
               straction = ' '.join(str(e) for e in arrayaction)
               strplayer = str(observation['playerToMove'])
               result = result+"|"+strpieces+"|"+strplayer+"|"+straction
            self.record.append(result)

 
    def save(self):
        if (not self.recordFile is None):
           text_file = open(self.recordFile, "w")
           text_file.write('\n'.join(self.record))
           text_file.close()


     
