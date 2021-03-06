import serial

def rpad(s, l):
    if(len(s) < l):
        s += (l - len(s)) * " "
        return s
    return s

def lpad(s, l):
    if(len(s) < l):
        s = (l - len(s)) * " " + s
        return s
    return s

def mpad(s, l):
    if(len(s) < l):
        r = l - len(s)
        s = int(.5 * r) * " " + s + (r - int(.5 * r)) * " "
        return s
    return s

class display(object):
    """docstring for display"""
    def __init__(self, port, baud):
        super(display, self).__init__()
        self.ser = serial.Serial(port, baud)
        self.printd('\x1F')
        self.fields = {}
    def printd(self, str):
        self.ser.write(str.encode('ascii', 'ignore'))
        self.ser.flush()
    def cursor(self, b):
        if(b): self.printd('\x13')
        else: self.printd('\x14')
    def update(self):
        [self.printd(f.getstring()) for f in self.fields.values()]
    def add(self, name, f):
        self.fields[name] = f
    def remove(self, name):
        self.fields.pop(name)

class field(object):
    """docstring for field"""
    def __init__(self, position, length):
        super(field, self).__init__()
        self.pos = position
        self.len = length
        self.visible = True
    def getstring(self):
        if(self.visible):
            return "\x10" + chr(self.pos) + self.prepstring()

class text(field):
    """docstring for text"""
    def __init__(self, position, length, textstr = "", bound = "l"):
        super(text, self).__init__(position, length)
        self.bound = bound
        self.change(textstr)
    def change(self, text):
        if((self.bound == "r") | (self.bound == "right")):
            self.text = lpad(text, self.len)
        elif((self.bound == "l") | (self.bound == "left")):
            self.text = rpad(text, self.len)
        elif((self.bound == "m") | (self.bound == "middle")):
            self.text = mpad(text, self.len)
        else:
            raise Exception("fuck you!")
    def prepstring(self):
        return(self.text[0:self.len])


class scrolltext(text):
    """docstring for scrolltext"""
    def __init__(self, position, length, text, bound):
        super(scrolltext, self).__init__(position, length, text, bound)
        self.spos = 0
        self.change(text)
    def shift(self):
        self.spos += 1
        if(self.spos > len(self.text) - self.len): self.spos = 0
    def prepstring(self):
        return self.text[self.spos:self.spos+self.len]
    def change(self, newtext):
        super(scrolltext, self).change(newtext)
        if(newtext != self.text):
            self.spos = 0

class pbar(field):
    """docstring for pbar"""
    def __init__(self, position, length, value):
        super(pbar, self).__init__(position, length)
        self.val = value
    def prepstring(self):
        p = int(self.val * self.len / 100)
        return p * "#" + (self.len - p) * "-"
    def change(self, value):
        self.val = value
