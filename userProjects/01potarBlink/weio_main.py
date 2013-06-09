# Simple standalone application, no web interface
# Reads digital potentiometer from A0 pin to blink LED slower or faster at digital pin 13

LED_PIN = 13
POTENTIOMETER_PIN = A0


def setup() :
    
    # tells that on LED pin we want output
    pinMode(LED_PIN, OUTPUT) 
    
    # Attaches sensor function to infinite loop 
    attach.process(blinky, ALWAYS)
    
    # Attaches sensor function to infinite loop 
    attach.process(potentiometer, ALWAYS)
    
    
def potentiometer() :
    val = analogRead(POTENTIOMETER_PIN)
    # map values between 0-1023 to time intervals 50 millis - 1000 millis
    val = map(val, 0,1023, 50,1000)
    
    # tells to blinky process to change parameters
    process.blinky(val)
    
    

def blinky(time) :
    # Blinks LED once with given time interval
    digitalWrite(LED_PIN, HIGH)
    delay(time)
    digitalWrite(LED_PIN, LOW)
    delay(time)
        
        
        

runWeio()