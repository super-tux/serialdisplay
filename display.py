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
        else: self.printd('\x14')

class field(object):
    """docstring for field"""
    def __init__(self, position, length):
        super(field, self).__init__()
        self.pos = position
        self.len = length
    def getstring(self):
        return "\x10" + chr(self.pos) + self.prepstring()

class scrolltext(field):
    """docstring for scrolltext"""
    def __init__(self, position, length, text):
        super(scrolltext, self, position, length).__init__()
        self.spos = 0
        self.text = rpad(text, length)
    def shift(self):
        self.spos += 1
        if(self.spos > len(self.text) - self.len): self.spos = 0
    def prepstring(self):
        return self.text[self.spos:self.spos+self.len]
    def update(self, newtext):
        if(newtext != self.text):
            self.spos = 0
            self.text = rpad(newtext, self.len)

class pbar(object):
    """docstring for pbar"""
    def __init__(self, length, value):
        super(pbar, self).__init__()
        self.len = length
        self.val = value
    def getstring(self):
        p = int(self.val * self.len)
        return p * "#" + (self.len - p) * "-"
    def update(self, value):
        self.val = value

def rpad(s, l):
    if(len(s) < l):
        s += (l - len(s)) * " "
    return s

def pos(p):
    return "\x10" + chr(p)

def getstuff(cmd):
    return os.popen(cmd).readlines()[0].strip("\n")


d1 = display('/dev/ttyUSB0', 2400)
d1.cursor(0)

mpc_cmd = "mpc -h 192.168.0.2 -P password current"
#song = scrolltext("ganz langer text der devinitiv laenger als 40 zeichen ist", 39)
song = scrolltext(40, 39, "")

while 1:
    date = rpad(getstuff("date"), 40)
    song.update(getstuff(mpc_cmd))
    d1.printd(pos(0) + date)
    d1.printd(song.getstring())
    song.shift()
    time.sleep(1)
