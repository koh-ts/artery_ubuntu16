from statistics import mean, median,variance,stdev
from collections import OrderedDict

import sys
args = sys.argv
pcamNo = int(args[1])

simStartTime = 200
timeDiff = 0.5

results_sensor_path = "output/output_GridWorld.pcam[" + str(pcamNo) + "].sensor.udpApp[0]_sender.txt"
results_rsu_path = "output/output_GridWorld.rsu[0].appl.middleware.CaService.txt"

analysis_pdr_path = "analysis/pdr_" + str(pcamNo) + ".txt"
analysis_delay_path = "analysis/delay_" + str(pcamNo) + ".txt"

delayf = open(analysis_delay_path, mode="w")
pdrf = open(analysis_pdr_path, mode="w")


with open(results_rsu_path) as f:
    rsu_lines = f.readlines()
with open(results_sensor_path) as f:
    sensor_lines = f.readlines()


# rsu の rsu_linesをpdrで再利用するのでrsu_linesに変更は加えてはいけない

# analysis of delay
delayf.write("simTime\tdelay_avg(ms)\tdelay_variance(ms)\n")
time = simStartTime
delays = []
for line in rsu_lines:
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


# analysis of pdr
rcvd_counts = OrderedDict()

# pcamのtransmissionの範囲を100m以上にした時は考慮していないので注意
# rsuの受信したパケットのsnの順序が正しくない可能性、同じsnを持つパケットの可能性を考慮する必要がある

time = simStartTime
send_counts = OrderedDict()
lastSn = -1
start_pos = 0

for s_line in sensor_lines:
    objs = s_line.split("\t")
    if int(objs[1].split(":")[1]) == lastSn:
        continue
    srcTime = float(objs[0].split(":")[1])
    targetTime = simStartTime + int((srcTime - simStartTime) / timeDiff) * timeDiff
    if str(targetTime) in send_counts:
        send_counts[str(targetTime)] += 1
    else:
        send_counts[str(targetTime)] = 1

    sn = int(objs[1].split(":")[1])
    for r_line in rsu_lines[start_pos:]:
        objs = r_line.split("\t")
        if srcTime > float(objs[0].split(":")[1]):
            start_pos += 1
        if float(objs[0].split(":")[1]) > srcTime + 3:
            # 遅延が3秒以上のパケットはpdrにカウントしない
            print("search aborted!")
            break
        if sn == int(objs[3].split(":")[1]) and pcamNo == int(objs[1].split(":")[1]):
            if str(targetTime) in rcvd_counts:
                rcvd_counts[str(targetTime)] += 1
            else:
                rcvd_counts[str(targetTime)] = 1
            break
    lastSn = sn

for key in rcvd_counts:
    print(key, float(rcvd_counts[key])/float(send_counts[key]))
