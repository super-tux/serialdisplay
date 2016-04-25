#!/usr/bin/python3

import serial
import io
import os
import time

class display(object):
    """docstring for display"""
    def __init__(self, port, baud):
        super(display, self).__init__()
        self.ser = serial.Serial(port, baud)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))
        self.printd('\x1F')
    def printd(self, str):
        self.sio.write(str)
        self.sio.flush()
    def cursor(self, b):
        if(b): self.printd('\x13')
        else: self.prind('\x14')


class scrolltext(object):
    """docstring for scrolltext"""
    def __init__(self, text, length):
        super(scrolltext, self).__init__()
        self.len = length
        self.pos = 0
        self.text = rpad(text, length)
    def shift(self):
        self.pos += 1
        if(self.pos > len(self.text) - self.len): self.pos = 0
    def getstring(self):
        return self.text[self.pos:self.pos+self.len]
    def change(self, newtext):
        if(newtext != self.text):
            self.pos = 0
            self.text = rpad(newtext, self.len)

def rpad(s, l):
    if(len(s) < l):
        s += (l - len(s)) * " "
    return s

def pos(p):
    return "\x10" + chr(p)

def getstuff(cmd):
    return os.popen(cmd).readlines()[0].strip("\n")


d1 = display('/dev/ttyUSB0', 2400)

mpc_cmd = "mpc -h 192.168.0.2 -P password current"
#song = scrolltext("ganz langer text der devinitiv laenger als 40 zeichen ist", 39)
song = scrolltext("", 39)

while 1:
    date = rpad(getstuff("date"), 40)
    song.change(getstuff(mpc_cmd))
    d1.printd(pos(0) + date)
    d1.printd(pos(40) + song.getstring())
    song.shift()
    time.sleep(1)
