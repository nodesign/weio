#######################################
#                                     #
#   Playing Wave audio using aplay    #
#                                     #
#######################################

# Python script will call aplay to play wave sample file
# You need to plug sound card dongle into USB to make this example work

from weioLib.weio import *
from subprocess import Popen, PIPE
import signal, os

audioDevice = "/dev/audio"

# You need some wav file to play it. If you don't have it, this sample will download one simple
# from here (make sure that you are connected to the Internet) :
# http://www.jahozafat.com/0053148414/WAVS/Movies/Star_Wars/starwars.wav

audioFile = "/tmp/starwars.wav"
pid = None

def setup():
    # check if soundcard is present
    if (os.path.exists(audioDevice)) :
        print "Sound card found \n"
        print execute(["amixer"])
        
        if not(os.path.exists(audioFile)) :
            url = "http://www.jahozafat.com/0053148414/WAVS/Movies/Star_Wars/starwars.wav"
            execute(["wget", "-P", "/tmp/", "-q", url])
            print "downloaded file \n"
        
        # set volume to 20%
        volume = 20
        print execute(["amixer", "set", "Headphone", str(volume)])
        
        # play sound 
        print execute(["aplay", audioFile])

    else :
        print "Soundcard is not connected or not recognized"


def execute(cmd): # cmd has to be an array
    global pid
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    # Get system PID of current process
    pid = proc.pid
    s = proc.communicate()
    # return console output
    return s[0]

def stop(): 
    # If music is playing then kill process using it's PID
    print "stopping project"
    os.kill(pid, signal.SIGTERM)