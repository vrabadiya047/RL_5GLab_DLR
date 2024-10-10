import pickle
import matplotlib.pyplot as plt
from matplotlib import axes
from typing import Dict, Tuple
from math import ceil

SPEED_AGG_RANGE = 14 / 7

OBJ = [
    'plain_1_2_2_10_1_0',
    'plain_1_2_3_10_1_0',
    'plain_1_2_4_10_1_0',
    'plain_1_2_5_10_1_0',
    'H1.00',
    # 'AI',
    'H0.75',
    'H0.50',
    'H0.25',
    'H0.00',
]

MIN_SPEED = 0
AVG_VEH = 1
NUM_REQ = 2

data = dict()
for f in OBJ:
    with open('tmp/' + f + '.pickle', 'rb') as file:
        data[f] = pickle.load(file)


def plot(title: str, result_type: int) -> None:
    lineprops = {'linewidth': 2}
    plt.title(title)
    plt.boxplot([data[f][result_type] for f in OBJ], boxprops=lineprops, whiskerprops=lineprops, medianprops=lineprops,
                capprops=lineprops)
    plt.xticks(list(range(1, len(OBJ) + 1)), [f for f in OBJ])
    plt.grid(axis='y')
    plt.show()
    return None


def plot_bar(data_type, topend: int = 14, title: str = "", aggrange: float = 1.0, ylim: float = 1.0) -> None:
    def aggregate(f, agg_range, data_type: int, topend=14) -> Dict[Tuple[float, float], int]:
        res = dict()
        for i in range(0, ceil(topend / agg_range)):
            res[(agg_range * i, agg_range * (i + 1))] = 0
        for date in data[f][data_type]:
            for key in res:
                if key[0] <= date and key[1] > date:
                    res[key] += 1
                    break
        return res

    def aggregate_all(agg_range, data_type: int, topend=14) -> Dict[str, Dict[Tuple[float, float], int]]:
        res = dict()
        for obj in OBJ:
            res[obj] = aggregate(obj, agg_range, data_type, topend)
        return res

    def bar(s_agg: Dict[Tuple[float, float], int], ax: axes.Axes, title: str, normalizer: int, ylim=1) -> None:
        sorted_key = sorted(s_agg.keys())
        xs = [str(key) for key in sorted_key]
        ax.bar(xs, [s_agg[key] / normalizer for key in sorted_key])
        ax.set_ylim([0, ylim])
        ax.tick_params(labelsize=8)
        ax.set_title(title, size=8)
        ax.grid(axis='y')

    agg = aggregate_all(aggrange, data_type, topend)
    num_samples = sum(list(agg.values())[0].values())
    fig, axs = plt.subplots(len(agg), 1)
    fig.suptitle(title)
    for i in range(len(agg)):
        key = list(agg.keys())[i]
        bar(agg[key], axs if len(agg) == 1 else axs[i], key, num_samples, ylim=ylim)
    plt.show()
    return None


plot('min speed ev', MIN_SPEED)
plot('avg waiting veh', AVG_VEH)
plot('num requests', NUM_REQ)
plot_bar(MIN_SPEED, 14, 'relative speed distribution', SPEED_AGG_RANGE, 0.5)
plot_bar(NUM_REQ, 10, 'relative num requests distribution', 1, 1)
