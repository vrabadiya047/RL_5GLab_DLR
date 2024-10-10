import gym
import os

from numpy.random import randint
from stable_baselines3 import PPO
from statistics import mean
from math import floor
from typing import Dict, Tuple, List
import matplotlib.pyplot as plt
import pickle

from ki_5g_env import Custom_Env
from experiments.eval.live_eval import LiveEvaluation
from experiments.misc import parse_cmd
from experiments.eval.decision_functions import DecisionFun, ModelDecisionFun, HeuristicDecisionFun

os.environ['KMP_DUPLICATE_LIB_OK']='True' # running into OMP error #15 on windows otherwise, occurs when trying to plot, potentially while tensorboard is active
DIR_PATH=os.path.dirname(os.path.dirname(__file__)+"/../../")


def single_test(options, decision_fun : DecisionFun):
    ev_insertion_time = randint(options.ev_step_range[0], options.ev_step_range[1])
    model_name = options.name
    test_length=options.test_length
    sumo_dir=str(DIR_PATH)+"/outputs/sumo/"+model_name+"/"
    if not os.path.exists(sumo_dir):
        os.makedirs(sumo_dir)
    
    env = gym.make("fiveg-v0",
                   debug=options.debug, 
                   sumo_output=options.sumo_output, 
                   model_name=model_name, 
                   seed_fun = options.seed_function,
                   verbose = 0,
                   frame_stacks = 90) # type: Custom_Env
    
    # run model for testing    
    eval = LiveEvaluation()
    env.set_em_veh_instertion_range(ev_insertion_time, ev_insertion_time)
    env.set_pre_learn_steps(ev_insertion_time)
    obs = env.reset()
    ev_step = None
    ev_passed = False
    for _ in range (1,test_length):
        if ev_passed or env.get_sumo_handler().em_veh_passed_stopline():
            action = 0
            ev_passed = True
        else:
            action = decision_fun.decide(obs)
        obs, _, _, _ =env.step(action)
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
    
    # mass eval math
    # min speed
    min_speed_ev = None
    ev_speed_data = eval.get_ev_speed_data().get_data()
    if len(ev_speed_data) > 0:
        start_cut = min(ev_insertion_time+30, len(ev_speed_data)-1)
        half_ev_speed_data = ev_speed_data[start_cut:]
        min_speed_ev = min(half_ev_speed_data)
    else: print("ERROR: NO MIN SPEED", ev_insertion_time, env.get_sumo_handler()._seed)
    
    # waiting veh
    avg_waiting_veh = None
    ev_present_data = eval.get_ev_present_data().get_data()
    waiting_data = eval.get_veh_waiting_data().get_data()
    combined_data = []
    for i in range(len(ev_present_data)):
        val = ev_present_data[i]
        if val > 0:
            combined_data.append(waiting_data[i])
    if len(combined_data) > 0: avg_waiting_veh = mean(combined_data)
    if not avg_waiting_veh: print("ERROR: NO WATING VEH", ev_insertion_time, env.get_sumo_handler()._seed)
    
    # action
    num_req = 0
    actions = eval.get_action_data().get_data()
    if len(actions) > 0:
        for i in range(1,len(actions)):
            num_req += abs(actions[i]-actions[i-1])
    
    
    return min_speed_ev, avg_waiting_veh, num_req/2


def multiple_tests(options):
    MIN_SPEED = 0
    AVG_VEH = 1
    NUM_REQ = 2
    funs = [
        ModelDecisionFun(PPO.load(DIR_PATH+"/outputs/models/"+options.name), options.name),
        # ModelDecisionFun(PPO.load(DIR_PATH+"/outputs/saved_models/"+options.name), options.name),
        # HeuristicDecisionFun(1.00),
        # HeuristicDecisionFun(0.75),
        # HeuristicDecisionFun(0.50),
        # HeuristicDecisionFun(0.25),
        # HeuristicDecisionFun(0.00),
    ] # type: # List[DecisionFun]
    results = dict() # type: # Dict[DecisionFun, Tuple[List, List]]
    print('Running %i tests for each of the following functions:' % options.num_runs_mass_eval)
    for fun in funs:
        print(fun.get_file_name())
    for fun in funs:
        results[fun] = ([], [], [])
        print('Running ',fun.get_file_name(), 'with', str(options.num_runs_mass_eval), 'repetitions...')
        for i in range(options.num_runs_mass_eval):
            print(str(i+1).rjust(len(str(options.num_runs_mass_eval))),'/', options.num_runs_mass_eval, end='\r')
            mse, awv, nr = single_test(options, fun)
            if mse != None: results[fun][MIN_SPEED].append(mse)
            if awv != None: results[fun][AVG_VEH].append(awv)
            if nr  != None: results[fun][NUM_REQ].append(nr)
    
    # pickle data for later use
    for fun in funs:
        with open('tmp/'+fun.get_file_name()+'.pickle','wb') as file:
            pickle.dump(results[fun], file)    
    
    if options.plot:
        def plot(title : str, result_type : int) -> None:
            plt.title(title)
            plt.boxplot([results[f][result_type] for f in funs])
            plt.xticks(list(range(1,len(funs)+1)), [f.get_name() for f in funs])
            plt.show()
            
        plot('min speed ev', MIN_SPEED)
        # plot('avg waiting veh', AVG_VEH)
        # plot('num requests', NUM_REQ)
    return None


if __name__ == "__main__":
    options = parse_cmd()
    multiple_tests(options)
