from __future__ import absolute_import
from __future__ import print_function
from itertools import groupby
import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '..'))
from sumolib.output import parse  # noqa
from sumolib.miscutils import Statistics  # noqa
import xml.etree.ElementTree as ET
import pandas as pd
import seaborn as sns

# Create boxplots for all tripinfo files in folder

mypath = r"D:\CD\5G 23.06..2022\5glab-ki-control\outputs\sumo\recur_ppo_seed_None_learningrate_None_evsr_1600_1800_rew_factors_1_2_3_20_1_0_20220623-202220.zip\20220624-135626_tripinfo.xml"


def cut_data(xmlfile):
    df_cols = ["id", "duration", "depart", "waitingTime", "timeLoss"]
    rows = []
    root = ET.parse(xmlfile).getroot()
    for node in root.findall('tripinfo'):
        n_id = node.attrib.get("id")
        n_dur = float(node.attrib.get("duration"))
        n_depart = float(node.attrib.get("depart"))
        n_wait = float(node.attrib.get("waitingTime"))
        n_loss = float(node.attrib.get("timeLoss"))
        rows.append({"id": n_id, "duration": n_dur, "depart": n_depart, "waitingTime": n_wait, "timeLoss": n_loss})
    df = pd.DataFrame(rows, columns=df_cols)

    tmp = df.loc[df["id"] == "firecar"]

    tmp_df = df.loc[df.depart.values > tmp.depart.values]
    return tmp_df


def main(tag, attr, xmlfiles, mypath):
    data = []
    df_cols = ["id", "duration", "depart", "waitingTime", "timeLoss"]
    rows = []
    df = pd.DataFrame(rows, columns=df_cols)
    dfs = []
    df_keys = []
    for xmlfile in xmlfiles:
        tmp_df = cut_data(xmlfile)
        stats = Statistics('%s %s' % (tag, attr))
        for elem in parse(xmlfile, tag):
            stats.add(float(elem.getAttribute(attr)), elem.id)
        data.append(stats.values)
        dfs.append(tmp_df)

    for k in range(len(dfs)):
        df_keys.append("s" + str(k))
    df = pd.concat(dfs, keys=df_keys, names=["frame_nr", "row id"])

    try:
        import matplotlib.pyplot as plt
    except Exception as e:
        sys.exit(e)

    # plt.figure("fullstats")
    # plt.xticks(range(len(xmlfiles)), xmlfiles)
    # plt.ylabel("%s %s" % (tag, attr))
    # plt.boxplot(data)
    # save_str = mypath+str(attr)+".png"
    # plt.savefig(save_str)
    # plt.show()

    plt.figure("cut_data")
    plt.ylabel("%s %s" % (tag, attr))
    df["duration"].unstack(level=0).boxplot()
    save_str = mypath + str(attr + "_cut") + ".png"
    plt.savefig(save_str)
    plt.show()


if __name__ == "__main__":
    files_list = []
    for path, subdirs, files in os.walk(mypath):
        for name in files:
            if name.endswith(".xml"):
                files_list.append((os.path.join(path, name)))
    # print(files_list)

    #  call specific attributes, e.g. duration, waitingTime...
    main("tripinfo", "duration", files_list, mypath)
    main("tripinfo", "waitingTime", files_list, mypath)
    main("tripinfo", "timeLoss", files_list, mypath)
