import sys
import weioCommand
#import subprocess
sys.path.append('./')

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


test = weioCommand.shellAsync(command)

print test

print "OUT"
