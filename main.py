#!/usr/bin/python3
import display as d
import re
import os
import time


def pos(p):
    return "\x10" + chr(p)

def getstuff(cmd):
    return os.popen(cmd).readlines()[0].strip("\n")


d1 = d.display('/dev/ttyUSB0', 2400)
d1.cursor(0)

mpc_cmd = "mpc -h 192.168.0.2 -P password"
#song = scrolltext("ganz langer text der devinitiv laenger als 40 zeichen ist", 39)
song = d.scrolltext(0, 39, "foo")
prog = d.pbar(40, 39, 0)

#p = int(re.search("\d+", re.search("\(\d*\%\)", os.popen(mpc_cmd).readlines()[1]).group()).group())

while 1:
    #date = rpad(getstuff("date"), 40)
    prog.update(int(re.search("\d+", re.search("\(\d*\%\)", os.popen(mpc_cmd).readlines()[1]).group()).group()))
    song.update(getstuff(mpc_cmd))
    #d1.printd(pos(0) + date)
    d1.printd(prog.getstring())
    d1.printd(song.getstring())
    song.shift()
    time.sleep(1)
