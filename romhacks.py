from pkmn_codec import *
codecs.register(custom_search_function)

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

filename = input("Input file:")
with open(filename, 'rb+') as file:
    buff = bytearray(file.read())

listPos = 0x3185c8
starterPos = 0x5b1df8
outputfilename = input("Save as:")

hacks = ['starters', 'firstenc']

pokemon_names = []
for i in range(500):
    name = codecs.decode(buff[listPos + (0xb * i): listPos + (0xb * (i+1))], encoding='pkmn').split('.')[0]
    
    if name == '-':
        break

    pokemon_names.append(name)

#print(pokemon_names)

def print_starters():
    for i in range(0,6,2):
        starter = buff[starterPos + i:starterPos+2 + i]
        starter = int.from_bytes(starter, 'little')
        print(pokemon_names[starter])

def possible_starters(name):
    return [pokemon_name for pokemon_name in pokemon_names if pokemon_name.startswith(name)]


def set_starter(num, index):
    # buff[starterPos + (index*2):starterPos + ((index+1)*2)] = num.toBytes()
    write(buff, starterPos + (index*2), num, 2)

def input_pokemon():
    name = input(":").upper()
    while name not in pokemon_names:
        print("No such pokemon, perhaps you meant one of the following:")
        print(possible_starters(name))
        name = input(":").upper()
    
    val = pokemon_names.index(name)
    print("%0X" % val)
    return val

# def complete(text, state):
#     for cmd in possible_starters(text):
#         if cmd.startswith(text):
#             if not state:
#                 return cmd
#             else:
#                 state -= 1

# readline.parse_and_bind("tab: complete")
# readline.set_completer(complete)
# input('Enter section name: ')

def main():

    #select hack
    hack = ''
    while hack not in hacks:
        print("valid hacks: %s" % hacks)
        hack = input(":")

    if hack == "starters":

        print("Current starters:")
        print_starters()

        print("Input 3 new starters:")
        done = 0
        while done < 3:
            val = input_pokemon()
            set_starter(val, done)
            done += 1

    
    elif hack == "firstenc":
        addr = 0x32706
        print("Input the desired first encounter pokemon:")
        val = input_pokemon()

        if (val % 2 == 0) and (val // 2 <= 0xff):
            write(buff, addr, val, 1)
            #write(buff, )
            #TODO: re-set LSL instruction test
        elif val <= 0xff:
            write(buff, addr, val, 1)
            write(buff, addr+2, 0x46c0, 2)
        elif val <= 0x1fe:
            val = val - 0xff
            write(buff, addr, val, 1)
            write(buff, addr+2, 0x31FF, 2)
        
        else:
            print("pokemon ID not yet supported")


    with open(outputfilename, 'wb+') as file:
        file.write(buff)

if __name__ == "__main__":
    main()
