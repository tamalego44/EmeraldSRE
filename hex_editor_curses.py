#!/usr/bin/env python

import os, msvcrt
from main import *
from gui import *
import curses
from curses import wrapper

romFileName = 'rom.gba'

inFileName = "save2.sav"
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


class Position:
    def __init__(self, maxY, maxScreenY, initialX:int=0, initialY:int=0):
        self.x = initialX
        self.y = initialY
        self.maxX = (width * 3)-2
        self.maxY = maxY
        self.maxScreenY = maxScreenY

        self.screenY = 0
    
    def addX(self, x):
        self.x = min(max(0, self.x+x), self.maxX)

    def addY(self, y):
        if self.y + y >= self.maxY or self.y + y <= 0: #update screen position if necessary
            self.screenY = min(max(0, self.screenY+y), self.maxScreenY)
        self.y = min(max(0, self.y+y), self.maxY)

    def __str__(self):
        return str((self.x, self.y))

class HexEditor:
    def __init__(self,stdscr):
        #Curses Screen setup
        self.stdscr = stdscr
        self.height = curses.LINES - 1

        curses.curs_set(2)

        #File setup
        self.open(romFileName)
        self.padl, self.padr, self.pada = self.screenSetUp()

        #Base functionality
        self.addr = 0
        self.pos = Position(self.height, self.data_height)
        self.mode = None

        #Find mode
        self.stringIndices = []

    def open(self, filename):
        with open(filename, 'rb+') as file:
            self.buff = bytearray(file.read())

    def screenSetUp(self):
        self.data_height = len(self.buff)//width
        padl, padr = curses.newpad(self.data_height, 3 * width), curses.newpad(self.data_height, width*2)
        pada = curses.newpad(self.data_height, 6)

        padl.scrollok(True)
        padr.scrollok(True)

        n = 0x1000

        #addresses
        for y in range(0, n):
            pada.addstr(y,0, "0x%04X" % (y * width))

        # divisor
        for y in range(0, curses.LINES):
            self.stdscr.addch(y, pada.getmaxyx()[1], '|')

        #hex
        for y in range(0, n):
            for x in range(0, width):
                    pos = (y * width) + (x)
                    padl.addstr(y, x * 3, ("%02X" % self.buff[pos]))
                    padl.addch(y, (x * 3) + 2, ord(' '))

        # divisor
        for y in range(0, curses.LINES):
            self.stdscr.addch(y, pada.getmaxyx()[1] + padl.getmaxyx()[1] + 1, '|')
        
        #ascii
        for y in range(0, n):
            for x in range(0, width):
                    pos = (y * width) + (x)
                    if y == 9:
                        print(pos)
                        print("\"%s\"" % (codecs.decode(self.buff[pos].to_bytes(1, 'little'), encoding='pkmn')))

                    #padr.addstr(y, x * 2, codecs.decode(self.buff[pos].to_bytes(1, 'little'), encoding='pkmn')[0])
                    padr.addch(y, x*2, ord('0') + (x+y) % 10)
                    padr.addch(y, (x * 2) + 1, ord(' '))

        # padl.refresh( 0,0, 5,5, 20,20)
        # padr.refresh( 0,0, 5,25, 20, 40,)

        return padl, padr, pada


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
        # test

        #Update cursor position
        print(self.pos.y, self.pos.x)
        self.stdscr.move(self.pos.y, self.pos.x)
        #self.padr.leaveok(1)
        #self.stdscr.leaveok(1)
        #self.padr.move(self.pos.y, self.pos.x)

        #If position dictates, fix view


        # update screen
        self.stdscr.noutrefresh()
        self.pada.noutrefresh(self.pos.screenY, 0, 0, 0,
                              0+self.height, self.pada.getmaxyx()[1])
        self.padl.noutrefresh(self.pos.screenY, 0, 0, self.pada.getmaxyx()[1] + 1, 
                              0+self.height, self.pada.getmaxyx()[1] + self.padl.getmaxyx()[1] + 1)
        self.padr.noutrefresh(self.pos.screenY, 0, 0,self.pada.getmaxyx()[1] + self.padl.getmaxyx()[1] + 2, 
                              0+self.height,self.pada.getmaxyx()[1] + self.padl.getmaxyx()[1] + self.padr.getmaxyx()[1] + 2)
        curses.doupdate()
        return

        size = 0x10 * height
        maxaddr = self.addr + size

        os.system('cls')
        for y, addr in enumerate(range(self.addr, maxaddr, width)):
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
        if (self.mode == "f"):
            print("Find mode activated")
            print("String: %s (%d of %d)" % (self.string, self.stringIndex, len(self.stringIndices)))
            print("s: set string, n: next, p: prev, f: exit find mode")

    def goto(self, n: int):
        self.pos.x = n % width
        self.addr = (n // width) * width

    def run(self):
        #self.stdscr.clear()
        while True:
            self.display()
            userInput = self.stdscr.getkey()
            print(userInput)
            if userInput == 'd':
                exit()

            elif userInput == '♥': # TODO: this should be Ctrl+C
                exit()
            elif userInput == 'KEY_UP':
                self.pos.addY(-1)
                #self.padl.scroll(-1)
            elif userInput == 'KEY_LEFT':
                self.pos.addX(-1)
                if self.pos.x % 3 == 2:
                    self.pos.addX(-1)
            elif userInput == 'KEY_DOWN':
                self.pos.addY(1)
            elif userInput == 'KEY_RIGHT':
                self.pos.addX(1)
                if self.pos.x % 3 == 2:
                    self.pos.addX(1)
            elif userInput == 'p':
                self.padl.scroll()
                self.padr.scroll()
            elif userInput == 'o':
                self.padl.scroll(-1)
                self.padr.scroll(-1)
                
            #GOTO
            elif userInput == 'g':
                n = int(input("goto:"), 16)
                self.goto(n)
            #Modes
            elif userInput == 'f':
                self.mode = None if self.mode == 'f' else 'f'
                self.string = None
                self.stringIndex = 0
            # Find mode
            elif self.mode == 'f':
                if userInput == 's':
                    self.string = input("Search string:")
                    self.stringIndices = searchString(self.buff, self.string)
                    self.goto(self.stringIndices[self.stringIndex])
                elif userInput == 'n':
                    self.stringIndex += 1
                    self.goto(self.stringIndices[self.stringIndex])
                elif userInput == 'p':
                    self.stringIndex -= 1
                    self.goto(self.stringIndices[self.stringIndex])
            #Normal Mode
            else:
                if userInput == 's':
                    print("Todo: Save")
                    msvcrt.getch()
                elif userInput == '\r':
                    print("Todo: enter value")
                    msvcrt.getch()
                elif userInput == 'l':
                    print("Press Key: ")
                    userInput = msvcrt.getch()
                    print(userInput)
                    print(msvcrt.getch())
                    msvcrt.getch()

def main(stdscr):
    
    p = HexEditor(stdscr)
    p.run()

if __name__ == "__main__":
    wrapper(main)