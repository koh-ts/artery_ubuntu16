from statistics import mean, median,stdev
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

cam_nums = ["num_5", "num_10", "num_15"]
# map_type = "grid"
# pcam_pos_non_los = [24, 16, 8, 0]
# pcam_pos_los = [24, 23, 22, 21]

simTotalInterval = 15

if not (method == "original_pcam" or method == "naive_grid_pcam" or method == "passive_grid_pcam"):
    print("error unknown method")
    sys.exit()

analysis_root_path = "analysis/" + map_type + "/" + method + "/"

print("this is summary of ", method + "\n")

# ここにはnum_*のnon_los,losが入る
all_pdrs_non_los = []
all_delays_non_los = []
all_delay_errors_non_los = []

all_pdrs_los = []
all_delays_los = []
all_delay_errors_los = []

print("entering non_los")

for cam_num in cam_nums:
    print("entering cam_num: ", cam_num)
    pdrs_non_los = []
    delays_non_los = []
    delay_errors_non_los = []
    for pos in pcam_pos_non_los:
        pdrs = []
        delays = []
        delay_errors = []
        sim_from = 205
        sim_to = 210
        for sim_num in range(100):
            with open(analysis_root_path + cam_num + "/sim_" + str(sim_num) + "/pdr_" + str(pos) + ".txt") as f:
                pdrlines = f.readlines()
            for pdrline in pdrlines[1:]:
                if float(pdrline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(pdrline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                    pdrs.append(float(pdrline.split("\t")[1]))
            with open(analysis_root_path + cam_num + "/sim_" + str(sim_num) + "/delay_" + str(pos) + ".txt") as f:
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
        pdrs_non_los.append(avg_pdr)
        delays_non_los.append(avg_delay)
        delay_errors_non_los.append(avg_delay_error)

    all_pdrs_non_los.append(pdrs_non_los)
    all_delays_non_los.append(delays_non_los)
    all_delay_errors_non_los.append(delay_errors_non_los)

print("entering los")

for cam_num in cam_nums:
    print("entering cam_num: ", cam_num)
    pdrs_los = []
    delays_los = []
    delay_errors_los = []
    for pos in pcam_pos_los:
        pdrs = []
        delays = []
        delay_errors = []
        sim_from = 205
        sim_to = 210
        for sim_num in range(100):
            with open(analysis_root_path + cam_num + "/sim_" + str(sim_num) + "/pdr_" + str(pos) + ".txt") as f:
                pdrlines = f.readlines()
            for pdrline in pdrlines[1:]:
                if float(pdrline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(pdrline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                    pdrs.append(float(pdrline.split("\t")[1]))
            with open(analysis_root_path + cam_num + "/sim_" + str(sim_num) + "/delay_" + str(pos) + ".txt") as f:
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
        pdrs_los.append(avg_pdr)
        delays_los.append(avg_delay)
        delay_errors_los.append(avg_delay_error)
    all_pdrs_los.append(pdrs_los)
    all_delays_los.append(delays_los)
    all_delay_errors_los.append(delay_errors_los)

# non_losのpdr
fig_pdr = plt.figure()
ax = fig_pdr.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_pdrs_non_los[0]) + 1))

df = pd.DataFrame({
    "x": x, cam_nums[0]: all_pdrs_non_los[0], cam_nums[1]: all_pdrs_non_los[1], cam_nums[2]: all_pdrs_non_los[2]
})

ax.plot('x', cam_nums[0], data=df, label='PPS 50', marker='o')
ax.plot('x', cam_nums[1], data=df, label='PPS 100', marker='o')
ax.plot('x', cam_nums[2], data=df, label='PPS 150', marker='o')

ax.legend()
ax.set_xlabel("distance")
ax.set_ylabel("PDR")
ax.set_ylim(-0.1, 1.1)
plt.xticks(np.arange(1,x.size + 1))
plt.title("method: " + method + " non line of sight")

pp = PdfPages("summary/" + map_type + "/sim_all/method_" + method + "_pdr_non_los.pdf")
pp.savefig(fig_pdr)
pp.close()




# non_losのdelay
fig_delay = plt.figure()
ax = fig_delay.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_delays_non_los[0]) + 1))

ax.errorbar(x, all_delays_non_los[0], yerr=all_delay_errors_non_los[0], marker='o', label='PPS 50', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_non_los[1], yerr=all_delay_errors_non_los[1], marker='o', label='PPS 100', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_non_los[2], yerr=all_delay_errors_non_los[2], marker='o', label='PPS 150', capthick=1, capsize=8, lw=1)

ax.legend()
ax.set_xlabel("distance")
ax.set_ylabel("delay")
ax.set_ylim(-150,400)
plt.xticks(np.arange(1,x.size + 1))
plt.title("method: " + method + " non line of sight")

pp = PdfPages("summary/" + map_type + "/sim_all/method_" + method + "_delay_non_los.pdf")
pp.savefig(fig_delay)
pp.close()



# losのpdr
fig_pdr = plt.figure()
ax = fig_pdr.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_pdrs_los[0]) + 1))

df = pd.DataFrame({
    "x": x, cam_nums[0]: all_pdrs_los[0], cam_nums[1]: all_pdrs_los[1], cam_nums[2]: all_pdrs_los[2]
})

ax.plot('x', cam_nums[0], data=df, label='PPS 50', marker='o')
ax.plot('x', cam_nums[1], data=df, label='PPS 100', marker='o')
ax.plot('x', cam_nums[2], data=df, label='PPS 150', marker='o')

ax.legend()
ax.set_xlabel("distance")
ax.set_ylabel("PDR")
ax.set_ylim(-0.1, 1.1)
plt.xticks(np.arange(1,x.size + 1))
plt.title("method: " + method + " line of sight")

pp = PdfPages("summary/" + map_type + "/sim_all/method_" + method + "_pdr_los.pdf")
pp.savefig(fig_pdr)
pp.close()




# losのdelay
fig_delay = plt.figure()
ax = fig_delay.add_subplot(1, 1, 1)

x = np.array(range(1, len(all_delays_los[0]) + 1))

ax.errorbar(x, all_delays_los[0], yerr=all_delay_errors_los[0], marker='o', label='PPS 50', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_los[1], yerr=all_delay_errors_los[1], marker='o', label='PPS 100', capthick=1, capsize=8, lw=1)
ax.errorbar(x, all_delays_los[2], yerr=all_delay_errors_los[2], marker='o', label='PPS 150', capthick=1, capsize=8, lw=1)

ax.legend()
ax.set_xlabel("distance")
ax.set_ylabel("delay")
ax.set_ylim(-150,400)
plt.xticks(np.arange(1,x.size + 1))
plt.title("method: " + method + " line of sight")

pp = PdfPages("summary/" + map_type + "/sim_all/method_" + method + "_delay_los.pdf")
pp.savefig(fig_delay)
pp.close()
