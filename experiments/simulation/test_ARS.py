import gym
from ki_5g_env import Custom_Env
from experiments.eval.live_eval import LiveEvaluation
from experiments.misc import parse_cmd
from sb3_contrib import *
import sys, os
import time

os.environ[
    'KMP_DUPLICATE_LIB_OK'] = 'True'  # running into OMP error #15 on windows otherwise, occurs when trying to plot, potentially while tensorboard is active
DIR_PATH = os.path.dirname(os.path.dirname(__file__) + "/../../")


def test_model(options):
    model_name = options.name
    start = time.time()

    eval = LiveEvaluation()

    sumo_dir = str(DIR_PATH) + "/outputs/sumo/" + model_name + "/"
    if not os.path.exists(sumo_dir):
        os.makedirs(sumo_dir)

    env = gym.make("fiveg-v0",
                   use_gui=options.plot,
                   debug=options.debug,
                   sumo_output=options.sumo_output,
                   model_name=model_name,
                   seed_fun=options.seed_function,
                   verbose=1,
                   frame_stacks=options.frame_stacks)  # type: # Custom_Env
    model = ARS.load(
        DIR_PATH + "/outputs/models/ARS_20220712-023042.zip")

    # parameters for experiment run
    test_length = options.test_length

    # run model for testing
    print(env.set_em_veh_instertion_range(500, 2000))
    env.set_pre_learn_steps(options.ev_step_test)
    obs = env.reset()
    ev_step = None
    ev_passed = False
    for _ in range(1, test_length):
        if ev_passed or env.get_sumo_handler().em_veh_passed_intersection():
            action = 0
            ev_passed = True
        else:
            action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = env.step(action)
        eval.update_all(env.get_sumo_handler().get_current_simulation_time(),
                        action,
                        env.get_sumo_handler().get_em_veh_speed(),
                        env.get_sumo_handler().get_number_of_waiting_vehicles(),
                        env.get_sumo_handler().em_phase_is_running(),
                        env.get_sumo_handler().em_phase_transition_is_running(),
                        env.get_sumo_handler().simulation_has_em_vehicle())
        if not ev_step:
            if env.get_sumo_handler().simulation_has_em_vehicle():
                ev_step = env.get_sumo_handler().get_current_simulation_time()

    env.close()
    elapsed_time = time.time() - start
    print(" #### Duration of the model testing: ", time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    if options.plot_training:
        # eval.plot_all(vline_pos=ev_step)
        estimated_trip_duration = 90
        eval.plot_all_clipped(ev_step - options.pre_learn_steps,
                              ev_step + options.post_done_steps + estimated_trip_duration, vline_pos=ev_step)


if __name__ == "__main__":
    options = parse_cmd()
    test_model(options)
