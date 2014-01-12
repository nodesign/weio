from weioLib.weioUserApi import attach, shared
import os, time
from subprocess import Popen, PIPE

videoDevice = "/dev/video0"
imageFile = "output.jpg"
imagePath = "./"

# easy with this, processor needs more time processing for better resolution
resolution = "320x240"

def setup():
    
    # check if webcam is connected
    if (os.path.exists(videoDevice)) :
        attach.process(takePicture)
    else :
        print "webcam is not connected or not recognized"
    
def takePicture():
    while True:
        # Use PIPES when calling external processes, otherwise is pretty dangerous, can block app
        proc = Popen(["fswebcam", "d", videoDevice, "--no-banner", "-r", resolution, imagePath+imageFile], stdout=PIPE, stderr=PIPE)
        proc.communicate()
        print "Photo Taken"
        
        # Tell to all connected clients that they can refresh image in browsers now
        for client in shared.connectedClients :
           client.connection.emit("refreshImage",imageFile)
        
        # give peace a chance
        #time.sleep(1)