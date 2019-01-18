from statistics import mean, median ,stdev
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import numpy as np
import pandas as pd
import sys

plt.style.use('default')
sns.set()
sns.set_style('whitegrid')
sns.set_palette('Set1')

args = sys.argv
methods = ["naive_grid_pcam", "passive_grid_pcam"]
cam_nums = ["num_5", "num_10", "num_15"]
map_types = ["grid", "bunkyo-ku"]

simTotalInterval = 15


print("this is summary of all\n")

for map_type in map_types:
    analysis_root_path = "analysis/" + map_type + "/"
    for method in methods:
        for cam_num in cam_nums:
            sim_from = 205
            sim_to = 210
            queue_ratios = []
            for sim_num in range(100):
                with open(analysis_root_path + method + "/" + cam_num + "/sim_" + str(sim_num) + "/queue_ratio.txt") as f:
                    queue_ratio_lines = f.readlines()
                for queue_ratio_line in queue_ratio_lines[1:]:
                    if float(queue_ratio_line.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(queue_ratio_line.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                        if not np.isnan(float(queue_ratio_line.split("\t")[1])):
                            queue_ratios.append(float(queue_ratio_line.split("\t")[1]))
            print("method: " + method + ", cam_num: " + cam_num + "\tqueue_ratio: " + str(mean(queue_ratios)))
