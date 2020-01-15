import subprocess
import csv
import sys


with open("index.txt", 'r') as f:
    file_index = int(f.read())
with open('fng.csv', newline='') as csvfile:
    index = 0
    fng = csv.reader(csvfile, delimiter=',', quotechar='"')
    for c in fng:
        if(index < file_index):
            index += 1
        else:
            with open("base.sh", 'r') as f:
                b = f.read()
            p = c[-1].split("/")
            if(len(p) == 3):
                s = "{:02d}{:02d}{:04d}".format(int(p[0]), int(p[1]), int(p[2]))
                c[-1] = s
            p = c[2].split(' ')
            with open("out.sh", 'w') as f:
                f.write(b + "\n")
                for i in range(len(c)):
                    if(i == 2):
                        p = c[i].split(' ')
                        for n in range(len(p)):
                            # subprocess.run(["xdotool", "type", p[n]])
                            f.write("xdotool type \"{}\"\n".format(p[n]))
                            # subprocess.run(["xdotool", "key", "space"])
                            f.write('xdotool key space\n')
                    else:
                        f.write("xdotool type \"{}\"\n".format(c[i]))
                    f.write('xdotool key Tab\n')
            subprocess.run(["bash", "out.sh"])
            index += 1
            with open("index.txt", 'w') as f:
                f.write(str(index))

            print("enter to continue")
            sys.stdin.readline()