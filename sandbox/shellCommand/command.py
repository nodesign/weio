import sys
#import subprocess
sys.path.append('/home/drasko/nodesign/weio')

from weioLib import weioSubprocess


command = 'sh waitMe.sh'

def aashellBlocking(command) :
    output = "PLACEHOLDER"

    print(str(command))

    try :
        output = subprocess.check_output(command, shell=True)
    except :
        print("Comand ERROR : " + str(output) + " " + command)
        output = "ERR_CMD"
	
    print output
    return output


test = weioSubprocess.commandAsync(command)

print "AAA, ", test

print "OUT"
