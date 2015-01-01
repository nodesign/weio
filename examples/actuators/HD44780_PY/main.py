#############################################
#                                           #
#           HD44780, LCD display            #
#                                           #
#############################################

# Example presents communication with HD44780 LCD displays
# This library use a complete port to work.
# Connection must be :
# bit 0 : D4 (LCD pin 11)
# bit 1 : D5 (LCD pin 12)
# bit 2 : D6 (LCD pin 13)
# bit 3 : D7 (LCD pin 14)
# bit 4 : Not used
# bit 5 : Enable (LCD pin 6)
# bit 6 : RS (Register select) (LCD pin 4)

# LCD pin 1, 3, 5 and 16 must be connected to GND
# LCD pin 2 must be connected to +5V
# LCD pin 15 must be connected to +5V through a 220R resistor
# LCD pins 7 to 10 must not be connected

from weioLib.weio import *
from things.output.display.hd44780 import Hd44780

def setup():
    attach.process(myProcess)
    
def myProcess():
    lcd = Hd44780(1)
    lcd.selectLine(lcd.LINE1)
    lcd.writeString("      WeIO      ")
    lcd.selectLine(lcd.LINE2)
    lcd.writeString("  HD44780 demo  ")