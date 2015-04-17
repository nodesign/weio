###############################################
#                                             #
#   Playing MP3 audio stream using madplay    #
#                                             #
###############################################

# This example runs shell script that plays radio using
# wget (for streaming) thru PIPE and madplay

from weioLib.weio import *
from subprocess import Popen, PIPE
import signal, os

audioDevice = "/dev/audio"

# You need Internet mp3 stream link of your favorite radio
# Here is one example
url = "http://stream-uk1.radioparadise.com/mp3-128"

pid = None
def setup():
    global pid
    
    # check if soundcard is present
    if (os.path.exists(audioDevice)) :
        print "Sound card found \n"

        # play Internet radio sound 
        stream = Popen(["sh", "/weioUser/flash/playInternetRadio/streaming.txt", url], stdout=PIPE, stderr=PIPE)
        pid = stream.pid
    else :
        print "Soundcard is not connected or not recognized"

def stop(): 
    # If music is playing then kill process using it's PID
    print "stopping project"
    os.kill(pid, signal.SIGTERM)
    p = Popen(["killall", "madplay"], stdout=PIPE, stderr=PIPE)
    print p.communicate()[0]