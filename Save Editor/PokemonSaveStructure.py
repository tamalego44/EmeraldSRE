from pkmn_codec import *
codecs.register(custom_search_function)

section_info = {
    0: (3884, "Trainer info"),
    1:	(3968, "Team / items"),
    2:	(3968,	"Game State"),
    3:	(3968,	"Misc Data"),
    4:	(3848,	"Rival info"),
    5:	(3968,	"PC buffer A"),
    6:	(3968,	"PC buffer B"),
    7:	(3968,	"PC buffer C"),
    8:	(3968,	"PC buffer D"),
    9:	(3968,	"PC buffer E"),
    10:	(3968,	"PC buffer F"),
    11:	(3968,	"PC buffer G"),
    12:	(3968,	"PC buffer H"),
    13:	(2000,	"PC buffer I")
}


# (section, offset, size, decodeFunc, encodeFunc)
fields = {
    "Name": (0, 0x0, 0x7,
        lambda x, y: codecs.decode(x.to_bytes(7, 'little'), encoding='pkmn'),
        lambda x, y: int.from_bytes(codecs.encode(x, encoding='pkmn'), "little")
    ),
    "Gender": (0, 0x8, 0x1,
        lambda x, y: "M" if x == 0 else "F",
        lambda x, y: 0 if x=="M" else 1
    ),
    "Trainer ID": (0, 0xA, 0x4,
        lambda x, y: {"Public": x & 0xFFFF,
                   "Secret": (x >> 16) & 0xFFFF},
        lambda x, y: x["Public"] + (x["Secret"] << 16)
    ),
    "Time Played": (0, 0xE, 0x5,
        lambda x, y: {"Hours": x & 0xFFFF,
                   "Minutes": (x >> 16) & 0xFF,
                   "Seconds": (x >> 24) & 0xFF,
                   "Frames": (x >> 32) & 0xFF},
        lambda x, y: x["Hours"] + (x["Minutes"] << 16) + (x["Seconds"] << 24) + (x["Frames"] << 32)
    ),
    "Options": (0, 0x13, 0x3,
        lambda x, y: x,
        lambda x, y: x
    ),
    "Security Key": (0, 0xAC, 0x4,
        lambda x, y: x,
        lambda x, y: x,
    ),
    "Team Size": (1, 0x234, 0x4,
        lambda x, y: x,
        lambda x, y: x    
    ),
    "Money": (1, 0x490, 0x4,
        lambda x, y: x ^ y,
        lambda x, y: x ^ y
    ),
    "Coins": (1, 0x494, 0x2, 
        lambda x, y: x ^ (y & 0xFFFF),
        lambda x, y: x ^ (y & 0xFFFF)
    )
}

#TODO: custom codec
#https://stackoverflow.com/questions/38777818/how-do-i-properly-create-custom-text-codecs

# char_encodings = {}
# with open("encoding.txt", "rb") as file:
#     i = 0
#     for line in file:
#         char_encodings[i] = line
#         i += 1

#print(char_encodings)

def read(buff, index, nBytes):
    return sum([buff[index + n] << (8 * n) for n in range(nBytes)])

def write(buff, index, data, nBytes=None):
    if nBytes == None:
        while data > 0:
            buff[index] = data & 0xFF
            data >>= 8
            index += 1
    else:
        for i in range(nBytes):
            if data > 0:
                buff[index] = data & 0xFF
                data >>= 8
            else:
                buff[index] = 0
            index += 1
    
    return buff

# def toString(num):
#     ret = ""
#     while num > 0:
#         ret += char_encodings[(num & 0xFF)]
#         num >>= 8
#     return ret

# def fromString(string):
#     ret = 0
#     for c, i in zip(string, range(len(string))):
#         ret += [k for k, v in char_encodings.items() if v == c][0] << (8*i)
#     return ret

class section:
    def __init__(self, offset, data, securityKey = None):
        self.offset = offset
        self.buff = data
        self.id = id = read(self.buff, 0xFF4, 2)
        self.size, self.name = section_info[id]
        self.checksum = read(self.buff, 0xFF6, 2)
        
        self.securityKey = securityKey

        self.generate_section_data()

    def calc_checksum(self):
        check = 0
        for i in range(0, self.size, 4):
            check += read(self.buff, i, 4)
        
        check = (check + (check >> 16)) & 0xFFFF
        return check

    def generate_section_data(self):
        self.raw_data = {}
        self.data = {}

        for field, value in fields.items():
            if value[0] == self.id:
                self.raw_data[field] = read(self.buff, value[1], value[2])
                self.data[field] = value[3](self.raw_data[field], self.securityKey)

    def updateBuffer(self, newData):

        #print(newData)
        for k,v in newData.items():
            field = fields[k]
            self.raw_data[k] = field[4](v, self.securityKey)
            self.data[k] = v
            write(self.buff, field[1], self.raw_data[k], field[2])
        
        #Fix checksum
        write(self.buff, 0xFF6, self.calc_checksum(), 2)

    def __str__(self):
        ret = "Section %d (%s): Checksum validated: %s\n" % (self.id, self.name, self.checksum == self.calc_checksum())
        for k,v in self.data.items():
            ret += "%s: %s\n" % (k, v)
        return ret

    

class saveFile:
    def __init__(self, filename, offset):
        self.filename = filename
        with open(self.filename, 'rb+') as file:
            self.buff = bytearray(file.read())
        self.offset = offset

        self.sections = []
        self.securityKey = None
        for i in range(14):
            data = self.buff[(0x1000 * i) + self.offset:(0x1000 * (i+1) + self.offset)]
            s = section((0x1000 * i) + self.offset, data, self.securityKey)
            # if s.checksum != s.calc_checksum():
            #     print("Section %s: checksums do not match, fixing" % s.name)
            #     buff[(0x1000 * i) + startLocation]
            #     buff = write(buff, startLocation + (0x1000 * i) + 0xFF6, s.calc_checksum(), 2)
            #     print(s)
            # if s.id == 1:
            #     print(s)

            if s.id == 0:
                if len(self.sections) != 0: # if we find another section 0, end processing
                    break
                self.securityKey = s.raw_data["Security Key"]
            
            self.sections.append(s)
    
    def export(self, filename):
        # Write to save file
        for section in self.sections:
            #self.buff = write(self.buff, section.offset, section.buff, 0x1000)
            # self.buff[section.offset] = section.buff
            # for i in range(0x1000):
            self.buff = self.buff[:section.offset] + section.buff + self.buff[section.offset + 0x1000:]
        with open(filename, 'wb+') as file:
            file.write(self.buff)