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

sim_from = 205
sim_to = 210

methods = ["original_pcam", "naive_grid_pcam", "passive_grid_pcam"]
pcam_pos_slants = [0,8,16,24]
pcam_pos_crosses = [21,22,23,24]

if not (cam_num == 5 or cam_num == 10 or cam_num == 15):
    print("error unknown cam_num")
    sys.exit()

analysis_root_path = "analysis/"

# ここにはnum_*のslants,crossesが入る
all_pdrs_slants = []
all_delays_slants = []
all_delay_errors_slants = []

all_pdrs_crosses = []
all_delays_crosses = []
all_delay_errors_crosses = []

pdrs = []
delays = []
delay_errors = []

for method in methods:
    pdrs_slants = []
    delays_slants = []
    delay_errors_slants = []
    for pos in pcam_pos_slants:
        with open(analysis_root_path + method + "/num_" + str(cam_num) + "/pdr_" + str(pos) + ".txt") as f:
            pdrlines = f.readlines()
        for pdrline in pdrlines[1:]:
            if float(pdrline.split("\t")[0]) > sim_from and float(pdrline.split("\t")[0]) < sim_to:
                pdrs.append(float(pdrline.split("\t")[1]))
        with open(analysis_root_path + method + "/num_" + str(cam_num) + "/delay_" + str(pos) + ".txt") as f:
            delaylines = f.readlines()
        for delayline in delaylines[1:]:
            print(delayline)
            if float(delayline.split("\t")[0]) > sim_from and float(delayline.split("\t")[0]) < sim_to:
                delays.append(float(delayline.split("\t")[1]))
                delay_errors.append(float(delayline.split("\t")[2]))
        print(pos, mean(pdrs), mean(delays), mean(delay_errors))
        pdrs_slants.append(mean(pdrs))
        delays_slants.append(mean(delays))
        delay_errors_slants.append(mean(delay_errors))

    all_pdrs_slants.append(pdrs_slants)
    all_delays_slants.append(delays_slants)
    all_delay_errors_slants.append(delay_errors_slants)

for cam_num in method:
    pdrs_crosses = []
    delays_crosses = []
    delay_errors_crosses = []
    for pos in pcam_pos_crosses:
        with open(analysis_root_path + method + "/num_" + str(cam_num) + "/pdr_" + str(pos) + ".txt") as f:
            pdrlines = f.readlines()
        for pdrline in pdrlines[1:]:
            if float(pdrline.split("\t")[0]) > sim_from and float(pdrline.split("\t")[0]) < sim_to:
                pdrs.append(float(pdrline.split("\t")[1]))
        with open(analysis_root_path + method + "/num_" + str(cam_num) + "/delay_" + str(pos) + ".txt") as f:
            delaylines = f.readlines()
        for delayline in delaylines[1:]:
            if float(delayline.split("\t")[0]) > sim_from and float(delayline.split("\t")[0]) < sim_to:
                delays.append(float(delayline.split("\t")[1]))
                delay_errors.append(float(delayline.split("\t")[2]))
        print(pos, mean(pdrs), mean(delays))
        pdrs_crosses.append(mean(pdrs))
        delays_crosses.append(mean(delays))
        delay_errors_crosses.append(mean(delay_errors))
    all_pdrs_crosses.append(pdrs_crosses)
    all_delays_crosses.append(delays_crosses)
    all_delay_errors_crosses.append(delay_errors_crosses)

# slantsのpdr
fig_pdr = plt.figure()
ax = fig_pdr.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_pdrs_slants[0]) + 1))

df = pd.DataFrame({
    "x": x, method[0]: all_pdrs_slants[0], method[1]: all_pdrs_slants[1], method[2]: all_pdrs_slants[2]
})

ax.plot('x', method[0], data=df, label='PPS 5', marker='o')
ax.plot('x', method[1], data=df, label='PPS 10', marker='o')
ax.plot('x', method[2], data=df, label='PPS 15', marker='o')

ax.legend()
ax.set_xlabel("hop num")
ax.set_ylabel("PDR")
ax.set_ylim(0, 1)
plt.title("cam_num: " + str(cam_num) + " slant")

pp = PdfPages("summary/cam_num_" + str(cam_num) + "_pdr_slant.pdf")
pp.savefig(fig_pdr)
pp.close()


# slantsのdelay
fig_delay = plt.figure()
ax = fig_delay.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_delays_slants[0]) + 1))

ax.errorbar(x, all_delays_slants[0], yerr=all_delay_errors_slants[0], marker='o', label='PPS 5', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_slants[1], yerr=all_delay_errors_slants[1], marker='o', label='PPS 10', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_slants[2], yerr=all_delay_errors_slants[2], marker='o', label='PPS 15', capthick=1, capsize=8, lw=1)

ax.legend()
ax.set_xlabel("hop num")
ax.set_ylabel("delay")
ax.set_ylim(0,100)
plt.title("cam_num: " + str(cam_num) + " slant")

pp = PdfPages("summary/cam_num_" + str(cam_num) + "_delay_slant.pdf")
pp.savefig(fig_delay)
pp.close()



# crossesのpdr
fig_pdr = plt.figure()
ax = fig_pdr.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_pdrs_crosses[0]) + 1))

df = pd.DataFrame({
    "x": x, method[0]: all_pdrs_crosses[0], method[1]: all_pdrs_crosses[1], method[2]: all_pdrs_crosses[2]
})

ax.plot('x', method[0], data=df, label='PPS 5', marker='o')
ax.plot('x', method[1], data=df, label='PPS 10', marker='o')
ax.plot('x', method[2], data=df, label='PPS 15', marker='o')

ax.legend()
ax.set_xlabel("hop num")
ax.set_ylabel("PDR")
ax.set_ylim(0, 1)
plt.title("cam_num: " + str(cam_num) + " cross")

pp = PdfPages("summary/cam_num_" + str(cam_num) + "_pdr_cross.pdf")
pp.savefig(fig_pdr)
pp.close()



# crossesのdelay
fig_delay = plt.figure()
ax = fig_delay.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_delays_crosses[0]) + 1))

ax.errorbar(x, all_delays_crosses[0], yerr=all_delay_errors_crosses[0], marker='o', label='PPS 5', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_crosses[1], yerr=all_delay_errors_crosses[1], marker='o', label='PPS 10', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_crosses[2], yerr=all_delay_errors_crosses[2], marker='o', label='PPS 15', capthick=1, capsize=8, lw=1)

ax.legend()
ax.set_xlabel("hop num")
ax.set_ylabel("delay")
ax.set_ylim(0,100)
plt.title("cam_num: " + str(cam_num) + " cross")

pp = PdfPages("summary/cam_num_" + str(cam_num) + "_delay_cross.pdf")
pp.savefig(fig_delay)
pp.close()
