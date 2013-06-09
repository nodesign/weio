# Push every 2 seconds data to WEB
# in meanwhile calculate average value 
# from sensor

SENSOR_PIN = A0

PUSH_WEB = "fromSensor"

def setup() :
    # execute function every 2 seconds
    attach.process(loop, 2000)

def loop():
    
    val = 0
    for a in range(10) :
        val+=analogRead(A0)
        delay(20)
        
    # push message to web if JSON format
    # "fromSensor" : 2.33
    webWrite(PUSH_WEB, val/10.0)
    
runWeio()