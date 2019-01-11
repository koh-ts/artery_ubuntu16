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
methods = ["original_pcam", "naive_grid_pcam", "passive_grid_pcam"]
cam_nums = ["num_5", "num_10", "num_15"]
map_type = "bunkyo-ku"

pcam_nums = range(49)

rsu_pos = np.array([700,1155])

pcam_poss = np.array([
    [700,1155],
    [750,1450],
    [810,1510],
    [965,1650],
    [1185,1830],
    [1240,1680],
    [1500,1680],
    [870,1345],
    [1060,1385],
    [1300,1460],
    [1530,1490],
    [890,1260],
    [1070,1285],
    [920,1155],
    [1100,1175],
    [1295,1140],
    [1540,1275],
    [1545,1180],
    [1540,1075],
    [550,280],
    [805,245],
    [1120,5],
    [720,1360],
    [535,210],
    [5,730],
    [200,710],
    [380,490],
    [470,1165],
    [385,1170],
    [275,1160],
    [70,1040],
    [600,540],
    [95,1170],
    [535,1405],
    [445,1430],
    [355,1450],
    [555,1500],
    [470,1520],
    [150,1380],
    [1540,960],
    [1240,140],
    [1305,265],
    [1370,385],
    [1425,605],
    [1445,845],
    [220,1710],
    [820,1785],
    [1135,1945],
    [905,190]
])
for i in range(len(pcam_poss)):
    print(i, np.linalg.norm(rsu_pos - pcam_poss[i]))

pcam_poss = pcam_poss[pcam_nums]

pcam_num_pos = zip(pcam_poss, pcam_nums)
pcam_num_pos = sorted(pcam_num_pos, key=lambda x: np.linalg.norm(rsu_pos - x[0]))

pcam_poss = [pos for pos,num in pcam_num_pos]
pcam_nums = [num for pos,num in pcam_num_pos]

for i in range(len(pcam_poss)):
    print(pcam_nums[i], pcam_poss[i],np.linalg.norm(rsu_pos - pcam_poss[i]))


simTotalInterval = 15

analysis_root_path = "analysis/" + map_type + "/"

print("this is summary of all\n")

all_pdrs = []
all_delays = []

all_pdrs_los = []
all_delays_los = []


for method in methods:
    print("entering method", method)
    for cam_num in cam_nums:
        print("entering cam_num: ", cam_num)
        pdrs_all_num = []
        delays_all_num = []
        for num in pcam_nums:
            pdrs = []
            delays = []
            sim_from = 205
            sim_to = 210
            for sim_num in range(47):
                with open(analysis_root_path + method + "/" + cam_num + "/sim_" + str(sim_num) + "/pdr_" + str(num) + ".txt") as f:
                    pdrlines = f.readlines()
                for pdrline in pdrlines[1:]:
                    if float(pdrline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(pdrline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                        pdrs.append(float(pdrline.split("\t")[1]))
                with open(analysis_root_path + method + "/" + cam_num + "/sim_" + str(sim_num) + "/delay_" + str(num) + ".txt") as f:
                    delaylines = f.readlines()
                for delayline in delaylines[1:]:
                    if float(delayline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(delayline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                        if not np.isnan(float(delayline.split("\t")[1])):
                            delays.append(float(delayline.split("\t")[1]))
            pdrs_all_num.append(pdrs)
            delays_all_num.append(delays)
        all_pdrs.append(pdrs_all_num)
        all_delays.append(delays_all_num)

# pdr
fig_pdr = plt.figure(figsize=(13,5), dpi= 300)
ax = fig_pdr.add_subplot(1, 1, 1)

x = []
for i in range(len(pcam_poss)):
    x.append(np.linalg.norm(rsu_pos - pcam_poss[i]))

plt.subplots_adjust(right=0.5)

ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]], marker='D', label='Original PCAM (PPS: 50)', capthick=1, capsize=8, lw=2, color="indigo")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]], marker='^', label='Original PCAM (PPS: 100)', capthick=1, capsize=8, lw=2, color="hotpink")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]], marker='x', label='Original PCAM (PPS: 150)', capthick=1, capsize=8, lw=2, color="red")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]], marker='s', label='Non priority Grid PCAM (PPS: 50)', capthick=1, capsize=8, lw=2, color="darkorange", linestyle="-.")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]], marker='>', label='Non priority Grid PCAM (PPS: 100)', capthick=1, capsize=8, lw=2, color="purple", linestyle="-.")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]], marker='h', label='Non priority Grid PCAM (PPS: 150)', capthick=1, capsize=8, lw=2, color="teal", linestyle="-.")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]], marker='d', label='Distance priority Grid PCAM (PPS: 50)', capthick=1, capsize=8, lw=2, color="limegreen", linestyle=":")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]], marker='p', label='Distance priority Grid PCAM (PPS: 100)', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle=":")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]], marker='o', label='Distance priority Grid PCAM (PPS: 150)', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")

ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=18)
ax.set_xlabel("distance (m)")
ax.set_ylabel("PDR")
ax.set_ylim(-0.1, 1.1)

pp = PdfPages("summary/" + map_type + "/sim_all/pdr.pdf")
pp.savefig(fig_pdr)
pp.close()

# delay
fig_delay = plt.figure(figsize=(13,5), dpi= 300)
ax = fig_delay.add_subplot(1, 1, 1)
plt.subplots_adjust(right=0.5)

ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[0]], marker='D', label='Original PCAM (PPS: 50)', capthick=1, capsize=8, lw=2, color="indigo")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[1]], marker='^', label='Original PCAM (PPS: 100)', capthick=1, capsize=8, lw=2, color="hotpink")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[2]], marker='x', label='Original PCAM (PPS: 150)', capthick=1, capsize=8, lw=2, color="red")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]], marker='s', label='Non priority Grid PCAM (PPS: 50)', capthick=1, capsize=8, lw=2, color="darkorange", linestyle="-.")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]], marker='>', label='Non priority Grid PCAM (PPS: 100)', capthick=1, capsize=8, lw=2, color="purple", linestyle="-.")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]], marker='h', label='Non priority Grid PCAM (PPS: 150)', capthick=1, capsize=8, lw=2, color="teal", linestyle="-.")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]], marker='d', label='Distance priority Grid PCAM (PPS: 50)', capthick=1, capsize=8, lw=2, color="limegreen", linestyle=":")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]], marker='p', label='Distance priority Grid PCAM (PPS: 100)', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle=":")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]], marker='o', label='Distance priority Grid PCAM (PPS: 150)', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")

ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=18)
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Delay (ms)")
ax.set_ylim(-150,500)

pp = PdfPages("summary/" + map_type + "/sim_all/delay.pdf")
pp.savefig(fig_delay)
pp.close()
