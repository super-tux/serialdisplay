#!/usr/bin/python3

import serial
import io
import os
import time

ser = serial.Serial('/dev/ttyUSB0', 2400)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

mpc_cmd = "mpc -h 192.168.0.2 -P password current"
chars = 39

class scrolltext(object):
    """docstring for scrolltext"""
    def __init__(self, text, length):
        super(scrolltext, self).__init__()
        self.len = length
        self.pos = 0
        self.text = rpad(text, length)
    def update(self):
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

#sio.write("\x1F\x14")
#sio.flush()

#song = scrolltext("ganz langer text der devinitiv laenger als 40 zeichen ist", 39)
song = scrolltext("", 39)

while 1:
    date = rpad(getstuff("date"), 40)
    song.change(getstuff(mpc_cmd))
    sio.write(pos(0) + date)
    sio.write(pos(40) + song.getstring())
    sio.flush()
    song.update()
    time.sleep(1)
