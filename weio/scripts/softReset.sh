#!/bin/sh
while true;
do
# key pressed, blocking
read input </dev/input/event0
# key released, blocking
read input </dev/input/event0

if [ -n "$(ps | grep  "[w]eioServer.py")" ]; then
	echo "Stopping python server.py..."
	killall weioServer.py
fi

if [ -n "$(ps | grep  "[w]eioRunner.py")" ]; then
    echo "Stopping user program weioRunner.py..."
    killall weioRunner.py
fi

done
