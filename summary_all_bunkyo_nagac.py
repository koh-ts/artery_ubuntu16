
# coding: utf-8

# In[1]:


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
# cam_nums = ["num_5", "num_15"]
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
                    if float(pdrline.split("\t")[0]) >= sim_from + simTotalInterval * sim_num and float(pdrline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                        pdrs.append(float(pdrline.split("\t")[1]))
                with open(analysis_root_path + method + "/" + cam_num + "/sim_" + str(sim_num) + "/delay_" + str(num) + ".txt") as f:
                    delaylines = f.readlines()
                for delayline in delaylines[1:]:
                    if float(delayline.split("\t")[0]) >= sim_from + simTotalInterval * sim_num and float(delayline.split("\t")[0]) < sim_to + simTotalInterval * sim_num:
                        if not np.isnan(float(delayline.split("\t")[1])):
                            delays.append(float(delayline.split("\t")[1]))
            pdrs_all_num.append(pdrs)
            delays_all_num.append(delays)
        all_pdrs.append(pdrs_all_num)
        all_delays.append(delays_all_num)


# In[48]:


# original_pcam (pastaさんの手法)
# naive_grid_pcam -> non priority (比較用の手法)
# passive_grid_pcam -> distance priority (提案手法)
# pcam_num = 5 or 10 or 15

# all_pdrs,all_delaysは順に
# [0] : original_pcam pcam_num = 5
# [1] : original_pcam pcam_num = 10
# [2] : original_pcam pcam_num = 15
# [3] : naive_grid_pcam pcam_num = 5
# [4] : naive_grid_pcam pcam_num = 10
# [5] : naive_grid_pcam pcam_num = 15
# [6] : passive_grid_pcam pcam_num = 5
# [7] : passive_grid_pcam pcam_num = 10
# [8] : passive_grid_pcam pcam_num = 15

# さらに各要素は配列となっており、
# pcam_numsで指定したpcam_numのrsuに近い順に並べ替えた順に
# all_pdrsの場合はPDR、all_delaysの場合はdelayが入っている

# 各PDRとdelayについて
# シミュレーションを100回行なっている
# 各シミュレーションでは0.5秒間隔で5秒間分、PDRと平均のdelayが記録されている
# all_pdrs,all_deleysにはその100回分のPDRとdelayが格納されている

# shape:
# all_pdrs, all_deleys: (9, len(pcam_nums), 5/0.5 * 100 = 1000(maxの値))

# pdr
x = []
for i in range(len(pcam_poss)):
    x.append(np.linalg.norm(rsu_pos - pcam_poss[i]))


fig_pdr = plt.figure(figsize=(10,5), dpi= 300)
ax = fig_pdr.add_subplot(1, 1, 1)
plt.subplots_adjust(right=0.6)
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]],markersize= 3, marker='D', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=1, color="indigo")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]],markersize= 3, marker='^', label='Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=1, color="hotpink")
ax.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]],markersize= 3, marker='x', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=1, color="red")
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=11)
ax.set_xlabel("distance (m)")
ax.set_ylabel("PDR")
ax.set_ylim(-0.1, 1.1)

fig_pdr1 = plt.figure(figsize=(10,5), dpi= 300)
ax1 = fig_pdr1.add_subplot(1, 1, 1)
plt.subplots_adjust(right=0.6)
ax1.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=1, color="darkorange", linestyle="-.")
ax1.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]],markersize= 3, marker='>', label='Non Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=1, color="purple", linestyle="-.")
ax1.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]],markersize= 3, marker='h', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=1, color="teal", linestyle="-.")
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=11)
ax1.set_xlabel("distance (m)")
ax1.set_ylabel("PDR")
ax1.set_ylim(-0.1, 1.1)

fig_pdr2 = plt.figure(figsize=(10,5), dpi= 300)
ax2 = fig_pdr2.add_subplot(1, 1, 1)
plt.subplots_adjust(right=0.6)
ax2.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=1, color="limegreen", linestyle=":")
ax2.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]],markersize= 3, marker='p', label='Distance Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=1, color="darkgreen", linestyle=":")
ax2.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]],markersize= 3, marker='o', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=1, color="navy", linestyle=":")
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=11)
ax2.set_xlabel("distance (m)")
ax2.set_ylabel("PDR")
ax2.set_ylim(-0.1, 1.1)

fig_pdr3 = plt.figure(figsize=(10,4), dpi= 300)
plt.tight_layout()
plt.subplots_adjust(bottom=0.35)
#xラベル用
fig_pdr3.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
#yラベル用
fig_pdr3.text(0.02, 0.5, 'PDR', ha='center', va='center', rotation='vertical')
# plt.subplots_adjust(right=0.6)

ax3 = fig_pdr3.add_subplot(1, 3, 1)
ax3.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]],markersize= 3, marker='o')
ax3.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]), alpha=0.5)
# ax3.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]],markersize= 3, marker='o', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="red")
ax3.set_ylim(-0.1, 1.1)
ax3 = fig_pdr3.add_subplot(1, 3, 2)
ax3.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]],markersize= 3, marker='o', label='Proxy CAM')
ax3.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]), alpha=0.5)
# ax3.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]],markersize= 3, marker='o', label='Proxy CAM', capthick=1, capsize=8, lw=2, color="red")
ax3.set_ylim(-0.1, 1.1)
ax3 = fig_pdr3.add_subplot(1, 3, 3)
ax3.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]],markersize= 3, marker='o')
ax3.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]), alpha=0.5)
# ax3.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]],markersize= 3, marker='o', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="red")
ax3.set_ylim(-0.1, 1.1)
ax3 = fig_pdr3.add_subplot(1, 3, 1)
ax3.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]],markersize= 3, marker='s')
ax3.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]), alpha=0.5)
# ax3.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax3.set_ylim(-0.1, 1.1)
ax3 = fig_pdr3.add_subplot(1, 3, 2)
ax3.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM')
ax3.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]), alpha=0.5)
# ax3.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax3.set_ylim(-0.1, 1.1)
ax3 = fig_pdr3.add_subplot(1, 3, 3)
ax3.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]],markersize= 3, marker='s')
ax3.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]), alpha=0.5)
# ax3.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax3.set_ylim(-0.1, 1.1)
ax3 = fig_pdr3.add_subplot(1, 3, 1)
ax3.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]],markersize= 3, marker='d')
ax3.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]), alpha=0.5)
# ax3.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax3.set_ylim(-0.1, 1.1)
ax3.set_xlabel("25vel/km")
# ax3.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

ax3 = fig_pdr3.add_subplot(1, 3, 2)
ax3.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM')
ax3.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]), alpha=0.5)
# ax3.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax3.set_ylim(-0.1, 1.1)
ax3.set_xlabel("50vel/km")
ax3.legend(bbox_to_anchor=(0.5, -0.35), loc = "center", borderaxespad=0, fontsize=8)

ax3 = fig_pdr3.add_subplot(1, 3, 3)
ax3.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]],markersize= 3, marker='d')
ax3.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]), alpha=0.5)
# ax3.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax3.set_ylim(-0.1, 1.1)
ax3.set_xlabel("75vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

fig_pdr4 = plt.figure(figsize=(10,4), dpi= 300)
plt.tight_layout()
plt.subplots_adjust(bottom=0.35)
#xラベル用
fig_pdr4.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
#yラベル用
fig_pdr4.text(0.02, 0.5, 'PDR', ha='center', va='center', rotation='vertical')
# plt.subplots_adjust(right=0.6)

ax4 = fig_pdr4.add_subplot(1, 3, 1)
ax4.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]],markersize= 3, marker='o')
ax4.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]), alpha=0.5)
# ax4.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]],markersize= 3, marker='o', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="red")
ax4.set_ylim(-0.1, 1.1)
ax4 = fig_pdr4.add_subplot(1, 3, 2)
ax4.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]],markersize= 3, marker='o', label='Proxy CAM')
ax4.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]), alpha=0.5)
# ax4.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]],markersize= 3, marker='o', label='Proxy CAM', capthick=1, capsize=8, lw=2, color="red")
ax4.set_ylim(-0.1, 1.1)
ax4 = fig_pdr4.add_subplot(1, 3, 3)
ax4.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]],markersize= 3, marker='o')
ax4.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]), alpha=0.5)
# ax4.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]],markersize= 3, marker='o', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="red")
ax4.set_ylim(-0.1, 1.1)
ax4 = fig_pdr4.add_subplot(1, 3, 1)
ax4.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]],markersize= 3, marker='s')
ax4.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]), alpha=0.5)
# ax4.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax4.set_ylim(-0.1, 1.1)
ax4 = fig_pdr4.add_subplot(1, 3, 2)
ax4.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM')
ax4.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]), alpha=0.5)
# ax4.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax4.set_ylim(-0.1, 1.1)
ax4 = fig_pdr4.add_subplot(1, 3, 3)
ax4.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]],markersize= 3, marker='s')
ax4.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]), alpha=0.5)
# ax4.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax4.set_ylim(-0.1, 1.1)
ax4 = fig_pdr4.add_subplot(1, 3, 1)
ax4.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]],markersize= 3, marker='d')
ax4.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]), alpha=0.5)
# ax4.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax4.set_ylim(-0.1, 1.1)
ax4.set_xlabel("25vel/km")
# ax4.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

ax4 = fig_pdr4.add_subplot(1, 3, 2)
ax4.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM')
ax4.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]), alpha=0.5)
# ax4.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax4.set_ylim(-0.1, 1.1)
ax4.set_xlabel("50vel/km")
ax4.legend(bbox_to_anchor=(0.5, -0.35), loc = "center", borderaxespad=0, fontsize=8)

ax4 = fig_pdr4.add_subplot(1, 3, 3)
ax4.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]],markersize= 3, marker='d')
ax4.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]), alpha=0.5)
# ax4.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax4.set_ylim(-0.1, 1.1)
ax4.set_xlabel("75vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

fig_pdr5 = plt.figure(figsize=(10,4), dpi= 300)
plt.tight_layout()
plt.subplots_adjust(bottom=0.35)
#xラベル用
fig_pdr5.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
#yラベル用
fig_pdr5.text(0.02, 0.5, 'PDR', ha='center', va='center', rotation='vertical')
# plt.subplots_adjust(right=0.6)

ax5 = fig_pdr5.add_subplot(1, 3, 1)
ax5.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]],markersize= 3, marker='o', lw=2)
ax5.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]]), alpha=0.5)
# ax5.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[0]],markersize= 3, marker='o', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="red")
ax5.set_ylim(-0.1, 1.1)
ax5 = fig_pdr5.add_subplot(1, 3, 2)
ax5.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]],markersize= 3, marker='o', label='Proxy CAM', lw=2)
ax5.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]]), alpha=0.5)
# ax5.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[1]],markersize= 3, marker='o', label='Proxy CAM', capthick=1, capsize=8, lw=2, color="red")
ax5.set_ylim(-0.1, 1.1)
ax5 = fig_pdr5.add_subplot(1, 3, 3)
ax5.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]],markersize= 3, marker='o', lw=2)
ax5.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]]), alpha=0.5)
# ax5.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[2]],markersize= 3, marker='o', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="red")
ax5.set_ylim(-0.1, 1.1)
ax5 = fig_pdr5.add_subplot(1, 3, 1)
ax5.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]],markersize= 3, marker='s', lw=2, linestyle="-.")
ax5.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]]), alpha=0.5)
# ax5.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[3]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax5.set_ylim(-0.1, 1.1)
ax5 = fig_pdr5.add_subplot(1, 3, 2)
ax5.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', lw=2, linestyle="-.")
ax5.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]]), alpha=0.5)
# ax5.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax5.set_ylim(-0.1, 1.1)
ax5 = fig_pdr5.add_subplot(1, 3, 3)
ax5.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]],markersize= 3, marker='s', lw=2, linestyle="-.")
ax5.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]]), alpha=0.5)
# ax5.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[5]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax5.set_ylim(-0.1, 1.1)
ax5 = fig_pdr5.add_subplot(1, 3, 1)
ax5.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]],markersize= 3, marker='d', lw=2, linestyle=":")
ax5.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]]), alpha=0.5)
# ax5.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[6]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax5.set_ylim(-0.1, 1.1)
ax5.set_xlabel("25vel/km")
# ax5.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

ax5 = fig_pdr5.add_subplot(1, 3, 2)
ax5.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', lw=2, linestyle=":")
ax5.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]]), alpha=0.5)
# ax5.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax5.set_ylim(-0.1, 1.1)
ax5.set_xlabel("50vel/km")
ax5.legend(bbox_to_anchor=(0.5, -0.35), loc = "center", borderaxespad=0, fontsize=8)

ax5 = fig_pdr5.add_subplot(1, 3, 3)
ax5.plot(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]],markersize= 3, marker='d', lw=2, linestyle=":")
ax5.fill_between(x,np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]) - np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]), np.array([mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]) + np.array([stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]]), alpha=0.5)
# ax5.errorbar(x, [mean(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]] , yerr= [stdev(pdrs) if len(pdrs) >= 2 else 0 for pdrs in all_pdrs[8]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax5.set_ylim(-0.1, 1.1)
ax5.set_xlabel("75vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)


# delay
fig_delay = plt.figure(figsize=(10,5), dpi= 300)
ax = fig_delay.add_subplot(1, 1, 1)
plt.subplots_adjust(right=0.6)

ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[0]],markersize= 3, marker='D', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=1, color="indigo")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[1]],markersize= 3, marker='^', label='Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=1, color="hotpink")
ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[2]],markersize= 3, marker='x', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=1, color="red")
# ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=1, color="darkorange", linestyle="-.")
# ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]],markersize= 3, marker='>', label='Non Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=1, color="purple", linestyle="-.")
# ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]],markersize= 3, marker='h', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=1, color="teal", linestyle="-.")
# ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=1, color="limegreen", linestyle=":")
# ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]],markersize= 3, marker='p', label='Distance Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=1, color="darkgreen", linestyle=":")
# ax.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]],markersize= 3, marker='o', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=1, color="navy", linestyle=":")

ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=11)
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Delay (ms)")
ax.set_ylim(-150,500)

fig_delay1 = plt.figure(figsize=(10,5), dpi= 300)
ax1 = fig_delay1.add_subplot(1, 1, 1)
plt.subplots_adjust(right=0.6)
ax1.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=1, color="darkorange", linestyle="-.")
ax1.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]],markersize= 3, marker='>', label='Non Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=1, color="purple", linestyle="-.")
ax1.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]],markersize= 3, marker='h', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=1, color="teal", linestyle="-.")
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=11)
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=11)
ax1.set_xlabel("Distance (m)")
ax1.set_ylabel("Delay (ms)")
ax1.set_ylim(-150,500)

fig_delay2 = plt.figure(figsize=(10,5), dpi= 300)
ax2 = fig_delay2.add_subplot(1, 1, 1)
plt.subplots_adjust(right=0.6)
ax2.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=1, color="limegreen", linestyle=":")
ax2.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]],markersize= 3, marker='p', label='Distance Priority Grid Proxy CAM, 50vel/km', capthick=1, capsize=8, lw=1, color="darkgreen", linestyle=":")
ax2.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]],markersize= 3, marker='o', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=1, color="navy", linestyle=":")
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=11)
ax2.set_xlabel("Distance (m)")
ax2.set_ylabel("Delay (ms)")
ax2.set_ylim(-150,500)

fig_delay3 = plt.figure(figsize=(10,4), dpi= 300)
plt.tight_layout()
plt.subplots_adjust(bottom=0.35)
#xラベル用
fig_delay3.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
#yラベル用
fig_delay3.text(0.02, 0.5, 'Delay(ms)', ha='center', va='center', rotation='vertical')
# plt.subplots_adjust(right=0.6)

ax3 = fig_delay3.add_subplot(1, 3, 1)
ax3.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]],markersize= 3, marker='o')
ax3.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[0]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[0]]), alpha=0.5)
# ax3.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[0]],markersize= 3, marker='o', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="red")
ax3.set_ylim(-150,350)
ax3 = fig_delay3.add_subplot(1, 3, 2)
ax3.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]],markersize= 3, marker='o', label='Proxy CAM')
ax3.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[1]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[1]]), alpha=0.5)
# ax3.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[1]],markersize= 3, marker='o', label='Proxy CAM', capthick=1, capsize=8, lw=2, color="red")
ax3.set_ylim(-150,350)
ax3 = fig_delay3.add_subplot(1, 3, 3)
ax3.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]],markersize= 3, marker='o')
ax3.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[2]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[2]]), alpha=0.5)
# ax3.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[2]],markersize= 3, marker='o', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="red")
ax3.set_ylim(-150,350)
ax3 = fig_delay3.add_subplot(1, 3, 1)
ax3.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]],markersize= 3, marker='s')
ax3.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]]), alpha=0.5)
# ax3.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax3.set_ylim(-150,350)
ax3 = fig_delay3.add_subplot(1, 3, 2)
ax3.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM')
ax3.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]]), alpha=0.5)
# ax3.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax3.set_ylim(-150,350)
ax3 = fig_delay3.add_subplot(1, 3, 3)
ax3.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]],markersize= 3, marker='s')
ax3.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]]), alpha=0.5)
# ax3.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax3.set_ylim(-150,350)
ax3 = fig_delay3.add_subplot(1, 3, 1)
ax3.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]],markersize= 3, marker='d')
ax3.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]]), alpha=0.5)
# ax3.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax3.set_ylim(-150,350)
ax3.set_xlabel("25vel/km")
# ax3.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

ax3 = fig_delay3.add_subplot(1, 3, 2)
ax3.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM')
ax3.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]]), alpha=0.5)
# ax3.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax3.set_ylim(-150,350)
ax3.set_xlabel("50vel/km")
ax3.legend(bbox_to_anchor=(0.5, -0.35), loc = "center", borderaxespad=0, fontsize=8)

ax3 = fig_delay3.add_subplot(1, 3, 3)
ax3.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]],markersize= 3, marker='d')
ax3.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]]), alpha=0.5)
# ax3.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax3.set_ylim(-150,350)
ax3.set_xlabel("75vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)


fig_delay4 = plt.figure(figsize=(10,4), dpi= 300)
plt.tight_layout()
plt.subplots_adjust(bottom=0.35)
#xラベル用
fig_delay4.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
#yラベル用
fig_delay4.text(0.02, 0.5, 'Delay(ms)', ha='center', va='center', rotation='vertical')
# plt.subplots_adjust(right=0.6)

ax4 = fig_delay4.add_subplot(1, 3, 1)
ax4.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]],markersize= 3, marker='o')
ax4.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[0]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[0]]), alpha=0.5)
# ax4.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[0]],markersize= 3, marker='o', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="red")
ax4.set_ylim(-150,350)
ax4 = fig_delay4.add_subplot(1, 3, 2)
ax4.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]],markersize= 3, marker='o', label='Proxy CAM')
ax4.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[1]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[1]]), alpha=0.5)
# ax4.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[1]],markersize= 3, marker='o', label='Proxy CAM', capthick=1, capsize=8, lw=2, color="red")
ax4.set_ylim(-150,350)
ax4 = fig_delay4.add_subplot(1, 3, 3)
ax4.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]],markersize= 3, marker='o')
ax4.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[2]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[2]]), alpha=0.5)
# ax4.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[2]],markersize= 3, marker='o', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="red")
ax4.set_ylim(-150,350)
ax4 = fig_delay4.add_subplot(1, 3, 1)
ax4.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]],markersize= 3, marker='s')
ax4.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]]), alpha=0.5)
# ax4.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax4.set_ylim(-150,350)
ax4 = fig_delay4.add_subplot(1, 3, 2)
ax4.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM')
ax4.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]]), alpha=0.5)
# ax4.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax4.set_ylim(-150,350)
ax4 = fig_delay4.add_subplot(1, 3, 3)
ax4.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]],markersize= 3, marker='s')
ax4.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]]), alpha=0.5)
# ax4.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax4.set_ylim(-150,350)
ax4 = fig_delay4.add_subplot(1, 3, 1)
ax4.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]],markersize= 3, marker='d')
ax4.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]]), alpha=0.5)
# ax4.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax4.set_ylim(-150,350)
ax4.set_xlabel("25vel/km")
# ax4.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

ax4 = fig_delay4.add_subplot(1, 3, 2)
ax4.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM')
ax4.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]]), alpha=0.5)
# ax4.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax4.set_ylim(-150,350)
ax4.set_xlabel("50vel/km")
ax4.legend(bbox_to_anchor=(0.5, -0.35), loc = "center", borderaxespad=0, fontsize=8)

ax4 = fig_delay4.add_subplot(1, 3, 3)
ax4.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]],markersize= 3, marker='d')
ax4.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]]), alpha=0.5)
# ax4.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax4.set_ylim(-150,350)
ax4.set_xlabel("75vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)


fig_delay5 = plt.figure(figsize=(10,4), dpi= 300)
plt.tight_layout()
plt.subplots_adjust(bottom=0.35)
#xラベル用
fig_delay5.text(0.5, 0.02, 'Distance(m)', ha='center', va='center')
#yラベル用
fig_delay5.text(0.02, 0.5, 'Delay(ms)', ha='center', va='center', rotation='vertical')
# plt.subplots_adjust(right=0.6)

ax5 = fig_delay5.add_subplot(1, 3, 1)
ax5.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]],markersize= 3, marker='o', lw=2)
ax5.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[0]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[0]]), alpha=0.5)
# ax5.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[0]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[0]],markersize= 3, marker='o', label='Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="red")
ax5.set_ylim(-150,350)
ax5 = fig_delay5.add_subplot(1, 3, 2)
ax5.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]],markersize= 3, marker='o', label='Proxy CAM', lw=2)
ax5.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[1]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[1]]), alpha=0.5)
# ax5.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[1]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[1]],markersize= 3, marker='o', label='Proxy CAM', capthick=1, capsize=8, lw=2, color="red")
ax5.set_ylim(-150,350)
ax5 = fig_delay5.add_subplot(1, 3, 3)
ax5.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]],markersize= 3, marker='o', lw=2)
ax5.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[2]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[2]]), alpha=0.5)
# ax5.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[2]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[2]],markersize= 3, marker='o', label='Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="red")
ax5.set_ylim(-150,350)
ax5 = fig_delay5.add_subplot(1, 3, 1)
ax5.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]],markersize= 3, marker='s', lw=2, linestyle="-.")
ax5.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]]), alpha=0.5)
# ax5.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[3]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[3]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax5.set_ylim(-150,350)
ax5 = fig_delay5.add_subplot(1, 3, 2)
ax5.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', lw=2, linestyle="-.")
ax5.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]]), alpha=0.5)
# ax5.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[4]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[4]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax5.set_ylim(-150,350)
ax5 = fig_delay5.add_subplot(1, 3, 3)
ax5.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]],markersize= 3, marker='s', lw=2, linestyle="-.")
ax5.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]]), alpha=0.5)
# ax5.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[5]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[5]],markersize= 3, marker='s', label='Non Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="darkgreen", linestyle="-.")
ax5.set_ylim(-150,350)
ax5 = fig_delay5.add_subplot(1, 3, 1)
ax5.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]],markersize= 3, marker='d', lw=2, linestyle=":")
ax5.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]]), alpha=0.5)
# ax5.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[6]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[6]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 25vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax5.set_ylim(-150,350)
ax5.set_xlabel("25vel/km")
# ax5.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)

ax5 = fig_delay5.add_subplot(1, 3, 2)
ax5.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', lw=2, linestyle=":")
ax5.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]]), alpha=0.5)
# ax5.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[7]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[7]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax5.set_ylim(-150,350)
ax5.set_xlabel("50vel/km")
ax5.legend(bbox_to_anchor=(0.5, -0.35), loc = "center", borderaxespad=0, fontsize=8)

ax5 = fig_delay5.add_subplot(1, 3, 3)
ax5.plot(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]],markersize= 3, marker='d', lw=2, linestyle=":")
ax5.fill_between(x,np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]]) - np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]]), np.array([mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]]) + np.array([stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]]), alpha=0.5)
# ax5.errorbar(x, [mean(delays) if len(delays) >= 2 else -100 for delays in all_delays[8]] , yerr= [stdev(delays) if len(delays) >= 2 else 0 for delays in all_delays[8]],markersize= 3, marker='d', label='Distance Priority Grid Proxy CAM, 75vel/km', capthick=1, capsize=8, lw=2, color="navy", linestyle=":")
ax5.set_ylim(-150,350)
ax5.set_xlabel("75vel/km")
# ax.legend(bbox_to_anchor=(0.5, -0.3), loc = "center", borderaxespad=0, fontsize=8)



# In[8]:


pp = PdfPages("summary/" + map_type + "/sim_all/pdr_original_pcam.pdf")
pp.savefig(fig_pdr)
pp.close()
pp = PdfPages("summary/" + map_type + "/sim_all/pdr_non_priority_grid_pcam.pdf")
pp.savefig(fig_pdr1)
pp.close()
pp = PdfPages("summary/" + map_type + "/sim_all/pdr_distance_priority_grid_pcam.pdf")
pp.savefig(fig_pdr2)
pp.close()
pp = PdfPages("summary/" + map_type + "/sim_all/pdr_cam_5.pdf")
pp.savefig(fig_pdr3)
pp.close()
pp = PdfPages("summary/" + map_type + "/sim_all/pdr_cam_10.pdf")
pp.savefig(fig_pdr4)
pp.close()
pp = PdfPages("summary/" + map_type + "/sim_all/pdr_cam_15.pdf")
pp.savefig(fig_pdr5)
pp.close()


# In[9]:


pp = PdfPages("summary/" + map_type + "/sim_all/delay_original_pcam.pdf")
pp.savefig(fig_delay)
pp.close()
pp = PdfPages("summary/" + map_type + "/sim_all/delay_non_priority_grid_pcam.pdf")
pp.savefig(fig_delay1)
pp.close()
pp = PdfPages("summary/" + map_type + "/sim_all/delay_distance_priority_grid_pcam.pdf")
pp.savefig(fig_delay2)
pp.close()
pp = PdfPages("summary/" + map_type + "/sim_all/delay_cam_5.pdf")
pp.savefig(fig_delay3)
pp.close()
pp = PdfPages("summary/" + map_type + "/sim_all/delay_cam_10.pdf")
pp.savefig(fig_delay4)
pp.close()
pp = PdfPages("summary/" + map_type + "/sim_all/delay_cam_15.pdf")
pp.savefig(fig_delay5)
pp.close()


# In[39]:
