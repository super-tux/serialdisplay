#!/usr/bin/python3
import display as d
import re
import os
import time


def pos(p):
    return "\x10" + chr(p)

def getstuff(cmd):
    return [s.strip("\n") for s in os.popen(cmd).readlines()]


d1 = d.display('/dev/ttyUSB0', 2400)
d1.cursor(0)

mpc_cmd = "mpc -h 192.168.0.2 -P password"
#song = scrolltext("ganz langer text der devinitiv laenger als 40 zeichen ist", 39)
#song = d.scrolltext(0, 39, "foo")
#prog = d.pbar(40, 39, 0)
d1.add("song", d.scrolltext(0, 39, "foo"))
d1.add("prog", d.pbar(40, 39, 0))

#p = int(re.search("\d+", re.search("\(\d*\%\)", os.popen(mpc_cmd).readlines()[1]).group()).group())

while 1:
    #date = rpad(getstuff("date"), 40)
    status = getstuff(mpc_cmd)
    d1.fields["prog"].change(int(re.search("\((\d+)\%\)", status[1]).group(1)))
    d1.fields["song"].change(status[0])
    #d1.printd(pos(0) + date)
    d1.update()
    d1.fields["song"].shift()
    time.sleep(1)
