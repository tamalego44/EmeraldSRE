# inFileName = input("File you're fixing: ")
# startlocation = int(input("Save file index in hex:"), 16) #TODO: This should be automatic
# outFileName = input("Save as: ")

from main import *
from gui import *

inFileName = "romhack.sav"
startLocation = 0x2000
# 0x2000 and 0x11000?
# outFileName = "new.sav"
# dataFileName = "save.data"


# Read save file
# with open(inFileName, 'rb+') as file:
#     buff = bytearray(file.read())

save = saveFile(inFileName, startLocation)
# sections = []
# for i in range(14):
#     data = buff[(0x1000 * i) + startLocation:(0x1000 * (i+1) + startLocation)]
#     s = section(data)
#     if s.checksum != s.calc_checksum():
#         print("Section %s: checksums do not match, fixing" % s.name)
#         buff[(0x1000 * i) + startLocation]
#         buff = write(buff, startLocation + (0x1000 * i) + 0xFF6, s.calc_checksum(), 2)
#         print(s)
#     if s.id == 1:
#         print(s)
#     sections.append(s)

# # Write data to data file
# with open(dataFileName, 'w+') as file:
#     for s in sections:
#         file.write(s.__str__())

# # Write to save file
# with open(outFileName, 'wb+') as file:
#     file.write(buff)

def main(): 
    GUISave(save).mainloop()

if __name__ == '__main__':
    main()