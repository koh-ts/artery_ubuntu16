from statistics import mean, median,variance,stdev

import sys
args = sys.argv
pcamNo = int(args[1])

simStartTime = 190
timeDiff = 0.05

results_path = "output/output_GridWorld.pcam[" + str(pcamNo) + "].sensor.udpApp[0]_sender.txt"
results_rsu_path = "output/output_GridWorld.rsu[0].appl.middleware.CaService.txt"

analysis_pdr_path = "analysis/pdr_" + str(pcamNo) + ".txt"
analysis_delay_path = "analysis/delay_" + str(pcamNo) + ".txt"

delayf = open(analysis_delay_path, mode="w")
pdrf = open(analysis_pdr_path, mode="w")


delayf.write("simTime\tdelay_avg(ms)\tdelay_variance(ms)\n")
with open(results_rsu_path) as f:
    lines = f.readlines()

time = simStartTime
delays = []
for line in lines:
    objs = line.split("\t")
    if int(objs[1].split(":")[1]) != pcamNo:
        continue
    srcTime = float(objs[2].split(":")[1]) / pow(10,6)
    dstTime = float(objs[0].split(":")[1])
    if srcTime < time + timeDiff:
        delays.append(dstTime - srcTime)
    else:
        if len(delays) == 0:
            print(str(time),"mean","nan","variance","nan", "\n")
            delayf.write(str(time) + "\t" + "nan" + "\t" + "nan" + "\n")
        elif len(delays) == 1:
            print(str(time),"mean",str(mean(delays) * 1000),"variance","nan","\n")
            delayf.write(str(time) + "\t" + str(mean(delays)* 1000) + "\t" + "nan" + "\n")
        else:
            print(str(time),"mean",str(mean(delays) * 1000),"variance",str(variance(delays) * 1000), "\n")
            delayf.write(str(time) + "\t" + str(mean(delays)* 1000) + "\t" + str(variance(delays)* 1000) + "\n")

        time += timeDiff
        while srcTime > time + timeDiff:
            print(str(time),"mean","nan","variance","nan", "\n")
            delayf.write(str(time) + "\t" + "nan" + "\t" + "nan" + "\n")
            time += timeDiff
        delays = []
        delays.append(dstTime - srcTime)
    print("srctime:",srcTime,"dsttime:",dstTime)


if len(delays) == 0:
    print(str(time),"mean","nan","variance","nan", "\n")
    delayf.write(str(time) + "\t" + "nan" + "\t" + "nan" + "\n")
elif len(delays) == 1:
    print(str(time),"mean",str(mean(delays) * 1000),"variance","nan", "\n")
    delayf.write(str(time) + "\t" + str(mean(delays)* 1000) + "\t" + "nan" + "\n")
else:
    print(str(time),"mean",str(mean(delays) * 1000),"variance",str(variance(delays) * 1000), "\n")
    delayf.write(str(time) + "\t" + str(mean(delays)* 1000) + "\t" + str(variance(delays)* 1000) + "\n")


delayf.close()
