#!/usr/bin/env python3

import os
from demand import create_route_file
from run_sumo import run_sumo
from constants import END_TIME_DEFAULT, STEPLENGTH_DEFAULT

# base flow splits: NW NS NE EN EW ES SE SN SW WS WE WN
SPLITS = [
    [40, 200, 10, 5, 1, 5, 10, 200, 40, 10, 1, 10],
    [10, 200, 10, 5, 1, 5, 10, 200, 10, 40, 1, 40],
]
# flow factors
FACTORS = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5]


def run(sumo_exe):
    num_scen = len(FACTORS) * len(SPLITS)
    i = 0
    for split in SPLITS:
        for factor in FACTORS:
            i += 1
            print("Running scenario %i/%i:" % (i, num_scen))
            print("Creating route files...")
            flows = [factor * float(s) for s in split]
            create_route_file(flows, END_TIME_DEFAULT)
            print("Running simulation...")
            run_sumo(sumo_exe, END_TIME_DEFAULT, STEPLENGTH_DEFAULT)
            print("Processing simulation results...\n")
            # process


if __name__ == "__main__":
    sumo_exe = os.path.join(os.environ["SUMO_HOME"], 'bin', 'sumo')
    run(sumo_exe)
