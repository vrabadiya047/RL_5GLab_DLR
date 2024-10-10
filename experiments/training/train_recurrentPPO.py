import gym
from sb3_contrib import RecurrentPPO

from ki_5g_env import Custom_Env
from experiments.misc import parse_cmd
from stable_baselines3.common.callbacks import CheckpointCallback
import sys, os
import time


DIR_PATH = os.path.dirname(os.path.dirname(__file__) + "/../../")


def train_testagent(options):
    # parameters for experiment run
    model_name = 'recur_' + options.full_name
    num_episodes = options.num_episodes
    episode_length = options.episode_length

    # create custom env
    env = gym.make("fiveg-v0",
                   use_gui=options.plot,
                   seed_fun=options.seed_function,
                   pre_learn_steps=options.pre_learn_steps,
                   post_done_steps=options.post_done_steps,
                   rew_factors=options.reward_factors,
                   verbose=2,
                   frame_stacks=90)  # type: # Custom_Env
    env.set_em_veh_instertion_range(options.ev_step_range[0], options.ev_step_range[1])

    model = RecurrentPPO("MlpLstmPolicy",
                         env,
                         n_steps=500,
                         batch_size=500,
                         verbose=1,
                         learning_rate=options.learning_rate_function,
                         create_eval_env=True,
                         policy_kwargs={"normalize_images": False,
                                        "lstm_hidden_size": 50},
                         tensorboard_log=DIR_PATH + "/outputs/tensorboard/PPO_recurrent/")

    print(" #### Learning model '%s' with %s sim_steps for %s episodes #####" % (
    model_name, episode_length, num_episodes))
    start = time.time()
    checkpoint_callback = CheckpointCallback(save_freq=episode_length * 1000, save_path=DIR_PATH + "/outputs/training/",
                                             name_prefix='temp' + model_name)
    model.learn(total_timesteps=num_episodes * episode_length, callback=checkpoint_callback)

    # save model
    model_file_name = model_name + "_" + time.strftime("%Y%m%d-%H%M%S")
    model.save(DIR_PATH + "/outputs/models/" + model_file_name)
    env.close()
    elapsed_time = time.time() - start
    print(" #### Duration of the training experiment =", time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print("Model name:", model_file_name)

    del model


if __name__ == "__main__":
    options = parse_cmd()
    train_testagent(options)
