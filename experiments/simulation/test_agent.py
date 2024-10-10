import gym
from ki_5g_env import Custom_Env
# from stable_baselines3.common.env_checker import check_env
import numpy as np
from numpy.random import randint

def generateSumoSeed() -> int:
    return randint(2**31)

def random_agent():
    env = Custom_Env(use_gui=True)
    # check_env(env)
    
    seed = generateSumoSeed()
    env.set_seed(seed)
    env.reset()
    for i in range(0, 2000):
        observation, reward, done, _ = env.step(0)
        if done:
            print(i, env._sumo_handler.get_simulation_step())
            seed = generateSumoSeed()
            env.set_seed(seed)
            env.reset()
    env.close()


def random_agent1():
    env = gym.make("fiveg-v0",use_gui=True, debug=True) #type: Custom_Env
    env.set_seed(2046)
    env.set_episode_length(1000)
    env.reset()

    for i in range(0,5000):
        action = env.action_space.sample()
        obs, reward, done, _ = env.step(action)
        if done:
            print(i, env.get_sumo_handler().get_simulation_step())
            env.set_seed(2046)
            env.set_episode_length(500)
            env.reset()
    print("DONE")
    env.close()


if __name__ == "__main__":
    random_agent1()
