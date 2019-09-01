import gym
import random

if __name__ == '__main__':

    env = gym.make('gym_tafl:tafl-v0', variant='Brandubh')

    action_space = env.action_space
    # tafl order of play is white (with king) first, black (attackers) second #TODO check
    # tafl is asymetric, so separate models are required for each player.
    from gym_tafl.agents.human_agent_with_rules import HumanAgentWithRules
    from gym_tafl.agents.random_agent_with_rules import RandomAgentWithRules
    agents = [ HumanAgentWithRules(action_space), RandomAgentWithRules(action_space) ]
    rewards = [0,0]

    observation = env.reset()

    done=False

    while not done:

       # tafl has only 2 plyers 
       player = observation['playerToMove']
       player = 1 if player == -1 else 0

       action = agents[player].act(observation, rewards[player], done)

       #print('action=', action)

       observation, reward, done, _  = env.step(action)
       print('reward=', reward, ' done=', done)

       # Zero-sum rewards assumed, since there is only one winner in tafl.
       for i in range(len(rewards)):
           if i == player:
               rewards[i] = reward
           else:    
               rewards[i] = rewards[i] + -reward//(len(agents)-1) 


       #TODO need some model feedback for other players when they lost when not their turn which allows developing critical defense adjustments.
       #This may require adding a 'pass' option if 'done' is set that is only legal in this phase, since there may be no legal moves at that point, and moves that win after another player has won are not allowed.  The only purpose of continuing the round is to pass the negative reward to the other players' agents/models.


    print(observation['pieces'])


    env.close()

