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
# methods = ["naive_grid_pcam"]
cam_nums = ["num_5", "num_10", "num_15"]
# cam_nums = ["num_5", "num_15"]
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
        x = []
        y = []
        # delay_errors_non_los = []
        for pos in pcam_pos_non_los:
            pdrs = []
            delays = []
            # delay_errors = []
            sim_from = 205
            sim_to = 210
            for sim_num in range(47):
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
                            # delays.append(float(delayline.split("\t")[1]))
                            # print(delayline.split("\t"))
                            if len(delayline.split("\t")) > 3:
                                x.append(float(delayline.split("\t")[3].split("\n")[0]))
                                y.append(float(delayline.split("\t")[1]))
            pdrs_non_los.append(pdrs)
            delays_non_los.append(delays)
        all_pdrs_non_los.append(pdrs_non_los)
        all_delays_non_los.append(delays_non_los)

        # non_losのdelay
        fig_delay = plt.figure(figsize=(10,4), dpi= 300)
        plt.tight_layout()
        plt.suptitle("Non Line of sight " + method + " " + cam_num)
        plt.subplots_adjust(bottom=0.35)
        #xラベル用
        fig_delay.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
        #yラベル用
        fig_delay.text(0.02, 0.5, 'Delay(ms)', ha='center', va='center', rotation='vertical')
        # x = np.array(x)
        # plt.subplots_adjust(right=0.6)

        ax = fig_delay.add_subplot(1, 3, 1)
        ax.scatter(x, y, s=2)
        ax.set_ylim(-150,350)

        pp = PdfPages("summary/" + map_type +"/sim_all/delay_non_los" + method + cam_num + ".pdf")
        pp.savefig(fig_delay)
        pp.close()

    print("entering los")
    for cam_num in cam_nums:
        print("entering cam_num: ", cam_num)
        pdrs_los = []
        delays_los = []
        x2 = []
        y2 = []
        # delay_errors_los = []
        for pos in pcam_pos_los:
            pdrs = []
            delays = []
            # delay_errors = []
            sim_from = 205
            sim_to = 210
            for sim_num in range(47):
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
                        if len(delayline.split("\t")) > 3:
                            x2.append(float(delayline.split("\t")[3].split("\n")[0]))
                            y2.append(float(delayline.split("\t")[1]))
            pdrs_los.append(pdrs)
            delays_los.append(delays)
            # non_losのdelay
            fig_delay = plt.figure(figsize=(10,4), dpi= 300)
            plt.tight_layout()
            plt.suptitle("Line of sight " + method + " " + cam_num)
            plt.subplots_adjust(bottom=0.35)
            #xラベル用
            fig_delay.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
            #yラベル用
            fig_delay.text(0.02, 0.5, 'Delay(ms)', ha='center', va='center', rotation='vertical')
            x = np.array(x2)
            y = np.array(y2)
            # plt.subplots_adjust(right=0.6)

            ax = fig_delay.add_subplot(1, 3, 1)
            ax.scatter(x, y, s=2)
            ax.set_ylim(-150,350)

            pp = PdfPages("summary/" + map_type +"/sim_all/delay_los" + method + cam_num + ".pdf")
            pp.savefig(fig_delay)
            pp.close()
        all_pdrs_los.append(pdrs_los)
        all_delays_los.append(delays_los)


# x = []
# y = []
# method = "passive_grid_pcam"
# cam_num = "num_15"
# pos = 8
# sim_num = 0
# for pos in range(18):
#     with open(analysis_root_path + method + "/" + cam_num + "/sim_" + str(sim_num) + "/delay_" + str(pos) + ".txt") as f:
#         delaylines = f.readlines()
#     for delayline in delaylines[1:]:
#         if float(delayline.split("\t")[0]) > sim_from + simTotalInterval * sim_num and float(delayline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
#             if not np.isnan(float(delayline.split("\t")[1])):
#                 x.append(float(delayline.split("\t")[3].split("\n")[0]))
#                 y.append(float(delayline.split("\t")[1]))

# non_losのdelay
fig_delay = plt.figure(figsize=(10,4), dpi= 300)
plt.tight_layout()
plt.suptitle("Non Line of sight")
plt.subplots_adjust(bottom=0.35)
#xラベル用
fig_delay.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
#yラベル用
fig_delay.text(0.02, 0.5, 'Delay(ms)', ha='center', va='center', rotation='vertical')
x = np.array(x)
# plt.subplots_adjust(right=0.6)

ax = fig_delay.add_subplot(1, 3, 1)
ax.scatter(x, y, s=2)
ax.set_ylim(-150,350)
fig_delay.show()

pp = PdfPages("summary/" + map_type + "/sim_all/delay_los.pdf")
pp.savefig(fig_delay)
pp.close()
# exit()


# non_losのpdr
fig_pdr = plt.figure(figsize=(12,4), dpi= 300) #ここを小さくすると文字が大きくなる dpiをあげる？
plt.tight_layout()
plt.suptitle("Non Line of sight", fontsize=20)
plt.subplots_adjust(bottom=0.35)
#xラベル用
fig_pdr.text(0.5, 0.03, 'Distance(m)', ha='center', va='center', fontsize=20)
#yラベル用
fig_pdr.text(0.06, 0.5, 'PDR', ha='center', va='center', rotation='vertical', fontsize=20)
x = np.array(['0', '141', '283', '424'])

ax = fig_pdr.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[0]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[0]], markersize= 3, marker='o', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2)
ax.set_ylim(-0.1, 1.1)
ax = fig_pdr.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[1]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[1]], markersize= 3, marker='o', label='Proxy CAM', capthick=1, capsize=8, lw=2)
ax.set_ylim(-0.1, 1.1)
ax = fig_pdr.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[2]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[2]], markersize= 3, marker='o', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2)
ax.set_ylim(-0.1, 1.1)

ax = fig_pdr.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[3]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[3]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-0.1, 1.1)
ax = fig_pdr.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[4]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[4]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-0.1, 1.1)
ax = fig_pdr.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[5]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[5]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-0.1, 1.1)
ax = fig_pdr.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[6]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[6]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-0.1, 1.1)
ax.set_xlabel("25vel/km", fontsize=14)
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

ax = fig_pdr.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[7]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[7]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-0.1, 1.1)
ax.set_xlabel("50vel/km", fontsize=14)
ax.legend(bbox_to_anchor=(0.5, -0.4), loc = "center", borderaxespad=0, fontsize=14, ncol=3)

ax = fig_pdr.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[8]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_non_los[8]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-0.1, 1.1)
ax.set_xlabel("75vel/km", fontsize=14)
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

pp = PdfPages("summary/" + map_type + "/sim_all/pdr_non_los.pdf")
pp.savefig(fig_pdr)
pp.close()

# non_losのdelay
fig_delay = plt.figure(figsize=(10,4), dpi= 300)
plt.tight_layout()
plt.suptitle("Non Line of sight")
plt.subplots_adjust(bottom=0.35)
#xラベル用
fig_delay.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
#yラベル用
fig_delay.text(0.02, 0.5, 'Delay(ms)', ha='center', va='center', rotation='vertical')
x = np.array(['0', '141', '283', '424'])
# plt.subplots_adjust(right=0.6)

ax = fig_delay.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[0]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[0]], markersize= 3, marker='o', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2)
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[1]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[1]], markersize= 3, marker='o', label='Proxy CAM', capthick=1, capsize=8, lw=2)
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[2]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[2]], markersize= 3, marker='o', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2)
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[3]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[3]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[4]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[4]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[5]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[5]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[6]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[6]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-150,350)
ax.set_xlabel("25vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

ax = fig_delay.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[7]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[7]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-150,350)
ax.set_xlabel("50vel/km")
ax.legend(bbox_to_anchor=(0.5, -0.35), loc = "center", borderaxespad=0, fontsize=8)

ax = fig_delay.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_non_los[8]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_non_los[8]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-150,350)
ax.set_xlabel("75vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

pp = PdfPages("summary/" + map_type + "/sim_all/delay_non_los.pdf")
pp.savefig(fig_delay)
pp.close()


# losのpdr
fig_pdr = plt.figure(figsize=(10,4), dpi= 300)
plt.tight_layout()
plt.suptitle("Line of sight")
plt.subplots_adjust(bottom=0.35)
#xラベル用
fig_pdr.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
#yラベル用
fig_pdr.text(0.02, 0.5, 'PDR', ha='center', va='center', rotation='vertical')
x = np.array(['0', '100', '200', '300'])

ax = fig_pdr.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[0]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[0]], markersize= 3, marker='o', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2)
ax.set_ylim(-0.1, 1.1)
ax = fig_pdr.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[1]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[1]], markersize= 3, marker='o', label='Proxy CAM', capthick=1, capsize=8, lw=2)
ax.set_ylim(-0.1, 1.1)
ax = fig_pdr.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[2]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[2]], markersize= 3, marker='o', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2)
ax.set_ylim(-0.1, 1.1)
ax = fig_pdr.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[3]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[3]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-0.1, 1.1)
ax = fig_pdr.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[4]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[4]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-0.1, 1.1)
ax = fig_pdr.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[5]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[5]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-0.1, 1.1)
ax = fig_pdr.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[6]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[6]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-0.1, 1.1)
ax.set_xlabel("25vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

ax = fig_pdr.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[7]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[7]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-0.1, 1.1)
ax.set_xlabel("50vel/km")
ax.legend(bbox_to_anchor=(0.5, -0.35), loc = "center", borderaxespad=0, fontsize=8)

ax = fig_pdr.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[8]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs_los[8]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-0.1, 1.1)
ax.set_xlabel("75vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

pp = PdfPages("summary/" + map_type + "/sim_all/pdr_los.pdf")
pp.savefig(fig_pdr)
pp.close()


# losのdelay
fig_delay = plt.figure(figsize=(10,4), dpi= 300)
plt.tight_layout()
plt.suptitle("Line of sight")
plt.subplots_adjust(bottom=0.35)
#xラベル用
fig_delay.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
#yラベル用
fig_delay.text(0.02, 0.5, 'Delay(ms)', ha='center', va='center', rotation='vertical')
x = np.array(['0', '100', '200', '300'])
# plt.subplots_adjust(right=0.6)

ax = fig_delay.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[0]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[0]], markersize= 3, marker='o', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2)
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[1]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[1]], markersize= 3, marker='o', label='Proxy CAM', capthick=1, capsize=8, lw=2)
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[2]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[2]], markersize= 3, marker='o', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2)
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[3]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[3]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[4]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[4]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[5]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[5]], markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, linestyle="-.")
ax.set_ylim(-150,350)
ax = fig_delay.add_subplot(1, 3, 1)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[6]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[6]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-150,350)
ax.set_xlabel("25vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

ax = fig_delay.add_subplot(1, 3, 2)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[7]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[7]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-150,350)
ax.set_xlabel("50vel/km")
ax.legend(bbox_to_anchor=(0.5, -0.35), loc = "center", borderaxespad=0, fontsize=8)

ax = fig_delay.add_subplot(1, 3, 3)
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays_los[8]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays_los[8]], markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, linestyle=":")
ax.set_ylim(-150,350)
ax.set_xlabel("75vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

pp = PdfPages("summary/" + map_type + "/sim_all/delay_los.pdf")
pp.savefig(fig_delay)
pp.close()
