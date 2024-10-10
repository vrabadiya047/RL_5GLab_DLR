#!/usr/bin/env python3

import os, sys
from optparse import OptionParser
from constants import TRIPINFOS_DEFAULT, END_TIME_DEFAULT, STEPLENGTH_DEFAULT
from demand import FLOW_DIRECTIONS
from k048.control import Siemens
import random

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci


def read_commandline_arguments():
    optParser = OptionParser(usage="Usage: %s [options]" % sys.argv[0])
    optParser.add_option("--sumo", help="sumo or sumo-gui", dest="sumo_exe")
    optParser.add_option("--end_time", type=float, default=END_TIME_DEFAULT, dest="end_time")
    optParser.add_option("--step_length", type=float, default=STEPLENGTH_DEFAULT, dest="step_length")
    options, _ = optParser.parse_args()

    # from command line, default is gui
    if options.sumo_exe is None:
        options.sumo_exe = "sumo-gui"

    # set complete sumo path
    if "SUMO_HOME" in os.environ:
        options.sumo_exe = os.path.join(os.environ["SUMO_HOME"], 'bin', options.sumo_exe)
    return options


def run_sumo(sumo_exe, end_time=END_TIME_DEFAULT, step_length=STEPLENGTH_DEFAULT):
    junction_control = Siemens(use_gui=True)

    sumo_cmd = [sumo_exe, "-c", "tostmannplatz.sumocfg",
                # "--tripinfo-output", TRIPINFOS_DEFAULT,
                "--no-step-log", "true",
                "-W",
                "--duration-log.disable",
                # "--quit-on-end",
                ]

    traci.start(sumo_cmd)
    step = 0
    # firecar_step = random.randrange(0,end_time,step_length)
    firecar_step = 1000
    print("Firecar starts at %is." % int(firecar_step / step_length))
    endstep = end_time / step_length
    while step < endstep:
        t = step * step_length
        if step == firecar_step:
            traci.route.add('firecar_route', [FLOW_DIRECTIONS[7][0], FLOW_DIRECTIONS[7][1]])
            traci.vehicle.add('firecar', 'firecar_route', 'firecar', departSpeed="max")
        # if step == firecar_step + 10:
        #     junction_control.controller.setEmergencyRequest(t, 1)
        # if step == firecar_step + 90:
        #     junction_control.controller.setEmergencyRequest(t, 0)
        junction_control.control(t)
        traci.simulationStep(t)
        step += 1
    traci.close()


if __name__ == "__main__":
    options = read_commandline_arguments()
    run_sumo(options.sumo_exe, options.end_time, options.step_length)