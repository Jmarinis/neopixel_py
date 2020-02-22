from machine import Pin
from neopixel import NeoPixel
import time

cnt = 12
np = NeoPixel(Pin(14), cnt)
j = 5
d = 1

mi = 30
si = 1

r = si
ri = 0
g = 0
gi = 0
b = 50
bi = -si

i = 0
k = 1

while True:
    i = (i+k)%(cnt-1)
    np[0] = (r,g,b)
    np.write()
    time.sleep(1/j)
    np[0] = (0,0,0)
    np[i+1] = (r,g,b)
    np.write()
    np[i+1] = (0,0,0)
    time.sleep(1/j)

    j+=d
    #print(i);
    if j<=1 :
        d = 1
        k = -k
    elif j>= 300 :
        d = -1

    if r >= mi :
        ri = -si
        gi = si
        g = gi
    elif r < si :
        ri = 0
    r += ri
    if g >= mi :
        gi = -si
        bi = si
        b = bi
    elif g < si :
        gi = 0
    g += gi
    if b >= mi :
        bi = -si
        ri = si
        r = ri
    elif b < si :
        bi = 0
    b += bi
