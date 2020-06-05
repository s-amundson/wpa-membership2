import subprocess
import csv
import sys

WindowID = 46137347
# with open("index.txt", 'r') as f:
#     file_index = int(f.read())
# with open('fng.csv', newline='') as csvfile:
#     index = 0
#     fng = csv.reader(csvfile, delimiter=',', quotechar='"')
#     for c in fng:
#         if(index < file_index):
#             index += 1
#         else:
#             with open("base.sh", 'r') as f:
#                 b = f.read()
#             p = c[-1].split("/")
#             if(len(p) == 3):
#                 s = "{:04d}{:02d}{:02d}".format(int(p[2]), int(p[0]), int(p[1]))
#                 print(f"dob= {int(p[2])}-{int(p[0])}-{int(p[1])}")
#                 c[-1] = s
#             p = c[2].split(' ')
#             with open("out.sh", 'w') as f:
#                 f.write(b + "\n")
#                 for i in range(len(c)):
#                     if(i == 2):
#                         p = c[i].split(' ')
#                         for n in range(len(p)):
#                             # subprocess.run(["xdotool", "type", p[n]])
#                             f.write("xdotool type \"{}\"\n".format(p[n]))
#                             # subprocess.run(["xdotool", "key", "space"])
#                             f.write('xdotool key space\n')
#                     else:
#                         f.write("xdotool type \"{}\"\n".format(c[i]))
#                     f.write('xdotool key Tab\n')
#             subprocess.run(["bash", "out.sh"])
#             index += 1
#             with open("index.txt", 'w') as f:
#                 f.write(str(index))
#
#             print("enter to continue")
#             sys.stdin.readline()

with open('fng.csv', newline='') as csvfile:
    with open("index.txt", 'r') as f:
        file_index = int(f.read())
    fields = ['GivenName', 'Surname', 'StreetAddress', 'City', 'State', 'ZipCode', 'EmailAddress',
              'TelephoneNumber', 'Birthday']
    rows = csv.DictReader(csvfile, fieldnames=fields)
    index = 0

    for row in rows:
        if index > file_index:
            print(row)
            p = row['Birthday'].split("/")
            if(len(p) == 3):
                row['Birthday'] = "{:04d}-{:02d}-{:02d}".format(int(p[2]), int(p[0]), int(p[1]))
                print(f"dob= {int(p[2])}-{int(p[0])}-{int(p[1])}")
            with open("out.sh", 'w') as f:
                f.write(f"xdotool windowactivate {WindowID}\n")
                f.write(f"xdotool type {row['GivenName']}\n")
                f.write('xdotool key Tab\n')
                f.write(f"xdotool type {row['Surname']}\n")
                f.write('xdotool key Tab\n')
                f.write(f"xdotool type {row['Birthday']}\n")
                f.write('xdotool key Tab\n')
                # f.write('xdotool key Tab\n')
                s = row['StreetAddress'].split(' ')
                for w in range(len(s)):
                    f.write(f"xdotool type {s[w]}\n")
                    f.write('xdotool key space\n')
                f.write('xdotool key Tab\n')
                s = row['City'].split(' ')
                for w in range(len(s)):
                    f.write(f"xdotool type {s[w]}\n")
                    f.write('xdotool key space\n')
                f.write('xdotool key Tab\n')
                f.write(f"xdotool type {row['State']}\n")
                f.write('xdotool key Tab\n')
                f.write(f"xdotool type {row['ZipCode']}\n")
                f.write('xdotool key Tab\n')
                f.write(f"xdotool type {row['EmailAddress']}\n")
                f.write('xdotool key Tab\n')
                f.write(f"xdotool type {row['TelephoneNumber']}\n")

            subprocess.run(["bash", "out.sh"])

            with open("index.txt", 'w') as f:
                f.write(str(index))
            index += 1
            print("enter to continue")
            sys.stdin.readline()
        else:
            index += 1