# Example of button interrupt

BUTTON_PIN = 0

def setup() :
    
    # tells that button is on pin 1
    pinMode(BUTTON_PIN, INPUT) 
    
    # tells that on LED pin we want output
    pinMode(LED_PIN, OUTPUT) 

    # Attaches sensor function to infinite loop 
    attach.process(loop, ALWAYS)
   

def loop(): 
    
    val = digitalRead(BUTTON_PIN)
    
    if (val==HIGH) :
        print "button pressed"

runWeio()