import sys
args = sys.argv
pcamNo = int(args[1])

pcamNum = 100

results_path = "output/output_GridWorld.pcam[" + str(pcamNo) + "].sensor.udpApp[0]_sender.txt"
results_rsu_path = "output/output_GridWorld.rsu[0].appl.middleware.CaService.txt"

analysis_pdr_path = "analysis/pdr_" + str(pcamNo) + ".txt"
analysis_delay_path = "analysis/delay_" + str(pcamNo) + ".txt"

with open(results_rsu_path) as f:
    lines = f.readlines()

for line in lines:
    objs = line.split("\t")
    if int(objs[1].split(":")[1]) > pcamNum:
        continue
    dstTime = float(objs[0].split(":")[1])
    print(dstTime)
    srcTime = float(objs[2].split(":")[1])
