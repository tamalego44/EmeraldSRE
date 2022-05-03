
from io import TextIOWrapper
from main import *
from gui import *

romFileName = 'rom.gba'

inFileName = "save2.sav"
startLocation = 0x11000
# 0x2000 and 0x11000?
# outFileName = "new.sav"
# dataFileName = "save.data"

def searchString(buff: bytearray, string):
    l = len(string)
    b = bytes(codecs.encode(string, encoding='pkmn'))
    indices = [0]
    while indices[-1] != -1:
        indices.append(buff.find(b, indices[-1] + 1))
    return indices[1:-1]

def replaceString(buff: bytearray, original, new, count=-1):
    assert len(original) == len(new)
    bo = bytearray(codecs.encode(original, encoding='pkmn'))
    bn = bytearray(codecs.encode(new, encoding='pkmn'))
    return buff.replace(bo, bn, count)

def dump(buff, minaddr, size):
        width = 0x10
        maxaddr = minaddr + size

        for addr in range(minaddr, maxaddr, width):
            bs = buff[addr:addr+width]
            #print address
            print("0x%08X" % addr, end=' | ')

            #print bytes
            for b in bs:
                print("%02X " % b, end='')

            print("| ", end='')
            # print encoding
            # for b in codecs.decode(bs, encoding='pkmn'):
            #     print(b, end=' ')

            for b in bs:
                d = codecs.decode(b.to_bytes(1, 'little'), encoding='pkmn')
                #print(len(d))
                print("%3s" % d, end=' ')

            print()
    
with open(romFileName, 'rb+') as file:
    buff = bytearray(file.read())
    # indices = searchString(buff, "CONTINUE")
    # print(indices)
    # buff = replaceString(buff, "CONTINUE", "TESTTEST")
    indices = searchString(buff, "hello")
    print(["%X" % s for s in indices])
    
    dump(buff, indices[1] - 0x80, 0x160)

# Write to new file
with open('newrom.gba', 'wb+') as file:
    file.write(buff)
exit()

