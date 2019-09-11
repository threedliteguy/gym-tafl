import gym
import random
import sys

class Runner(object):

    def __init__(self,env,agents):
        self.env=env
        self.agents=agents

    def run(self):

        rewards = [0,0]

        observation = self.env.reset()

        done=False

        while not done:

           # tafl has only 2 plyers 
           player = observation['playerToMove']
           player = 1 if player == -1 else 0

           action = self.agents[player].act(observation, rewards[player], done)

           observation, reward, done, _  = self.env.step(action)
           print('reward=', reward, ' done=', done)

           # Zero-sum rewards assumed, since there is only one winner in tafl.
           for i in range(len(rewards)):
               if i == player:
                   rewards[i] = reward
               else:    
                   rewards[i] = rewards[i] + -reward//(len(agents)-1) 
           


        for i,agent in enumerate(self.agents):
            try:
               agent.act(None, rewards[i], done)
               agent.save()
            except Exception as e: 
               print(e)

        print(observation['pieces'])

        
        self.env.close()

        return rewards



if __name__ == '__main__':
    
    # tafl order of play is white (with king) first, black (attackers) second #TODO check
    # tafl is asymetric, so separate models are required for each player.
    
    from gym_tafl.agents.model_agent_with_rules import ModelAgentWithRules
    from gym_tafl.agents.human_agent_with_rules import HumanAgentWithRules
    from gym_tafl.agents.random_agent_with_rules import RandomAgentWithRules
    from gym_tafl.agents.greedy_agent_with_rules import GreedyAgentWithRules
    from gym_tafl.agents.mcts_agent_with_rules import MctsAgentWithRules
    
    env = gym.make('gym_tafl:tafl-v0', variant='Brandubh')

    arg = 'human' if len(sys.argv)==1 else sys.argv[1]
  
    if arg == 'contest':
       
        # With random vs random play, white wins about 75% of time.
        # With white random vs black greedy play, white wins about 7-10% of time.
        # With white greedy vs black random play, white wins about 95% of time.
        # With white greedy vs black greedy play, white wins about 25-30% of time.

        #agents = [ RandomAgentWithRules(env.action_space), RandomAgentWithRules(env.action_space) ]
        #agents = [ RandomAgentWithRules(env.action_space), GreedyAgentWithRules(env.action_space) ]
        #agents = [ GreedyAgentWithRules(env.action_space), RandomAgentWithRules(env.action_space) ]
        #agents = [ GreedyAgentWithRules(env.action_space), GreedyAgentWithRules(env.action_space) ]
        
        #agents = [ ModelAgentWithRules('gym-tafl/gym_tafl/train/models/model_1',env.action_space), RandomAgentWithRules(env.action_space) ]
        #agents = [ RandomAgentWithRules(env.action_space), ModelAgentWithRules('gym-tafl/gym_tafl/train/models/model_2',env.action_space) ]
        
        #agents = [ ModelAgentWithRules('gym-tafl/gym_tafl/train/models/model_1',env.action_space), GreedyAgentWithRules(env.action_space) ]
        #agents = [ GreedyAgentWithRules(env.action_space), ModelAgentWithRules('gym-tafl/gym_tafl/train/models/model_2',env.action_space) ]
        
        #agents = [ ModelAgentWithRules('gym-tafl/gym_tafl/train/models/model_1',env.action_space), ModelAgentWithRules('gym-tafl/gym_tafl/train/models/model_2',env.action_space) ]
        #agents = [ ModelAgentWithRules('gym-tafl/gym_tafl/train/models_v2/model_1',env.action_space), ModelAgentWithRules('gym-tafl/gym_tafl/train/models_v1/model_2',env.action_space) ]
        #agents = [ ModelAgentWithRules('gym-tafl/gym_tafl/train/models_v2/model_1',env.action_space), GreedyAgentWithRules(env.action_space) ]

        #agents = [ GreedyAgentWithRules(env.action_space), MctsAgentWithRules(env.action_space) ]
        agents = [ MctsAgentWithRules(env.action_space), GreedyAgentWithRules(env.action_space) ]


        # Notes:
        # The v1 model for black seems to be better than random and similar to greedy vs. white greedy
        # The v1 model for white seems to be twice as good as random but half as good as greedy vs. black greedy
        # Recording games between the two v1 models, and using that to train a second set of models, the white model v2 improved to win 20-23% against black greedy (closer to white greedy), but the black model v2 performance fell to lose 60% vs white greedy.
        # note: training times were increased in the second round of training.
        
        # TODO: Not all of the offical rules are implemented in TaflGame.py, so those could be added, for example king being safe in home square.
        # A fairly small Feed Forward net was used to be able to train and interate quickly on a CPU.

        score=0
        
        rounds=1000
        #rounds=100

        for i in range(rounds):
           runner = Runner(env,agents)
           rewards = runner.run()
           if rewards[0] > 0: score = score + 1
        print("White's final score: ", score/rounds*100, '%')   

    elif arg == 'record':  
   
        for i in range(1000):
           agents = [ 
                      MctsAgentWithRules(env.action_space,"output/player_1-"+str(i)+".txt"), 
                      #MctsAgentWithRules(env.action_space,"output/player_2-"+str(i)+".txt") 
                      #GreedyAgentWithRules(env.action_space,"output/player_1-"+str(i)+".txt"), 
                      GreedyAgentWithRules(env.action_space,"output/player_2-"+str(i)+".txt") 
                      #ModelAgentWithRules('gym-tafl/gym_tafl/train/models/model_1',env.action_space,"output/player_1-"+str(i)+".txt"), 
                      #ModelAgentWithRules('gym-tafl/gym_tafl/train/models/model_2',env.action_space,"output/player_2-"+str(i)+".txt") 
                      ]
           runner = Runner(env,agents)
           runner.run()

    elif arg == 'human':

        agents = [ HumanAgentWithRules(env.action_space), MctsAgentWithRules(env.action_space) ]
        #agents = [ MctsAgentWithRules(env.action_space), HumanAgentWithRules(env.action_space) ]
        #agents = [ HumanAgentWithRules(env.action_space), GreedyAgentWithRules(env.action_space) ]
        #agents = [ HumanAgentWithRules(env.action_space), ModelAgentWithRules('gym-tafl/gym_tafl/train/models/model_2',env.action_space) ]
        runner = Runner(env,agents)
        runner.run()


