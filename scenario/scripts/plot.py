from enum import Enum, unique
import matplotlib.pyplot as plt
import csv
import statistics as stats
import os

INPUT_FILE="output.csv"

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
INPUT_FILE_PATH = os.path.join(THIS_DIR, "..\\output\\", INPUT_FILE)


@unique
class ID(Enum):
    TIME        = 0
    PHASE       = 1
    TRANS       = 2
    DUR         = 3
    NUM_VEH     = 4
    VEH_INT     = 5
    VEH_WAIT    = 6
    EV_DIST     = 7
    EV_SPEED    = 8
    SEED        = 9

TIME_BEFORE_END = 90
SAMPLE_TIME_STEPS = [i*300 for i in range(1,11)]
END_TIME = SAMPLE_TIME_STEPS[-1] + TIME_BEFORE_END
FIRECAR_STEP = END_TIME - TIME_BEFORE_END
LAST_DOCUMENTATION_STEP = FIRECAR_STEP + 75
SAMPLE_TIME_STEPS.append(LAST_DOCUMENTATION_STEP)
TIMES = SAMPLE_TIME_STEPS

def init_dict():
    d = {}
    for t in TIMES:
        d[t] = {}
        for id in ID:
            d[t][id] = []
    return d

def read_row(row,data):
    for id in ID:
        data[int(row[ID.TIME.value])][id].append(float(row[id.value]))
        
def cumulateData(data, id: ID):
    cumulatedData = []
    for key in data.keys():
        date = data[key]
        cumulatedData.append(date[id])
    return cumulatedData

def cumulatePhaseData(data):
    counts = {}
    durations = {}
    for key in data.keys():
        if not key in counts:
            durations[key] = {}
            counts[key] = {}
        date = data[key]
        
        for i in range(len(date[ID.PHASE])):
            phase_key = (date[ID.PHASE][i], date[ID.TRANS][i])
            if not phase_key in counts[key]:
                counts[key][phase_key] = 0
                durations[key][phase_key] = []
            counts[key][phase_key]+=1
            durations[key][phase_key].append(date[ID.DUR][i])
    return counts, durations
            
def plotData(figure_name: str, data, id: ID):
    num_veh_data = cumulateData(data,id)
    plt.figure(figure_name)    
    plt.boxplot(num_veh_data)
    plt.show()

data = init_dict()
with open(INPUT_FILE_PATH) as file:
    reader = csv.reader(file, delimiter=";")
    for row in reader:
        read_row(row,data)

counts, durations = cumulatePhaseData(data)

for time_key in counts:
    print(time_key)
    for key in counts[time_key]:
        durs = durations[time_key][key]
        print(key, "\t%i\t%.1f\t%.1f\t%.1f\t%.1f"%(counts[time_key][key],stats.mean(durs), stats.median(durs), min(durs), max(durs)))

plotData("number of vehicles in the network", data, ID.NUM_VEH)
plotData("number of vehicles at the intersection", data, ID.VEH_INT)
plotData("number of vehicles waiting from south to north", data, ID.VEH_WAIT)
plotData("distance of emergency vehicle from intersection", data, ID.EV_DIST)
plotData("speed of emergency vehicle", data, ID.EV_SPEED)