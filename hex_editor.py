#!/usr/bin/env python

import os, msvcrt
from main import *
from gui import *
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'rom.gba' #default file
#filename = 'dump'

#inFileName = "save2.sav"
startLocation = 0x11000
# 0x2000 and 0x11000?
# outFileName = "new.sav"
# dataFileName = "save.data"

def searchString(buff: bytearray, string):
    b = bytes(codecs.encode(string, encoding='pkmn'))
    indices = [0]
    while indices[-1] != -1:
        indices.append(buff.find(b, indices[-1] + 1))
    return indices[1:-1]

width = 0x10
height = 0x18



class Position:
    def __init__(self, initialX:int=0, initialY:int=0):
        self.x = initialX
        self.y = initialY
        self.maxX = width
        self.maxY = height

        self.addr = 0
    
    def addX(self, x):
        self.x = min(max(0, self.x+x), self.maxX)

    def addY(self, y):
        if self.y + y >= self.maxY or self.y + y <= 0: #update screen position if necessary
            #self.screenY = min(max(0, self.screenY+y), self.maxScreenY)
            new_addr = self.addr + (width * y)
            self.addr = max(0, new_addr)
        self.y = min(max(0, self.y+y), self.maxY-1)

    def currentAddress(self):
        return self.addr + (width * self.y) + self.x 

    def __str__(self):
        return str((self.x, self.y))

class HexEditor:
    def __init__(self):

        #File setup
        self.open(filename)

        #Base functionality
        self.pos = Position()
        self.mode = None

        #Find mode
        self.stringIndices = []

    def open(self, filename):
        with open(filename, 'rb+') as file:
            self.buff = bytearray(file.read())

    # def searchString(buff: bytearray, string):
    #     l = len(string)
    #     b = bytes(codecs.encode(string, encoding='pkmn'))
    #     indices = [0]
    #     while indices[-1] != -1:
    #         indices.append(buff.find(b, indices[-1] + 1))
    #     return indices[1:-1]

    # def replaceString(buff: bytearray, original, new, count=-1):
    #     assert len(original) == len(new)
    #     bo = bytearray(codecs.encode(original, encoding='pkmn'))
    #     bn = bytearray(codecs.encode(new, encoding='pkmn'))
    #     return buff.replace(bo, bn, count)

    def display(self) -> None:
        size = 0x10 * height
        maxaddr = self.pos.addr + size

        os.system('cls')
        for y, addr in enumerate(range(self.pos.addr, maxaddr, width)):
            bs = self.buff[addr:addr+width]
            #print address
            print("0x%08X" % addr, end=' | ')

            #print bytes
            for x, b in enumerate(bs):
                if y == self.pos.y and x == self.pos.x:
                    print( "\033[%dm" % 7, end='')
                print("%02X " % b, end="\033[%dm" % 0)

            print("| ", end='')
            # print encoding
            # for b in codecs.decode(bs, encoding='pkmn'):
            #     print(b, end=' ')

            for b in bs:
                d = codecs.decode(b.to_bytes(1, 'little'), encoding='pkmn')
                #print(len(d))
                print("%3s" % d, end=' ')

            print()

        #Post display info
        if (self.mode == None): # Normal Mode
            print("f: find mode, s: save, g: goto, enter: modify value")
        elif (self.mode == "f"): # Find mode
            print("Find mode activated")
            print("String: %s (%d of %d)" % (self.string, (self.stringIndex + 1), len(self.stringIndices)))
            print("s: set string, n: next, p: prev, f: exit find mode")

    def goto(self, n: int):
        self.pos.x = n % width
        self.pos.addr = (n // width) * width

    def run(self):
        #self.stdscr.clear()
        while True:
            self.display()
            userInput = msvcrt.getch()

            if userInput == b'd':
                exit()

            elif userInput == '♥': # TODO: this should be Ctrl+C
                exit()
            elif userInput == b'\xe0':
                userInput = msvcrt.getch()
                if userInput == b'H':
                    self.pos.addY(-1)
                    #self.padl.scroll(-1)
                elif userInput == b'K':
                    self.pos.addX(-1)
                elif userInput == b'P':
                    self.pos.addY(1)
                elif userInput == b'M':
                    self.pos.addX(1)
                
            #GOTO
            elif userInput == b'g':
                n = int(input("goto:"), 16)
                self.goto(n)
            #Modes
            elif userInput == b'f':
                self.mode = None if self.mode == 'f' else 'f'
                self.string = None
                self.stringIndex = 0
            # Find mode
            elif self.mode == 'f':
                if userInput == b's':
                    self.string = input("Search string:")
                    self.stringIndices = searchString(self.buff, self.string)
                    self.goto(self.stringIndices[self.stringIndex])
                elif userInput == b'n':
                    self.stringIndex = (self.stringIndex + 1) % len(self.stringIndices)
                    self.goto(self.stringIndices[self.stringIndex])
                elif userInput == b'p':
                    self.stringIndex = (self.stringIndex - 1) % len(self.stringIndices)
                    self.goto(self.stringIndices[self.stringIndex])
            #Normal Mode
            else:
                if userInput == b's':
                    #print("Todo: Save")
                    fn = input("Save as:")
                    with open(fn, 'wb+') as file:
                        file.write(self.buff)
                    print("Saved, press any button to continue")
                    msvcrt.getch()
                elif userInput == b'\r':
                    #print("Todo: enter value")
                    new = input("New value:")
                    new = int(new, 16)
                    
                    index = self.pos.currentAddress()
                    self.buff[index] = new

                    #msvcrt.getch()
                elif userInput == b'l':
                    print("Press Key: ")
                    userInput = msvcrt.getch()
                    print(userInput)
                    print(msvcrt.getch())
                    msvcrt.getch()

def main():
    p = HexEditor()
    p.run()

if __name__ == "__main__":
    main()