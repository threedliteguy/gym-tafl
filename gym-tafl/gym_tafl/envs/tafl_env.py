import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.spaces import Discrete, Tuple, Box, Dict
import numpy as np


class TaflEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    variant = ''
    g = None

    def __init__(self, variant='Brandubh'):
        
        print('init ', variant)
        
        self.variant = variant
        self._setGameVariant(variant)

        self.action_space = Dict({
            "from_location":Tuple((Discrete(self.g.size),Discrete(self.g.size))),
            "to_location":Tuple((Discrete(self.g.size),Discrete(self.g.size)))
            })

        self.observation_space = Dict({
            "board": Box(low=0,high=2,shape=(self.g.size,self.g.size),dtype=np.int32), 
            "pieces": Box(low=-1,high=2,shape=(self.g.size,self.g.size),dtype=np.int32), 
            "playerToMove": Discrete(2)
            })

        self.seed()


    def _setGameVariant(self,variant):
        from gym_tafl.envs import TaflGame
        from gym_tafl.envs import GameVariants

        if variant == 'Brandubh': self.g = TaflGame.GameState(GameVariants.Brandubh())
        elif variant == 'Tablut': self.g = TaflGame.GameState(GameVariants.Tablut())
        elif variant == 'Tawlbwrdd': self.g = TaflGame.GameState(GameVariants.Tawlbwrdd())
        elif variant == 'Hnefatafl': self.g = TaflGame.GameState(GameVariants.Hnefatafl())
        elif variant == 'AleaEvangelii': self.g = TaflGame.GameState(GameVariants.AleaEvangelii())
        else: self.g = TaflGame.GameState()


    def _mapStateToObs(self):
        board = np.zeros((self.g.size, self.g.size), dtype=np.int32)
        pieces = np.zeros((self.g.size, self.g.size), dtype=np.int32)

        for item in self.g.board:
            board[item[1]][item[0]] = item[2]

        for piece in self.g.pieces:
            if piece[0] >= 0: pieces[piece[1]][piece[0]] = piece[2]
   
        ob = { "board":board, "pieces":pieces, "playerToMove":(self.g.time%2 == 0) }
        return ob
    
    def _mapActionToMove(self,action):
        move = [action['from_location'][0],action['from_location'][1],action['to_location'][0],action['to_location'][1]]    
        return move

    def reset(self):
        print('reset')
        self._setGameVariant(self.variant)
        ob = self._mapStateToObs()
        return ob

    def step(self, action):
        print('step')
        move = self._mapActionToMove(action)
        result = self.g.move(*move)
        reward = result
        episode_over = self.g.done != 0
        # if game is just now done, last player to move would have won. Other player(s) agent could get corresponding negative reward.
        if episode_over:
           reward = 1000 
        ob = self._mapStateToObs()
        player = -1 if self.g.time%2==0 else 1 
        valids = self.g.getValidMoves(player)
        return ob, reward, episode_over, {"valid_moves":valids}

    def render(self, mode='human'):
        print('render')
        self.g.render()

    def close(self):
        print('close')

    def seed(self, seed=None):
        print('seed')
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

