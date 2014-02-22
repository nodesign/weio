from weioLib.weioUserApi import attach
from subprocess import Popen, PIPE
import os

videoDevice = "/dev/video0"
   
def setup():
    
     # check if webcam is connected
    if (os.path.exists(videoDevice)) :
        # if any mjpegstreamer is already running, kill it
        proc = Popen(["killall", "mjpg_streamer"], stdout=PIPE, stderr=PIPE)
        proc.communicate()
        attach.process(startVideoStreaming)
    else :
        print "webcam is not connected or not recognized"

def startVideoStreaming():
    print("Starting video stream server on 8080 port")
    
    i = '"/usr/lib/input_uvc.so -d /dev/video0 -y -r 320x240 -f 25"'
    o = "'/usr/lib/output_http.so -w /www/webcam -p 8080'"
    proc = Popen(["mjpg_streamer", "-i", i, "-o", o], stdout=PIPE, stderr=PIPE)
    print proc.communicate()