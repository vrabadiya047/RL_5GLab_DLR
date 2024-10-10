import gym, os, sys
from gym import spaces
import numpy as np
from typing import Dict, Tuple, Callable
from .sumo_interfacing import SumoHandler
from numpy.random import randint
from .ringbuffer import Ringbuffer


def _generate_sumo_seed() -> int:
    return randint(2 ** 31)


class Custom_Env(gym.Env):
    _OBS_TYPE = np.float64

    def __init__(self, use_gui: bool = False,
                 seed_fun: Callable[[], int] = None,
                 debug: bool = False,
                 model_name: str = "test_model",
                 sumo_output: bool = False,
                 pre_learn_steps: int = 0,
                 post_done_steps: int = 90,
                 ev_step_range=(1600, 1800),
                 rew_factors=None,
                 verbose=0,
                 frame_stacks=0) -> None:
        self._sumo_handler = SumoHandler(use_gui=use_gui, model_name=model_name, sumo_output=sumo_output)
        self.observation_space = spaces.Box(low=0,
                                            high=1,
                                            shape=(6 + 4 + 2 * 9 + frame_stacks,),
                                            # +2*len(self._sumo_handler.get_det_data().get_data()), ),
                                            dtype=self._OBS_TYPE)
        self.action_space = spaces.Discrete(2)
        if seed_fun == None:
            self._seed_fun = _generate_sumo_seed  # type: # Callable[[], int]
        else:
            self._seed_fun = seed_fun
        if rew_factors == None:
            self._rew_factors = (1, 100, 3, 10, 1, 10)
        else:
            self._rew_factors = rew_factors
        self._episode_length = 1000
        self._previous_action = 0
        self._run = 0
        self._debug = debug
        self._em_veh_insertion_step = 850
        self._em_req_in_a_row = 0
        self._pre_learn_steps = pre_learn_steps
        self._post_done_steps = post_done_steps
        self._ev_step_range = ev_step_range
        self._verbose = verbose
        self._det_obs_hist = Ringbuffer(1 + frame_stacks)

    def get_sumo_handler(self) -> SumoHandler:
        return self._sumo_handler

    def set_em_veh_insertion_step(self, step: int) -> None:
        self._em_veh_insertion_step = step

    def set_em_veh_instertion_range(self, min_step: int, max_step: int) -> None:
        self._ev_step_range = (min_step, max_step)

    def set_pre_learn_steps(self, num: int) -> None:
        self._pre_learn_steps = num

    def set_post_learn_steps(self, num: int) -> None:
        self._post_done_steps = num

    def get_em_veh_insertion_step(self) -> int:
        return self._em_veh_insertion_step

    def _get_random_ev_insertion_step(self) -> int:
        return randint(self._ev_step_range[0], self._ev_step_range[1] + 1)

    def reset(self) -> np.ndarray:
        self._run += 1
        if self._sumo_handler.sumo_is_running():
            self._sumo_handler.release_em_phase()
            for _ in range(self._post_done_steps):
                self._sumo_handler.do_simulation_step()
            self._sumo_handler.stop_sumo()
        self._det_obs_hist.reset()
        self._sumo_handler.reset()
        self.set_em_veh_insertion_step(self._get_random_ev_insertion_step())
        seed = self._seed_fun()
        self._sumo_handler.set_seed(seed)
        if self._verbose >= 1: print("Seed for new episode: ", seed)
        self._sumo_handler.start_sumo()
        for _ in range(self.get_em_veh_insertion_step() - self._pre_learn_steps):
            self._sumo_handler.do_simulation_step()
        return self._compute_observation()

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict]:
        self._apply_action(action)

        if self._sumo_handler.get_current_simulation_time() == self.get_em_veh_insertion_step():
            self._sumo_handler.insert_em_vehicle()

        self._sumo_handler.do_simulation_step()

        observation = self._compute_observation()
        reward = self._compute_reward()
        done = self._compute_done()
        info = self._compute_info()

        self._set_previous_action(action)
        if done and self._verbose >= 2: print("Finished episode: ", self._run)

        if self._debug:
            print("#### Timestep: %s , Action: %s , Reward: %s , Observation:\n%s" % (
            self._sumo_handler.get_current_simulation_time(), action, reward, observation))

        return observation, reward, done, info

    def _apply_action(self, action: int) -> None:
        if action == 1:
            self._sumo_handler.request_em_phase()
            self._em_req_in_a_row += 1
        elif action == 0:
            self._sumo_handler.release_em_phase()
            self._em_req_in_a_row = 0

    def _compute_observation(self) -> np.ndarray:
        obs=[]

        # em veh in sim - 1
        obs.append(int(self._sumo_handler.simulation_has_em_vehicle()))

        # em veh speed - 1
        obs.append(self._sumo_handler.get_em_veh_speed() / self._sumo_handler.get_em_veh_desired_speed())

        # em veh distance - 1
        obs.append(self._sumo_handler.get_em_veh_distance_to_junction() / self._sumo_handler.get_em_veh_max_distance())

        # em req in a row - 1
        norm_req_nr = min(self._em_req_in_a_row, 60) / 60
        obs.append(norm_req_nr)

        # current phase as bit vector - 9
        cur_phase_list = [0 for _ in range(9)]
        cur_phase_id = self._sumo_handler.get_junction_control().getController().getCurrentPhaseID()
        cur_phase_list[cur_phase_id] = 1
        obs += cur_phase_list

        # next phase as bit vector - 9
        nex_phase_list = [0 for _ in range(9)]
        nex_phase_id = int(max(self._sumo_handler.get_junction_control().getController().getNextPhaseID(), 0.0))
        nex_phase_list[nex_phase_id] = 1
        obs += nex_phase_list

        # current phase duration, 0 during transition - 1
        phase_dur = 0
        if self._sumo_handler.get_junction_control().getController().somePhaseIsActive():
            phase_dur = self._sumo_handler.get_junction_control().getController().getCurrentPhaseDuration(
                self._sumo_handler.get_current_simulation_time())
        obs.append(min(1.0, phase_dur / 30))

        # current phase transition duration, 0 during phase - 1
        phase_transition_dur = 0
        if self._sumo_handler.get_junction_control().getController().somePhaseTransitionIsActive():
            phase_transition_dur = self._sumo_handler.get_junction_control().getController().getCurrentPhaseTransitionDuration(
                self._sumo_handler.get_current_simulation_time())
        obs.append(min(1.0, phase_transition_dur / 30))

        # vehicle estimate within detector range:
        no, ea, so, we = self._sumo_handler.get_veh_estimate()
        self._det_obs_hist.write(so)
        obs.append(no)
        obs.append(ea)
        obs.append(we)
        obs.extend(self._det_obs_hist.get_sorted_data())

        # detector value pairs - 2x len(self._sumo_handler.get_det_data().get_data())
        # det_data = self._sumo_handler.get_det_data()
        # for date in det_data.get_data().values():
        #     obs.append(date.get_vehicle_count()/date.get_accumulation_length())
        #     obs.append(date.get_occupancy())
        obs = np.array(obs, dtype=self._OBS_TYPE)
        return obs

    def _compute_reward(self) -> float:
        reward_pieces = []
        # normalize rewards to [-1, 1]
        # 1 reward requesting em phase when ev in simulation
        # max reward: 1
        if self._sumo_handler.simulation_has_em_vehicle() and (self._sumo_handler.em_phase_is_requested()
                                                               or self._sumo_handler.em_phase_is_running()
                                                               or self._sumo_handler.em_phase_transition_is_running()):
            reward_pieces.append(1)
        else:
            reward_pieces.append(0)
        # 2 reward running em phase when ev in simulation    
        # if self._sumo_handler.simulation_has_em_vehicle() and self._sumo_handler.em_phase_is_running():
        #     reward_pieces.append(1)
        # else:
        #     reward_pieces.append(0)
        # 3 punish requesting or running em phase when ev is not in simulation
        # max punishment: 2000
        if not self._sumo_handler.simulation_has_em_vehicle() and (self._sumo_handler.em_phase_is_requested()
                                                                   or self._sumo_handler.em_phase_is_running()
                                                                   or self._sumo_handler.em_phase_transition_is_running()):
            reward_pieces.append(-1)
        else:
            reward_pieces.append(0)
        # 4 punish requesting or running em phase when ev is far away
        # max punishment: 1000
        if self._sumo_handler.simulation_has_em_vehicle() and (self._sumo_handler.em_phase_is_requested()
                                                               or self._sumo_handler.em_phase_is_running()
                                                               or self._sumo_handler.em_phase_transition_is_running()):
            reward_pieces.append(-self._sumo_handler.get_em_veh_distance_to_junction() / 1000)
        else:
            reward_pieces.append(0)
        # 5 punish low speed of em vehicle
        # max punishment: 2500
        if self._sumo_handler.simulation_has_em_vehicle():
            desired = self._sumo_handler.get_em_veh_desired_speed() * 3.6
            speed = self._sumo_handler.get_em_veh_speed() * 3.6
            em_req_in_a_row_factor = min(2.0, 1 + self._em_req_in_a_row / 60)
            reward_pieces.append(max(-1.0, -(desired - speed) * (desired - speed) / 2500 / em_req_in_a_row_factor))
        else:
            reward_pieces.append(0)
        # 6 punish waiting vehicles when em phase is requested or em phase is running
        # max punishment: 100???
        # if self._sumo_handler.em_phase_is_requested() or self._sumo_handler.em_phase_is_running():
        #     reward_pieces.append(-self._sumo_handler.get_number_of_waiting_vehicles()/100)
        # else:
        #     reward_pieces.append(0)
        # 7 punish taking em request back or canceling em phase
        # if (self._get_previous_action()==1 or self._sumo_handler.em_phase_is_running()) and not self._sumo_handler.em_phase_is_requested():
        #     reward_pieces.append(-1)
        # else:
        #     reward_pieces.append(0)
        # 8 reward em requests in a row
        reward_pieces.append(min(1.0, self._em_req_in_a_row / 60))

        # 9 punish deactivating em req when ev in sim
        if self._sumo_handler.simulation_has_em_vehicle() and self._em_req_in_a_row == 0 and self._get_previous_action() == 1:
            reward_pieces.append(-1)
        else:
            reward_pieces.append(0)

        # 1 reward request when ev in sim, combine with 2
        # # 2 reward running em phase when ev in sim
        # 3 punish requesting or running em phase when ev is not in simulation
        # 4 punish requesting or running em phase when ev is far away
        # 5 punish low speed of ev
        # # 6 punish waiting vehicles when em phase is requested or em phase is running
        # # 7 punish taking em request back or canceling em phase
        # 8 reward em requests in a row (up to 60)
        # 9 punish deactivating em req when ev in sim
        #            1,   3, 4,  5, 8,  9
        # factors = [1, 100, 3, 10, 1, 10]
        reward = sum([reward_pieces[i] * self._rew_factors[i] for i in range(len(self._rew_factors))])
        return reward

    def _compute_done(self) -> bool:
        if self._sumo_handler.em_veh_passed_intersection():
            return True
        return False

    def _compute_info(self) -> Dict:
        return {}

    def close(self) -> None:
        if self._sumo_handler.sumo_is_running():
            self._sumo_handler.stop_sumo()

    def set_seed_fun(self, seed_fun: Callable) -> None:
        self._seed_fun = seed_fun

    def set_episode_length(self, episode_length: int) -> None:
        self._episode_length = episode_length

    def _set_previous_action(self, action: int) -> None:
        self._previous_action = action

    def _get_previous_action(self) -> int:
        return self._previous_action
