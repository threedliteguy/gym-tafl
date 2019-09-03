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
    
    env = gym.make('gym_tafl:tafl-v0', variant='Brandubh')

    arg = 'human' if len(sys.argv)==1 else sys.argv[1]
  
    if arg == 'contest':
       
        # With random play, white wins 75% of time.

        #agents = [ RandomAgentWithRules(env.action_space), RandomAgentWithRules(env.action_space) ]
        #agents = [ ModelAgentWithRules('gym-tafl/gym_tafl/train/models/model_1',env.action_space), RandomAgentWithRules(env.action_space) ]
        agents = [ RandomAgentWithRules(env.action_space), ModelAgentWithRules('gym-tafl/gym_tafl/train/models/model_2',env.action_space) ]
        
        score=0
        for i in range(100):
           runner = Runner(env,agents)
           rewards = runner.run()
           if rewards[0] > 0: score = score + 1
        print("White's final score: ", score, '%')   

    elif arg == 'record':  
   
        for i in range(1000):
           agents = [ GreedyAgentWithRules(env.action_space,"output/player_1-"+str(i)+".txt"), 
                      GreedyAgentWithRules(env.action_space,"output/player_2-"+str(i)+".txt") ]
           runner = Runner(env,agents)
           runner.run()

    elif arg == 'human':

        agents = [ HumanAgentWithRules(env.action_space), GreedyAgentWithRules(env.action_space) ]
        runner = Runner(env,agents)
        runner.run()


