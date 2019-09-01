from gym.envs.registration import register

register(id='tafl-v0',
         entry_point='gym_tafl.envs:TaflEnv',
)
