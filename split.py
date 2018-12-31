from pathlib import Path

methods = ["naive_grid_pcam"]#, "naive_grid_pcam", "passive_grid_pcam"]
pcam_nums = ["num_5"]#, "num_10", "num_15"]

simStartTime = 200
simTotalInterval = 15

for method in methods:
    for pcam_num in pcam_nums:
        outputDir = Path("output/" + method + "/" + pcam_num + "/sim_all/")
        files = outputDir.glob("*")
        for file in files:
            print(file)
            with file.open() as f:
                lines = f.readlines()
            if len(lines) == 0:
                for path in outputDir.parent.glob("sim_*"):
                    if "sim_all" in str(path):
                        continue
                    else:
                        f = open(str(path) + "/" + file.name, mode="w")
                        f.close()
            else:
                count = 0
                startPos = 0
                for i,line in enumerate(lines):
                    objs = line.split("\t")
                    if float(objs[0].split(":")[1]) >= simStartTime + simTotalInterval * (count + 1):
                        of_path = str(outputDir.parent) + "/sim_" + str(count) + "/" + file.name
                        of = open(of_path,mode="w")
                        for oline in lines[startPos:i]:
                            of.write(oline)
                        startPos = i
                        count += 1
                of_path = str(outputDir.parent) + "/sim_" + str(count) + "/" + file.name
                of = open(of_path,mode="w")
                for oline in lines[startPos:i]:
                    of.write(oline)
