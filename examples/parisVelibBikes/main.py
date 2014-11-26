################################################################################################
#                                                                                              #
#   Check if Parisian Velib bikes are avaibile and blink a LED                                 #
#                                                                                              #
#   Made by Uros Petrevski, many thanks to Aurelien Fache for his WeIO project that            #
#   I was inspired :                                                                           # 
#   http://www.makery.info/2014/11/11/on-a-proto-teste-weio-larduino-des-designers-connectes/  #
#                                                                                              #
################################################################################################

from weioLib.weio import *
import urllib2, json

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("Hello Velib Paris!")
    
    # to find your bike station number : https://developer.jcdecaux.com/#/opendata/vls?page=static
    city = "paris"
    velibStation = "10025"
    # to get your own api key : https://developer.jcdecaux.com
    apiKey = "xxx"
    
    while True :
        url = "https://api.jcdecaux.com/vls/v1/stations/"+velibStation+"?contract="+city+"&apiKey="+apiKey
        
        print "Checking station"
        # Opening URL and getting data
        data = urllib2.urlopen(url).read()
        velib = json.loads(data)
        
        # get some basic info from this station
        print "station", velib["name"]
        print "available places", velib["available_bike_stands"]
        print "available bikes", velib["available_bikes"]
        
        ledPinOK = 19 # green
        ledPinNo = 18 # red
        
        # if no bikes available turn ON red LED for 2sec
        if (velib["available_bikes"]==0):
            digitalWrite(ledPinNo,LOW)
            delay(2000)
        else :
            # if bikes available blink number of times that express number of available bikes
            for i in range(velib["available_bikes"]):
                digitalWrite(ledPinOK,LOW)
                delay(200)
                digitalWrite(ledPinOK,HIGH)
                delay(200)
                
        # Give peace a chance! Check for available bikes every 5 sec    
        delay(5000)