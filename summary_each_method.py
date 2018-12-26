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
method = args[1]

sim_from = 205
sim_to = 210

cam_nums = ["num_5", "num_10", "num_15"]
pcam_pos_slants = [0,8,16,24]
pcam_pos_crosses = [21,22,23,24]

if not (method == "original_pcam" or method == "naive_grid_pcam" or method == "passive_grid_pcam"):
    print("error unknown method")
    sys.exit()

analysis_root_path = "analysis/" + method + "/"

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

for cam_num in cam_nums:
    pdrs_slants = []
    delays_slants = []
    delay_errors_slants = []
    for pos in pcam_pos_slants:
        with open(analysis_root_path + cam_num + "/pdr_" + str(pos) + ".txt") as f:
            pdrlines = f.readlines()
        for pdrline in pdrlines[1:]:
            if float(pdrline.split("\t")[0]) > sim_from and float(pdrline.split("\t")[0]) < sim_to:
                pdrs.append(float(pdrline.split("\t")[1]))
        with open(analysis_root_path + cam_num + "/delay_" + str(pos) + ".txt") as f:
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
    all_delay_errors_slants.appne(delay_errors_slants)

for cam_num in cam_nums:
    pdrs_crosses = []
    delays_crosses = []
    delay_errors_crosses = []
    for pos in pcam_pos_crosses:
        with open(analysis_root_path + cam_num + "/pdr_" + str(pos) + ".txt") as f:
            pdrlines = f.readlines()
        for pdrline in pdrlines[1:]:
            if float(pdrline.split("\t")[0]) > sim_from and float(pdrline.split("\t")[0]) < sim_to:
                pdrs.append(float(pdrline.split("\t")[1]))
        with open(analysis_root_path + cam_num + "/delay_" + str(pos) + ".txt") as f:
            delaylines = f.readlines()
        for delayline in delaylines[1:]:
            if float(delayline.split("\t")[0]) > sim_from and float(delayline.split("\t")[0]) < sim_to:
                delays.append(float(delayline.split("\t")[1]))
                delay_errors.append(float(delayline.split("\t")[2]))
        print(pos, mean(pdrs), mean(delays))
        pdrs_crosses.append(mean(pdrs))
        delays_crosses.append(mean(delays))
        delay_errors_crosses.appen(mean(delay_errors))
    all_pdrs_crosses.append(pdrs_crosses)
    all_delays_crosses.append(delays_crosses)
    all_delay_errors_crosses.append(delay_errors_crosses)

# slantsのpdr
fig_pdr = plt.figure()
ax = fig_pdr.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_pdrs_slants[0]) + 1))

df = pd.DataFrame({
    "x": x, cam_nums[0]: all_pdrs_slants[0], cam_nums[1]: all_pdrs_slants[1], cam_nums[2]: all_pdrs_slants[2]
})

ax.plot('x', cam_nums[0], data=df, label='PPS 5', marker='o')
ax.plot('x', cam_nums[1], data=df, label='PPS 10', marker='o')
ax.plot('x', cam_nums[2], data=df, label='PPS 15', marker='o')

ax.legend()
ax.set_xlabel("hop num")
ax.set_ylabel("PDR")
ax.set_ylim(0, 1)
plt.title("method: " + method + " slant")

pp = PdfPages("summary/method_" + method + "_pdr_slant.pdf")
pp.savefig(fig)
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
ax.setylim(0,100)
plt.title("method: " + method + " slant")

pp = PdfPages("summary/method_" + method + "_delay_slant.pdf")
pp.savefig(fig)
pp.close()



# crossesのpdr
fig_pdr = plt.figure()
ax = fig_pdr.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_pdrs_crosses[0]) + 1))

df = pd.DataFrame({
    "x": x, cam_nums[0]: all_pdrs_crosses[0], cam_nums[1]: all_pdrs_crosses[1], cam_nums[2]: all_pdrs_crosses[2]
})

ax.plot('x', cam_nums[0], data=df, label='PPS 5', marker='o')
ax.plot('x', cam_nums[1], data=df, label='PPS 10', marker='o')
ax.plot('x', cam_nums[2], data=df, label='PPS 15', marker='o')

ax.legend()
ax.set_xlabel("hop num")
ax.set_ylabel("PDR")
ax.set_ylim(0, 1)
plt.title("method: " + method + " cross")

pp = PdfPages("summary/method_" + method + "_pdr_cross.pdf")
pp.savefig(fig)
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
ax.setylim(0,100)
plt.title("method: " + method + " cross")

pp = PdfPages("summary/method_" + method + "_delay_cross.pdf")
pp.savefig(fig)
pp.close()
