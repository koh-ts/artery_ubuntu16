from statistics import mean, median,variance,stdev
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
cam_num = int(args[1])
map_type = "grid"

methods = ["original_pcam", "naive_grid_pcam", "passive_grid_pcam"]
pcam_pos_slants = [24, 16, 8, 0]
pcam_pos_crosses = [24, 23, 22, 21]

simTotalInterval = 15

if not (cam_num == 5 or cam_num == 10 or cam_num == 15):
    print("error unknown cam_num")
    sys.exit()

analysis_root_path = "analysis/" + map_type + "/"

print("this is summary of ", str(cam_num) + "\n")

# ここにはnum_*のslants,crossesが入る
all_pdrs_slants = []
all_delays_slants = []
all_delay_errors_slants = []

all_pdrs_crosses = []
all_delays_crosses = []
all_delay_errors_crosses = []


print("entering slants")

for method in methods:
    print("entering method: ", method)
    pdrs_slants = []
    delays_slants = []
    delay_errors_slants = []
    for pos in pcam_pos_slants:
        pdrs = []
        delays = []
        delay_errors = []
        sim_from = 205
        sim_to = 210
        for sim_num in range(100):
            with open(analysis_root_path + method + "/num_" + str(cam_num) + "/sim_" + str(sim_num) + "/pdr_" + str(pos) + ".txt") as f:
                pdrlines = f.readlines()
            for pdrline in pdrlines[1:]:
                if float(pdrline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(pdrline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                    pdrs.append(float(pdrline.split("\t")[1]))
            with open(analysis_root_path + method + "/num_" + str(cam_num) + "/sim_" + str(sim_num) + "/delay_" + str(pos) + ".txt") as f:
                delaylines = f.readlines()
            for delayline in delaylines[1:]:
                if float(delayline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(delayline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                    if not np.isnan(float(delayline.split("\t")[1])):
                        delays.append(float(delayline.split("\t")[1]))
                    if not np.isnan(float(delayline.split("\t")[2])):
                        delay_errors.append(float(delayline.split("\t")[2]))
        if len(pdrs) < 2:
            avg_pdr = 0
        else:
            avg_pdr = mean(pdrs)
        if len(delays) < 2:
            avg_delay = -100
            avg_delay_error = 0
        else:
            avg_delay = mean(delays)
            avg_delay_error = mean(delay_errors)
        print(pos, avg_pdr, avg_delay, avg_delay_error)
        pdrs_slants.append(avg_pdr)
        delays_slants.append(avg_delay)
        delay_errors_slants.append(avg_delay_error)

    all_pdrs_slants.append(pdrs_slants)
    all_delays_slants.append(delays_slants)
    all_delay_errors_slants.append(delay_errors_slants)

print("entering crosses")

for method in methods:
    print("entering method: ", method)
    pdrs_crosses = []
    delays_crosses = []
    delay_errors_crosses = []
    for pos in pcam_pos_crosses:
        pdrs = []
        delays = []
        delay_errors = []
        sim_from = 205
        sim_to = 210
        for sim_num in range(100):
            with open(analysis_root_path + method + "/num_" + str(cam_num) + "/sim_" + str(sim_num) + "/pdr_" + str(pos) + ".txt") as f:
                pdrlines = f.readlines()
            for pdrline in pdrlines[1:]:
                if float(pdrline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(pdrline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                    pdrs.append(float(pdrline.split("\t")[1]))
            with open(analysis_root_path + method + "/num_" + str(cam_num) + "/sim_" + str(sim_num) + "/delay_" + str(pos) + ".txt") as f:
                delaylines = f.readlines()
            for delayline in delaylines[1:]:
                if float(delayline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(delayline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                    if not np.isnan(float(delayline.split("\t")[1])):
                        delays.append(float(delayline.split("\t")[1]))
                    if not np.isnan(float(delayline.split("\t")[2])):
                        delay_errors.append(float(delayline.split("\t")[2]))
        if len(pdrs) < 2:
            avg_pdr = 0
        else:
            avg_pdr = mean(pdrs)
        if len(delays) < 2:
            avg_delay = -100
            avg_delay_error = 0
        else:
            avg_delay = mean(delays)
            avg_delay_error = mean(delay_errors)
        print(pos, avg_pdr, avg_delay, avg_delay_error)
        pdrs_crosses.append(avg_pdr)
        delays_crosses.append(avg_delay)
        delay_errors_crosses.append(avg_delay_error)
    all_pdrs_crosses.append(pdrs_crosses)
    all_delays_crosses.append(delays_crosses)
    all_delay_errors_crosses.append(delay_errors_crosses)

# slantsのpdr
fig_pdr = plt.figure()
ax = fig_pdr.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_pdrs_slants[0]) + 1))

df = pd.DataFrame({
    "x": x, methods[0]: all_pdrs_slants[0], methods[1]: all_pdrs_slants[1], methods[2]: all_pdrs_slants[2]
})

ax.plot('x', methods[0], data=df, label='original pcam', marker='o')
ax.plot('x', methods[1], data=df, label='naive grid pcam', marker='o')
ax.plot('x', methods[2], data=df, label='passive grid pcam', marker='o')

ax.legend()
ax.set_xlabel("hop num")
ax.set_ylabel("PDR")
ax.set_ylim(-0.1, 1.1)
plt.xticks(np.arange(1,x.size + 1))
plt.title("cam_num: " + str(cam_num) + " slant")

pp = PdfPages("summary/" + map_type + "/sim_all/cam_num_" + str(cam_num) + "_pdr_slant.pdf")
pp.savefig(fig_pdr)
pp.close()


# slantsのdelay
fig_delay = plt.figure()
ax = fig_delay.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_delays_slants[0]) + 1))

ax.errorbar(x, all_delays_slants[0], yerr=all_delay_errors_slants[0], marker='o', label='original pcam', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_slants[1], yerr=all_delay_errors_slants[1], marker='o', label='naive grid pcam', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_slants[2], yerr=all_delay_errors_slants[2], marker='o', label='passive grid pcam', capthick=1, capsize=8, lw=1)

ax.legend()
ax.set_xlabel("hop num")
ax.set_ylabel("delay")
ax.set_ylim(-150,400)
plt.xticks(np.arange(1,x.size + 1))
plt.title("cam_num: " + str(cam_num) + " slant")

pp = PdfPages("summary/" + map_type + "/sim_all/cam_num_" + str(cam_num) + "_delay_slant.pdf")
pp.savefig(fig_delay)
pp.close()



# crossesのpdr
fig_pdr = plt.figure()
ax = fig_pdr.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_pdrs_crosses[0]) + 1))

df = pd.DataFrame({
    "x": x, methods[0]: all_pdrs_crosses[0], methods[1]: all_pdrs_crosses[1], methods[2]: all_pdrs_crosses[2]
})

ax.plot('x', methods[0], data=df, label='original pcam', marker='o')
ax.plot('x', methods[1], data=df, label='naive grid pcam', marker='o')
ax.plot('x', methods[2], data=df, label='passive grid pcam', marker='o')

ax.legend()
ax.set_xlabel("hop num")
ax.set_ylabel("PDR")
ax.set_ylim(-0.1, 1.1)
plt.xticks(np.arange(1,x.size + 1))
plt.title("cam_num: " + str(cam_num) + " cross")

pp = PdfPages("summary/" + map_type + "/sim_all/cam_num_" + str(cam_num) + "_pdr_cross.pdf")
pp.savefig(fig_pdr)
pp.close()



# crossesのdelay
fig_delay = plt.figure()
ax = fig_delay.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_delays_crosses[0]) + 1))

ax.errorbar(x, all_delays_crosses[0], yerr=all_delay_errors_crosses[0], marker='o', label='original pcam', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_crosses[1], yerr=all_delay_errors_crosses[1], marker='o', label='naive grid pcam', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_crosses[2], yerr=all_delay_errors_crosses[2], marker='o', label='passive grid pcam', capthick=1, capsize=8, lw=1)

ax.legend()
ax.set_xlabel("hop num")
ax.set_ylabel("delay")
ax.set_ylim(-150,400)
plt.xticks(np.arange(1,x.size + 1))
plt.title("cam_num: " + str(cam_num) + " cross")

pp = PdfPages("summary/" + map_type + "/sim_all/cam_num_" + str(cam_num) + "_delay_cross.pdf")
pp.savefig(fig_delay)
pp.close()
