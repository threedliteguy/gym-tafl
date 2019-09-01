import gym

env = gym.make('gym_tafl:tafl-v0', variant='Brandubh')

ob = env.reset()
print('ob=',ob)

action = env.action_space.sample()
print('action=', action)

ob, reward, done, _ = env.step(action)

print('ob =', ob, ' reward=', reward, ' done=', done)

env.close()

