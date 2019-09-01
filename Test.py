import gym
import random

env = gym.make('gym_tafl:tafl-v0', variant='Brandubh')

ob = env.reset()

done=False

while not done:

   print(ob['pieces'])
   valids = ob['validMoves']
   valids = list(map(lambda y: y.tolist(), list(filter(lambda x: sum(x)>0, valids))))
   print('validMoves=',valids)

   chosen = random.choice(valids)

   #action = env.action_space.sample()
   action = { "from_location": chosen[0:2], "to_location": chosen[2:4] }

   print('action=', action)

   ob, reward, done, _  = env.step(action)
   print('reward=', reward, ' done=', done)


print(ob['pieces'])


env.close()

