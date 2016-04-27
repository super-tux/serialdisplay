import serial
import io

def rpad(s, l):
    if(len(s) < l):
        s += (l - len(s)) * " "
        return s

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
        super(scrolltext, self).__init__(position, length)
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

class pbar(field):
    """docstring for pbar"""
    def __init__(self, position, length, value):
        super(pbar, self).__init__(position, length)
        self.val = value
    def prepstring(self):
        p = int(self.val * self.len / 100)
        return p * "#" + (self.len - p) * "-"
    def update(self, value):
        self.val = value
