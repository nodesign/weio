# Running RGB LED from browser

LED_R_PIN = 0
LED_G_PIN = 1
LED_B_PIN = 2

COLOR_WEB = "rgb"


def setup() :
    
    # Attaches interrupt from Web client
    attach.interrupt(COLOR_WEB, onColor)
    


def onColor(rgb): 
    
    r = int(rgb["red"])
    g = int(rgb["green"])
    b = int(rgb["blue"])
    
    pwmWrite(LED_R_PIN, r)
    pwmWrite(LED_G_PIN, g)
    pwmWrite(LED_B_PIN, b)
    

runWeio()