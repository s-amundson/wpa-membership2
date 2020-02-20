# from DbHelper import DbHelper
# from CurrentRegistration import CurrentRegistration
#
# # from helpers import apology, login_required
# from MemberDb import MemberDb
# from FamilyClass import FamilyClass
#
# import subprocess
# import csv
# import sys
#
# db = DbHelper()
# mem = MemberDb(db)
# with open("importer/index.txt", 'r') as f:
#     file_index = int(f.read())
# with open('importer/fng.csv', newline='') as csvfile:
#     index = 0
#     fng = csv.reader(csvfile, delimiter=',', quotechar='"')
#     for c in fng:
#         if (index < file_index):
#             index += 1
#         else:
#             print(c)
#             p = c[-1].split("/")
#             if(len(p) == 3):
#                 s = "{:04d}-{:02d}-{:02d}".format(int(p[2]), int(p[0]), int(p[1]))
#                 c[-1] = s
#             m = {
#                 "first_name": c[0],
#                 "last_name": c[1],
#                 "street": c[2],
#                 "city": c[3],
#                 "state": c[4],
#                 "zip": c[5],
#                 "phone": c[7],
#                 "email": c[6],
#                 "dob": c[8],
#                 "level": 'standard',
#                 "benefactor": 0,
#                 "fam": "NULL"
#                 #  GivenName,Surname,StreetAddress,City,State,ZipCode,EmailAddress,TelephoneNumber,Birthday
#             }
#             mem.setbyDict(m)
#             mem.add(None)
#             index += 1
#             with open("importer/index.txt", 'w') as f:
#                 f.write(str(index))
#             print("enter to continue")
#             sys.stdin.readline()
#
#         # p = c[2].split(' ')
#
#             # with open("out.sh", 'w') as f:
#             #     f.write(b + "\n")
#             #     for i in range(len(c)):
#             #         if(i == 2):
#             #             p = c[i].split(' ')
#             #             for n in range(len(p)):
#             #                 # subprocess.run(["xdotool", "type", p[n]])
#             #                 f.write("xdotool type \"{}\"\n".format(p[n]))
#             #                 # subprocess.run(["xdotool", "key", "space"])
#             #                 f.write('xdotool key space\n')
#             #         else:
#             #             f.write("xdotool type \"{}\"\n".format(c[i]))
#             #         f.write('xdotool key Tab\n')
#             # subprocess.run(["bash", "out.sh"])
#             # index += 1
#             # with open("index.txt", 'w') as f:
#             #     f.write(str(index))
#             #
#             # print("enter to continue")
#             # sys.stdin.readline()

# import hashlib
# hash_obj = hashlib.md5(b'fTNNi2gLPqPQq4ZO3GQZ')
# print(hash_obj.hexdigest())
members = "12, 13, "
print(members.strip(", "))