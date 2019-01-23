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
map_type = "grid"
pcam_pos_non_los = [24, 16, 8, 0]
pcam_pos_los = [24, 23, 22, 21]



simTotalInterval = 15

analysis_root_path = "analysis/" + map_type + "/"

print("this is summary of all\n")

# ここにはnum_*のnon_los,losが入る
all_pdrs_non_los = []
all_delays_non_los = []
# all_delay_errors_non_los = []

all_pdrs_los = []
all_delays_los = []
# all_delay_errors_los = []


for method in methods:
    print("entering method", method)
    print("entering non_los")
    for cam_num in cam_nums:
        print("entering cam_num: ", cam_num)
        pdrs_non_los = []
        delays_non_los = []
        # delay_errors_non_los = []
        for pos in pcam_pos_non_los:
            pdrs = []
            delays = []
            # delay_errors = []
            sim_from = 205
            sim_to = 210
            for sim_num in range(100):
                with open(analysis_root_path + method + "/" + cam_num + "/sim_" + str(sim_num) + "/pdr_" + str(pos) + ".txt") as f:
                    pdrlines = f.readlines()
                for pdrline in pdrlines[1:]:
                    if float(pdrline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(pdrline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                        pdrs.append(float(pdrline.split("\t")[1]))
                with open(analysis_root_path + method + "/" + cam_num + "/sim_" + str(sim_num) + "/delay_" + str(pos) + ".txt") as f:
                    delaylines = f.readlines()
                for delayline in delaylines[1:]:
                    if float(delayline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(delayline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                        if not np.isnan(float(delayline.split("\t")[1])):
                            delays.append(float(delayline.split("\t")[1]))
            pdrs_non_los.append(pdrs)
            delays_non_los.append(delays)
        all_pdrs_non_los.append(pdrs_non_los)
        all_delays_non_los.append(delays_non_los)

    print("entering los")
    for cam_num in cam_nums:
        print("entering cam_num: ", cam_num)
        pdrs_los = []
        delays_los = []
        # delay_errors_los = []
        for pos in pcam_pos_los:
            pdrs = []
            delays = []
            # delay_errors = []
            sim_from = 205
            sim_to = 210
            for sim_num in range(100):
                with open(analysis_root_path + method + "/" + cam_num + "/sim_" + str(sim_num) + "/pdr_" + str(pos) + ".txt") as f:
                    pdrlines = f.readlines()
                for pdrline in pdrlines[1:]:
                    if float(pdrline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(pdrline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                        pdrs.append(float(pdrline.split("\t")[1]))
                with open(analysis_root_path + method + "/" + cam_num + "/sim_" + str(sim_num) + "/delay_" + str(pos) + ".txt") as f:
                    delaylines = f.readlines()
                for delayline in delaylines[1:]:
                    if float(delayline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(delayline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                        if not np.isnan(float(delayline.split("\t")[1])):
                            delays.append(float(delayline.split("\t")[1]))
            pdrs_los.append(pdrs)
            delays_los.append(delays)
        all_pdrs_los.append(pdrs_los)
        all_delays_los.append(delays_los)

# non_losのpdr
fig_pdr = plt.figure(figsize=(10,5), dpi= 300)
ax = fig_pdr.add_subplot(1, 1, 1)
x = np.array(['0', '141', '283', '424'])
plt.subplots_adjust(right=0.6)

ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[0]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[0]], marker='D', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="indigo")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[1]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[1]], marker='^', label='Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="hotpink")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[2]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[2]], marker='x', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="red")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[3]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[3]], marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="darkorange", linestyle="-.")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[4]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[4]], marker='>', label='Non Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="purple", linestyle="-.")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[5]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[5]], marker='h', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="teal", linestyle="-.")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[6]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[6]], marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="limegreen", linestyle=":")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[7]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[7]], marker='p', label='Distance Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle=":")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[8]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[8]], marker='o', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")

ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=11)
ax.set_xlabel("distance (m)")
ax.set_ylabel("PDR")
ax.set_ylim(-0.1, 1.1)
plt.title("Non line of sight")

pp = PdfPages("summary/" + map_type + "/sim_all/pdr_non_los.pdf")
pp.savefig(fig_pdr)
pp.close()

# non_losのdelay
fig_delay = plt.figure(figsize=(10,5), dpi= 300)
ax = fig_delay.add_subplot(1, 1, 1)
x = np.array(['0', '141', '283', '424'])
plt.subplots_adjust(right=0.6)

ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[0]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[0]], marker='D', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="indigo")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[1]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[1]], marker='^', label='Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="hotpink")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[2]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[2]], marker='x', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="red")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[3]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[3]], marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="darkorange", linestyle="-.")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[4]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[4]], marker='>', label='Non Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="purple", linestyle="-.")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[5]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[5]], marker='h', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="teal", linestyle="-.")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[6]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[6]], marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="limegreen", linestyle=":")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[7]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[7]], marker='p', label='Distance Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle=":")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[8]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[8]], marker='o', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")

ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=11)
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Delay (ms)")
ax.set_ylim(-150,350)
plt.title("Non line of sight")

pp = PdfPages("summary/" + map_type + "/sim_all/delay_non_los.pdf")
pp.savefig(fig_delay)
pp.close()


# losのpdr
fig_pdr = plt.figure(figsize=(10,5), dpi= 300)
ax = fig_pdr.add_subplot(1, 1, 1)
x = np.array(['0', '100', '200', '300'])
plt.subplots_adjust(right=0.6)

ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[0]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[0]], marker='D', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="indigo")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[1]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[1]], marker='^', label='Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="hotpink")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[2]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[2]], marker='x', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="red")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[3]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[3]], marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="darkorange", linestyle="-.")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[4]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[4]], marker='>', label='Non Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="purple", linestyle="-.")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[5]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[5]], marker='h', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="teal", linestyle="-.")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[6]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[6]], marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="limegreen", linestyle=":")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[7]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[7]], marker='p', label='Distance Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle=":")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[8]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[8]], marker='o', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")

ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=11)
ax.set_xlabel("distance (m)")
ax.set_ylabel("PDR")
ax.set_ylim(-0.1, 1.1)
plt.title("Line of sight")

pp = PdfPages("summary/" + map_type + "/sim_all/pdr_los.pdf")
pp.savefig(fig_pdr)
pp.close()


# losのdelay
fig_delay = plt.figure(figsize=(10,5), dpi= 300)
ax = fig_delay.add_subplot(1, 1, 1)
x = np.array(['0', '100', '200', '300'])
plt.subplots_adjust(right=0.6)

ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[0]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[0]], marker='D', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="indigo")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[1]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[1]], marker='^', label='Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="hotpink")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[2]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[2]], marker='x', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="red")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[3]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[3]], marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="darkorange", linestyle="-.")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[4]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[4]], marker='>', label='Non Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="purple", linestyle="-.")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[5]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[5]], marker='h', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="teal", linestyle="-.")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[6]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[6]], marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="limegreen", linestyle=":")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[7]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[7]], marker='p', label='Distance Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle=":")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[8]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[8]], marker='o', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")

ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=11)
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Delay (ms)")
ax.set_ylim(-150,350)
plt.title("Line of sight")

pp = PdfPages("summary/" + map_type + "/sim_all/delay_los.pdf")
pp.savefig(fig_delay)
pp.close()
