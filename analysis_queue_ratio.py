from statistics import mean, median,stdev
from collections import OrderedDict

import sys
args = sys.argv
method = args[1]
cam_num = args[2]
map_type = "grid"
world_name = "GridWorld"
#gridなら24　bunkyoなら0
center_pcam_num = "24"

if not (method == "original_pcam" or method == "naive_grid_pcam" or method == "passive_grid_pcam"):
    print("error unknown method")
    sys.exit()
if not (int(cam_num) == 5 or int(cam_num) == 10 or int(cam_num) == 15):
    print("error unknown pcam pos num")
    sys.exit()

simTotalInterval = 15

for sim_num in range(100):

    simStartTime = 200 + simTotalInterval * sim_num
    timeDiff = 0.5

    results_queue_ratio_path = "output/" + map_type + "/" + method + "/num_" + cam_num + "/sim_" + str(sim_num) + "/output_" + world_name + ".pcam[" + center_pcam_num + "].disseminator.nic.mac1609_4.txt"

    analysis_queue_ratio_path = "analysis/" + map_type + "/" + method + "/num_" + cam_num + "/sim_" + str(sim_num) + "/queue_ratio.txt"

    queue_ratiof = open(analysis_queue_ratio_path, mode="w")


    with open(results_queue_ratio_path) as f:
        queue_ratio_lines = f.readlines()

    # analysis of delay
    queue_ratiof.write("simTime\tratio\n")
    time = simStartTime
    queue_ratios = []
    for line in queue_ratio_lines:
        objs = line.split("\t")
        srcTime = float(objs[0].split(":")[1])
        queue_ratio = float(objs[1].split(":")[1])
        if srcTime < time + timeDiff:
            queue_ratios.append(queue_ratio)
        else:
            if len(queue_ratios) == 0:
                print(str(time),"mean: nan\n")
                queue_ratiof.write(str(time) + "\t" + "nan\n")
            else:
                print(str(time),"mean: " + str(mean(queue_ratios)) + "\n")
                queue_ratiof.write(str(time) + "\t" + str(mean(queue_ratios)) + "\n")
            time += timeDiff
            while srcTime > time + timeDiff:
                print(str(time),"mean: nan\n")
                queue_ratiof.write(str(time) + "\t" + "nan\n")
                time += timeDiff
            queue_ratios = []
        print("srctime:",srcTime)


    if len(queue_ratios) == 0:
        print(str(time),"mean: nan\n")
        queue_ratiof.write(str(time) + "\t" + "nan\n")
    else:
        print(str(time),"mean: " + str(mean(queue_ratios)) + "\n")
        queue_ratiof.write(str(time) + "\t" + str(mean(queue_ratios)) + "\n")

    queue_ratiof.close()
