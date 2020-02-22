from machine import Pin
from machine import Timer

import time
from neopixel import NeoPixel

gamma8 = [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
            1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
            2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
            5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
           10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
           17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
           25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
           37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
           51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
           69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
           90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
          115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
          144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
          177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
          215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255]

class Hand:
    def __init__(self, total_indexes, max_ticks, max_intensity):
        self.total_indexes = total_indexes
        self.max_ticks = max_ticks
        self.max_intensity = max_intensity
        self.count = 0

    def tick(self, incr = 1):
        retval = 0
        if self.count+incr >= self.max_ticks:
            retval = 1
        self.count = (self.count+incr)%self.max_ticks
        return retval

    def intensity(self):
        return (self.max_intensity//(self.max_ticks//self.total_indexes))*(self.count%(self.max_ticks//self.total_indexes))

    def current(self):
        return self.count//(self.max_ticks//self.total_indexes)

    def prior(self):
        return (self.current()-1)%self.total_indexes

    def next(self):
        return (self.current()+1)%self.total_indexes

cnt = 12
np = NeoPixel(Pin(14), cnt)

z = []
for x in range(cnt):
    z.append(0)

s = Hand(cnt, 60, 150)
m = Hand(cnt, 60, 150)
h = Hand(cnt, 12, 150)

def intHandler(timer):
    state = machine.disable_irq()
    #print(s.count, s.intensity(), s.max_intensity-s.intensity())
    r = z.copy()
    g = z.copy()
    b = z.copy()
    r[s.current()] = gamma8[s.max_intensity-s.intensity()]
    r[s.next()]    = gamma8[s.intensity()]
    g[m.current()] = gamma8[m.max_intensity-m.intensity()]
    g[m.next()]    = gamma8[m.intensity()]
    b[h.current()] = gamma8[h.max_intensity-h.intensity()]
    b[h.next()]    = gamma8[h.intensity()]
    for x in range(cnt):
        np[x] = (r[x],g[x],b[x])
    np.write()
    if s.tick():
        if m.tick():
            h.tick()
    machine.enable_irq(state)

timer = machine.Timer(0)
timer.init(freq=1, callback=intHandler)

while True:
    pass
