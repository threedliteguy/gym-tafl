import gym
import random


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




if __name__ == '__main__':
    
    # tafl order of play is white (with king) first, black (attackers) second #TODO check
    # tafl is asymetric, so separate models are required for each player.
    from gym_tafl.agents.human_agent_with_rules import HumanAgentWithRules
    from gym_tafl.agents.random_agent_with_rules import RandomAgentWithRules
    env = gym.make('gym_tafl:tafl-v0', variant='Brandubh')
    #agents = [ HumanAgentWithRules(env.action_space), RandomAgentWithRules(env.action_space) ]
    agents = [ RandomAgentWithRules(env.action_space,"player1.txt"), RandomAgentWithRules(env.action_space,"player2.txt") ]
    runner = Runner(env,agents)
    runner.run()


