#!/usr/bin/env python3

import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sys.path.append(os.path.dirname(os.path.dirname(__file__)+"\\..\\"))    
from k048.control import Siemens, Controller
from k048.sumo_interfacing import reset_caches
from demand import FLOW_DIRECTIONS
import traci
from numpy.random import default_rng

OUTPUT_FILE="output.csv"
NUM_RUNS=1000

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_FILE_PATH = os.path.join(THIS_DIR, "../output/", OUTPUT_FILE)
STEP_LENGTH = 1
TIME_BEFORE_END = 90
SAMPLE_TIME_STEPS = [i*300 for i in range(1,11)]
END_TIME = SAMPLE_TIME_STEPS[-1] + TIME_BEFORE_END
FIRECAR_STEP = END_TIME - TIME_BEFORE_END
LAST_DOCUMENTATION_STEP = FIRECAR_STEP + 75

def build_sumo_cmd(sumo_exe="sumo", seed=23423) -> str:
    sumo_exe = os.path.join(os.environ["SUMO_HOME"], 'bin', sumo_exe)
    sumo_cmd = [sumo_exe, "-c", THIS_DIR+"/../tostmannplatz.sumocfg",
                "--no-step-log", "true",
                "-W",
                "--duration-log.disable",
                "--seed", str(seed),
                ]
    return sumo_cmd

def add_fire_car_to_simulation():
    traci.route.add('firecar_route', [FLOW_DIRECTIONS[7][0], FLOW_DIRECTIONS[7][1]])
    traci.vehicle.add('firecar', 'firecar_route', 'firecar', departSpeed="max")
    
def create_snapshot(controller : Controller, t : float, seed):
    EDGES_WAITING_VEHICLES = ["51932979", "51812159.-60", "51812159"]
    EDGES_VEH_AT_INTERSECTION = ["51932979", "51811895b", "51811895a", "-786367651", "-51812052", "-51811895a", "51812134", "-554747345", "51812159.-60"]
    curPh, nexPh, curPhDur, waitingVehiclesSN, numVehs, vehAtIntersection = 0, 0, 0, 0, 0, 0
    
    curPh = controller.getCurrentPhaseID()
    nexPh = controller.getNextPhaseID()
    if controller.somePhaseIsActive():
        curPhDur = controller.getCurrentPhaseDuration(t)
    elif controller.somePhaseTransitionIsActive():
        curPhDur = controller.getCurrentPhaseTransitionDuration(t)
    vehIdList = traci.vehicle.getIDList()
    numVehs = len(vehIdList)
    for edge in EDGES_WAITING_VEHICLES:
        for veh in traci.edge.getLastStepVehicleIDs(edge):
            if traci.vehicle.getSpeed(veh) < 0.1:
                waitingVehiclesSN+=1
    for edge in EDGES_VEH_AT_INTERSECTION:
        vehAtIntersection += traci.edge.getLastStepVehicleNumber(edge)
    firecar_dist = -1
    firecar_speed = -1
    if 'firecar' in vehIdList:
        dist = {}
        dist["51932979"] = traci.lane.getLength("51932979"+"_0")
        dist["51812159.-60"]= traci.lane.getLength("51812159.-60"+"_0")+dist["51932979"]
        dist["51812159"] = traci.lane.getLength("51812159"+"_0")+dist["51812159.-60"]
        dist["gneE4"] = traci.lane.getLength("gneE4"+"_0")+dist["51812159"]
        firecar_edge = traci.vehicle.getLaneID("firecar")[:-2]
        if firecar_edge in dist:
            firecar_lanepos = traci.vehicle.getLanePosition("firecar")
            firecar_dist = dist[firecar_edge] - firecar_lanepos
            firecar_speed = traci.vehicle.getSpeed('firecar')
        
    with open(OUTPUT_FILE_PATH,'a') as file:
        file.write("%i;%i;%i;%i;%i;%i;%i;%.1f;%.1f;%i\n"%(
            t,
            curPh,
            nexPh,
            curPhDur,
            numVehs,
            vehAtIntersection,
            waitingVehiclesSN,
            firecar_dist,
            firecar_speed,
            seed
        ))
            
        
    

def execute_full_simulation_run(sumo_exe="sumo",seed=23423):
    sumo_cmd = build_sumo_cmd(sumo_exe,seed)
    traci.start(sumo_cmd)
    junction_control = Siemens()
    reset_caches()
    step = 0
    endstep = END_TIME / STEP_LENGTH
    while step < endstep:
        step += 1
        t = step * STEP_LENGTH
        if step == FIRECAR_STEP:
            add_fire_car_to_simulation()
        # if step == firecar_step + 10:
        #     junction_control.controller.setEmergencyRequest(t, 1)
        # if step == firecar_step + 90:
        #     junction_control.controller.setEmergencyRequest(t, 0)
        junction_control.control(t)
        if step in SAMPLE_TIME_STEPS or step==LAST_DOCUMENTATION_STEP:
            create_snapshot(junction_control.controller, t, seed)
        traci.simulationStep(t)
    traci.close()
        
if __name__ == "__main__":
    for i in range(NUM_RUNS):
        seed = default_rng().integers(0,2**31)
        print(i, seed)
        # execute_full_simulation_run(sumo_exe="sumo-gui",seed=seed)
        execute_full_simulation_run(sumo_exe="sumo",seed=seed)