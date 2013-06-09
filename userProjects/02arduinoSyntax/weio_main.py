# Example of Arduino pattern

# declaration of LED pin
LED_PIN = 13

# delay time in millis
time = 200

def setup() :
    
    # tells that on LED pin we want output
    pinMode(LED_PIN, OUTPUT) 
    
    # Attaches sensor function to infinite loop 
    attach.process(loop, ALWAYS)
    
    
def loop() :

    # Blinks LED once with given time interval
    digitalWrite(LED_PIN, HIGH)
    delay(time)
    digitalWrite(LED_PIN, LOW)
    delay(time)
        

runWeio()