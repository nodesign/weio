#######################################
#                                     #
#   Playing Starwars theme on WeIO    #
#                                     #
#######################################

from weioLib.weio import *

pin = 23

z = 0
c = 261.0
d = 294.0
e = 329.0
f = 349.0
g = 391.0
gS = 415.0
a = 440.0
aS = 455.0
b = 466.0
cH = 523.0
cSH = 554.0
dH = 587.0
dSH = 622.0
eH = 659.0
fH = 698.0
fSH = 740.0
gH = 784.0
gSH = 830.0
aH = 880.0


def setup():
    attach.process(myProcess)
    
def myProcess():
    print("StarWars")
    while True :
        play(melody1)
        play(melody2)
        play(melody3)
        play(melody2)
        play(melody4)
        
def play(song):
    for note in song:
        tone(pin, note["note"], note["duration"])

melody1 = [
    {"note": a, "duration":500},
    {"note": a, "duration":500},
    {"note": a, "duration":500},
    {"note": f, "duration":350},
    {"note": cH, "duration":150},
    {"note": a, "duration":500},
    {"note": f, "duration":350},
    {"note": cH, "duration":150},
    {"note": a, "duration":650},
    {"note": z, "duration":500},
    {"note": eH, "duration":500},
    {"note": eH, "duration":500},
    {"note": eH, "duration":500},
    {"note": fH, "duration":350},
    {"note": cH, "duration":150},
    {"note": gS, "duration":500},
    {"note": f, "duration":350},
    {"note": cH, "duration":150},
    {"note": a, "duration":650},
    {"note": z, "duration":500},   
]
melody2 = [
    {"note": aH, "duration":500},
    {"note": a, "duration":300},
    {"note": a, "duration":150},
    {"note": aH, "duration":500},
    {"note": gSH, "duration":325},
    {"note": gH, "duration":175},
    {"note": fSH, "duration":125},
    {"note": fH, "duration":125},
    {"note": fSH, "duration":250},
    {"note": z, "duration":325},
    {"note": aS, "duration":250},
    {"note": dSH, "duration":500},
    {"note": dH, "duration":325},
    {"note": cSH, "duration":175},
    {"note": cH, "duration":125},
    {"note": b, "duration":125},
    {"note": cH, "duration":250},
    {"note": z, "duration":350},   
]
melody3 = [
    {"note": f, "duration":250},
    {"note": gS, "duration":500},
    {"note": f, "duration":350},
    {"note": a, "duration":125},
    {"note": cH, "duration":500},
    {"note": a, "duration":375},
    {"note": cH, "duration":125},
    {"note": eH, "duration":650}, 
    {"note": z, "duration":500},   
]
melody4 = [
    {"note": f, "duration":250},
    {"note": gS, "duration":500},
    {"note": f, "duration":375},
    {"note": cH, "duration":125},
    {"note": a, "duration":500},
    {"note": f, "duration":375},
    {"note": cH, "duration":125},
    {"note": a, "duration":650}, 
    {"note": z, "duration":650},   
]


