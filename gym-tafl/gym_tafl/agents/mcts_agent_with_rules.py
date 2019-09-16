
from __future__ import division

import gym
import random


from copy import deepcopy
from mcts import mcts
from functools import reduce
import operator

from base_agent import BaseAgent
from gym_tafl.envs.TaflGame import GameState
from gym_tafl.envs.GameVariants import Brandubh

class GSetup():
    def __init__(self,size,board,pieces):
        self.size=size
        self.board=board
        self.pieces=pieces


# For PyPi mcts.mcts's interface, see https://raw.githubusercontent.com/pbsinclair42/MCTS/master/naughtsandcrosses.py 
class MctsBoardState():
    def __init__(self,gs,player):
        self.gs = gs
        self.reward=0
        self.player=player
        self.originalplayer=player
        self.lastaction=None

    def getPossibleActions(self):

        valids = self.gs.getValidMoves(self.player)

        return list(map(lambda a: Action(self.player,a[0],a[1],a[2],a[3]), valids))

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.lastaction=action
        caps = newState.gs.move(action.x1, action.y1, action.x2, action.y2)
        newState.reward = caps * self.player * self.originalplayer
        if newState.gs.done: newState.reward = newState.gs.done * 1000 * self.originalplayer
        newState.player = -newState.player
        return newState

    def isTerminal(self):
        #if not self.reward==0: print("leaf reward=",self.reward, self.lastaction, self.player, self.originalplayer)
        return not self.gs.getWinLose() == 0

    def getReward(self):
        return self.reward

class Action():
    def __init__(self, player, x1, y1, x2, y2):
        self.player = player
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return str((self.x1, self.y1, self.x2, self.y2))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2 and self.player == other.player

    def __hash__(self):
        return hash((self.x1, self.y1, self.x2, self.y2, self.player))



class MctsAgentWithRules(BaseAgent):


    def __init__(self, action_space, recordFile=None):
        super().__init__(action_space, recordFile)
        self.board = Brandubh().board

    def act(self, observation, reward, done):
        
        if done:
            super().recordAction(None, reward, done, None)
            return None

        valids = observation['validMoves']
        valids = list(map(lambda y: y.tolist(), list(filter(lambda x: sum(x)>0, valids))))

        pieces = observation['pieces']
        size=len(pieces)
        chosen = None
        player = observation['playerToMove']

        g = GSetup(len(pieces), self.board, self._convertPieces(pieces)) 
        gs = GameState(g)
        gs.quiet=True
        gs.time = 0 if player == 1 else 1
       
        if not len(valids) == len(gs.getValidMoves(player)): raise Exception('rules mismatch')
 
        initialState = MctsBoardState(gs,player)
        amcts = mcts(timeLimit=30000)
        action = amcts.search(initialState=initialState)
        chosen=[action.x1,action.y1,action.x2,action.y2]

        print("mcts chosen action: ", chosen)
    
        if chosen==None: chosen = random.choice(valids)

        action = { "from_location": chosen[0:2], "to_location": chosen[2:4] }
        
        super().recordAction(observation, reward, done, action)        

        return action

    def _convertPieces(self,pieces):
        types = []
        for y,row in enumerate(pieces):
            for x,cell in enumerate(row):
               if not cell == 0: types.append([x,y,cell])
        return types

        return reward       




     
