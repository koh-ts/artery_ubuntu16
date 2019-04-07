from pathlib import Path

# methods = [ "naive_grid_pcam", "passive_grid_pcam", "original_pcam"]
methods = ["original_pcam"]
pcam_nums = ["num_5", "num_10", "num_15"]
# pcam_nums = ["num_10"]

simStartTime = 200
simTotalInterval = 15

map_type = "paris"

offset = 0


for method in methods:
    for pcam_num in pcam_nums:
        outputDir = Path("output/" + map_type + "/" + method + "/" + pcam_num + "/sim_all/")
        files = outputDir.glob("*")
        for file in files:
            print(file)
            if "node" in str(file):
                print("passed")
                continue
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
                    # 次のシミュレーションの最初の行を探している for oline in lines[startPos:i]参照
                    if float(objs[0].split(":")[1]) >= simStartTime + simTotalInterval * (count + 1):
                        of_path = str(outputDir.parent) + "/sim_" + str(count + offset) + "/" + file.name
                        of = open(of_path,mode="w")
                        for oline in lines[startPos:i]:
                            objs = oline.split("\t")
                            objs[0] = objs[0].split(":")[0] + ": " + str(float(objs[0].split(":")[1]) + offset * simTotalInterval)
                            if "rsu" in str(file):
                                objs[2] = objs[2].split(":")[0] + ": " + str(float(objs[2].split(":")[1])+ offset * simTotalInterval * pow(10,6))
                            oline = "\t".join(objs)
                            of.write(oline)
                        startPos = i
                        count += 1
                of_path = str(outputDir.parent) + "/sim_" + str(count + offset) + "/" + file.name
                of = open(of_path,mode="w")
                for oline in lines[startPos:i]:
                    objs = oline.split("\t")
                    objs[0] = objs[0].split(":")[0] + ": " + str(float(objs[0].split(":")[1]) + offset * simTotalInterval)
                    if "rsu" in str(file):
                        objs[2] = objs[2].split(":")[0] + ": " + str(float(objs[2].split(":")[1]) + offset * simTotalInterval * pow(10,6))
                    oline = "\t".join(objs)
                    of.write(oline)
