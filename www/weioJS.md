Javascript
==========
Boilerplate
-----------
### HTML & JS boilerplate
This is html boilerplate for WeIO. WeIO needs weioApi library to work properly. 
Other dependencies are optional like p5js, jQuery, Chart and Bootstrap. 
```html
<!DOCTYPE html>
<html lang="en">

  <head >
    <!-- This is main weio api please call it always at first place -->
    <script src="www/libs/weio/weioApi.js"></script>
    <!-- This is p5 js - Processing for javascript library, desactivate if you d'ont need it -->
    <script src="www/libs/p5/p5.min.js"></script>

    <!-- Here you can add other local libraries -->
    <!-- <script src="www/libs/jquery/jquery-2.0.2.min.js"></script> -->
    <!-- <script src="www/libs/chartJS/Chart.min.js"></script> -->

    <!-- This is your processing p5 sketch -->
    <script src="sketch.js"></script>

    <title>My first Web app</title>

    <meta name="viewport" content="user-scalable=no,initial-scale=1,maximum-scale=1,minimum-scale=1,width=device-width">

  </head>

  <body>

  <script> 

    function onWeioReady() {
       console.log("DOM is loaded, websocket is opened");
    }

  </script>
  </body>
</html>
```
### onWeioReady()
This function is called when the DOM is fully loaded and websocket to WeIO is fully opened. Main difference between .ready() function from jQuery is that jQuery don't open websockets as they are not part of it's architecture. When using onWeioReady function, websocket communication with WeIO board is guaranteed, otherwise is not possible to send messages to the server before it fully opens it's websockets. It's recommended to use onWeioReady() as a replacement for .ready() from jQuery
```javascript
function onWeioReady() {
 console.log("DOM is loaded, websocket is opened");
}
```

Digital I/O
-----------
### digitalWrite(pin, value)
Sets voltage to +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground.
First add support for jQuery in index.html uncommenting this line inside head section
```html
<script src="www/libs/jquery/jquery-2.0.2.min.js"></script>
```
Continue to edit index.html by adding one button in the body section
```html
<button type="button" id="myButton">ON</button>
```
In Javascript we can bind one event to this button and then turn one pin HIGH or LOW. Pin 20 is connected to green LED on WeIO board. You will see green LED turning ON and OFF by clicking to button in your interface.
```javascript
// actual state of html button, true - ON, false - OFF
var buttonState = false;

function onWeioReady() {
  $( "#myButton" ).click(function() {
     if (buttonState) {
         digitalWrite(20,HIGH);
         $( "#myButton" ).html("ON");
     } else {
         digitalWrite(20,LOW);
         $( "#myButton" ).html("OFF");
     }
     buttonState = !buttonState;
    });
}
```

However you can make automatic blinking LED with calling setInterval JS function like this

```javascript
var led = false; // false LOW, true HIGH

function onWeioReady() {
  setInterval(function() {
    // Do something every half second
    if (led)
        digitalWrite(20,HIGH);
    else
        digitalWrite(20,LOW);
    // inverts variable state
    led = !led;
    }, 500);
}
```

### digitalRead(pin, callback)
Reads actual voltage on corresponding pin. WeIO inputs are 5V TOLERANT. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected. If only digitalRead function is provided, pin will be in HIGH Z state. See pinMode(pin,mode) function for more options.

In Javascript DigitalRead asks to provide callback function that will be called when WeIO board finish reading state on the pin. Callback function arguments will be populated with dictionary that provides pin number and pin state as information. This example with setInterval pooling is useful to check time to time pin state, if immediate reaction is needed than see attachInterrupt function.
```javascript
function onWeioReady() {
    console.log("hello");
    setInterval(function() {
    // Do something every 100ms
    //pinCallback will be called when data arrives from server
    digitalRead(0,pinCallback);
    }, 100);
}

function pinCallback(data) {
    $("#phrase").html("DigitalRead Value on the pin 0 is "+ data.data);
    $("body").css("background","white");
    $("#phrase").css("color","black");
}
```

### portWrite(port, value)
PortWrite allows faster manipulation of the i/o pins of the microcontroller. That means that you can send one byte of data that will be directly exported on 8 pins in form of HIGH and LOW signals instead sending them one by one. There are 4 available ports on the board. Port 0 for pins 0-7, Port 1 for pins 8-15, Port 2 for pins 16-23 and Port 3 for pins 24-31
This example will blink LEDs. There is only one instruction that is called instead calling digitalWrite for each pin separately 
```javascript
var led = false; // false LOW, true HIGH

function onWeioReady() {
  portMode(2, OUTPUT);
  setInterval(function() {
    // Blinks all 3 LEDs every half second
    if (led)
        portWrite(2, 227)
    else
        portWrite(2, 255)
    // inverts variable state
    led = !led;
    }, 500);
```

### portRead(port, callback)
PortRead allows faster manipulation of the i/o pins of the microcontroller. That means that you can read one byte of data instead reading them one by one using digitalRead function. There are 4 available ports on the board. Port 0 for pins 0-7, Port 1 for pins 8-15, Port 2 for pins 16-23 and Port 3 for pins 24-31
In Javascript portRead needs to be provided with callback function where results will be sent.
```javascript

function onWeioReady() {
    portMode(0, INPUT);
    console.log("DOM is loaded, websocket is opened");
    setInterval(function(){ portRead(0, read); }, 100);
}

function read(rcv) {
  //console.log(rcv.data);
  $("#portReadHtml").html(rcv.data);
}

```
### portMode(port, mode)
Sets states on one port (8 pins) at the same time. There are 4 available ports on the board. Port 0 for pins 0-7, Port 1 for pins 8-15, Port 2 for pins 16-23 and Port 3 for pins 24-31 Available modes are : PULL_UP, PULL_DOWN, INPUT and OUTPUT
This function activates pullups, pulldowns or high Z state (INPUT only) on declared ports. 

```javascript

function onWeioReady() {
    portMode(0, INPUT);
    console.log("DOM is loaded, websocket is opened");
    setInterval(function(){ portRead(0, read); }, 100);
}

function read(rcv) {
  //console.log(rcv.data);
  $("#portReadHtml").html(rcv.data);
}

```

### pinMode(pin, mode)

Sets state on the pin. Available modes are : PULL_UP, PULL_DOWN, INPUT and OUTPUT
This function activates pullups, pulldowns or high Z state (INPUT only) on declared pins. If pinMode function is not called and digitalRead is performed pin state will be in high Z by default

PinMode is available directly form JavaScript
```javascript
function onWeioReady() {
  // sets pulldown resistor on pin 13
  inputMode(13,INPUT_PULLDOWN);
  digitalRead(13, pinCallback);
}

function pinCallback(pinInput) {
    console.log("Pin number " + String(pinInput.pin) + " is in state " +  String(pinInput.data));
    if (pinInput.data===0) {
        $('body').css('background', 'black');
    } else {
        $('body').css('background', 'white');
    }
}
```

### pulseIn(pin, level, timeout, callback)
*pulseIn* reads a pulse (either HIGH or LOW) on a pin. For example, if value is HIGH, pulseIn() waits for the pin to go HIGH, starts timing, then waits for the pin to go LOW and stops timing. Returns the length of the pulse in microseconds or 0 if no complete pulse was received within the timeout.

Please also note that if the pin is already high when the function is called, it will wait for the pin to go LOW and then HIGH before it starts counting.

```javascript
var pin = 23;
var timeout = 500000;

function onWeioReady() {
	// Read a LOW pulse for 0.5s on pin 23 and call pulseInCallback
	var time = pulseIn(pin, LOW, timeout, pulseInCallback);
}

function pulseInCallback(callback) {
	// Print pulseIn duration
	console.log( "PulseIn duration = " + callback.data );
	// Read a LOW pulse for 0.5s on pin 23 and call pulseInCallback
	pulseIn(23, LOW, 500000, pulseInCallback);
}
```

Analog I/O
----------
### analogRead(pin, callback)
Reads input on specified Analog to Digital Convertor. 8 ADC are available on pins from 24 to 31. Output is 10bits resolution or expressed in decimal numbers from 0-1023.

AnalogRead asks to provide callback function that will be called when WeIO board finish reading state on the pin. Callback function arguments will be populated with dictionary that provides pin number and ADC value as information.
```javascript
function onWeioReady() {
 setInterval(function() {
    // Do something every 100ms
        //analogCallback will be called when data arrives from server
        analogRead(30, analogCallback);
    }, 100);

}

function analogCallback(pinInput) {
    console.log("Pin number " + String(pinInput.pin) + " ADC value " +  String(pinInput.data));
    if (pinInput.data > 512) {
        $('body').css('background', 'black');
    } else {
        $('body').css('background', 'white');
    }
}
```

### pwmWrite(pin, value)
Pulse with modulation is available at 6 pins from 18 to 23 and has 16bits of precision. By default WeIO sets PWM frequency at 1000us and it's value is expressed as percent of duty cycle from 0-100%. 
```javascript
var count = 0;
var mode = true; // fade in - true, fade out - false
function onWeioReady() {
  setInterval(function() {
    // Do something every 20ms
    fader();
    }, 20);
}

function fader() {
    if (mode) {
        if (count < 100) {
            count++;
        } else {
            mode = !mode;
        }
    } else {
        if (count > 0) {
            count--;
        } else {
            mode = !mode;
        }
    }
    pwmWrite(20,count);
}
```

### setPwmPeriod(period)
Overrides default value of 1000us to set new period frequency for whole 6 PWM pins.
```javascript
var count = 0;
var mode = true; // fade in - true, fade out - false

function onWeioReady() {
  setPwmPeriod(4000);
  setInterval(function() {
    // Do something every 20ms
    fader();
    }, 20);
}

function fader() {
    if (mode) {
        if (count < 255) {
            count++;
        } else {
            mode = !mode;
        }
    } else {
        if (count > 0) {
            count--;
        } else {
            mode = !mode;
        }
    }
    pwmWrite(20,count);
}
```

### startPackaging() and stopPackage()
Activate instruction buffering. In some cases it's more optimized to put a lot of instructions in one package and than send package. In that case for example instead sending 8 separate messages one packet will be send that contains 8 messages packed together. To start package buffering call startPackage() function. To send a package call sendPackage()
```javascript
startPackaging();
for (var j=0; j<7; j++) {
    if (id>=j) {
        digitalWrite(pins[j], HIGH);
    } else {
        digitalWrite(pins[j], LOW);
    }
}
sendPackage();
```

Interrupts
----
Interrupts allow to execute code when the state of an IO is changed without the need to continuously watch its state. WeIO allows upto eight, user defined, interrupts sources.
Interrupts can be trigged on levels (HIGH or LOW) or transitions (RISING, FALLING, CHANGE). 

### attachInterrupt(pin, mode, callback, obj)
*attachInterrupt* register and configure the interrupts. This function takes four parameters :
* pin : The pin number which will generate an interrupt
* mode : The mode : LOW; HIGH; CHANGE; RISING or FALLING
* callback : The callback function to execute when an interrupt occurs
* obj : A user defined object which will be passed to the callback function.

```javascript
var pin = 18;

function onWeioReady() {
	var obj = {pinNum:pin, mode:"RISING", callbackName:"interruptCallback"}; 
	attachInterrupt(pin,RISING,interruptCallback,obj);
}

function interruptCallback(data) {
    console.log( data.event + ", User object : " + data.obj );
}
```

### detachInterrupt(pin)
This function detach the interrupt on the specified *pin*.

```javascript
var pin = 18;

function onWeioReady() {
	var obj = { pinNum:pin, mode:"RISING", callbackName:"interruptCallback"}; 
	attachInterrupt(pin,RISING,interruptCallback,obj);
}

function interruptCallback(data) {
    console.log( data.event + ", User object : " + data.obj );
	detachInterrupt(pin);
    console.log( "and is now detached from pin" + String(pin) );
}
```

WeIO info
=========
### versionWeIO
Gets actual version of WeIO software

Interfaces
==========

Serial port
-----------
### listSerials()
List available serial ports on WeIO. By default there are 3 serial ports /dev/ttyACM1, /dev/ttyACM0, /dev/ttyATH0. Each of them has it's own function. ttyACM1 is WeIO serial port that is connected to pins 0-RX and 1-TX. ttyACM0 is reserved for communication with LPC processor and ttyATH0 is reserved for user console via micro USB (you should not touch these two ports).
WeIO has integrated drivers for the most common USB to serial devices so It's perfectly possible to connect some serial device over USB and communicate with it.

In Javascript call listSerials and provide callback function that will be called once data is ready and sent from the server.

```javascript
      function onWeioReady() {
       console.log("DOM is loaded, websocket is opened");
       listSerials(listPorts);
      }
      
      function listPorts(ports) {
          console.log(ports.data);
      }
```

Client-server I/O
-----------------
### getConnectedUsers(callback)
This function returns array of all connected users to the server. It's specially useful for communication between clients using WeIO as bridge. However as this function discovers some of client information user can ban it or overload it to specify output information from python code. If function is banned then message warning message is sent to console.log.

GetConnectedUsers asks to provide callback function that will be called once WeIO board sent client information. Callback function arguments will be populated with dictionary that provides client information. See example below for all possible keys. These information are got from JS navigator object from each client, keys uuid and ip are provided by server and added to the dictionary.
```javascript
function onWeioReady() {
  $( "#myButton" ).click(function() {
     getConnectedUsers(printUsers);
    });
}

function printUsers(data) {
    var connections = data.data;
    for (var i in connections) {
        var connection = connections[i];
        console.log("");
        console.log("Client appCodeName ",  connection.appCodeName);
        console.log("Client appName ",      connection.appName);
        console.log("Client appVersion ",   connection.appVersion);
        console.log("Client cookieEnabled ",connection.cookieEnabled);
        console.log("Client ip ",           connection.ip);
        console.log("Client onLine ",       connection.onLine);
        console.log("Client platform ",     connection.platform);
        console.log("Client userAgent ",    connection.userAgent);
        console.log("Client uuid ",         connection.uuid);
    }
}
```
### getMyUuid()
Gets unique uuid number generated for this connection. This number is used by server to identify each client and can be used to address other clients that are connected. See getConnectedUsers for example.

GetMyUuid can be called once WeIO is ready for communication.
```javascript
function onWeioReady() {
  console.log(getMyUuid());
}
```
### talkTo(uuid, data)
TalkTo delivers json object to connected client with specific uuid. In this example message is sent to itself.
```javascript
function onWeioReady() {
    var myName = getMyUuid();
    data = {};
    data.info = "hello to myself";
    talkTo(myName, data);
}

function onReceiveMessage(data) {
    console.log("Received from ", data.from);
    console.log("Contents ", data.data);
}
```

### onReceiveMessage(data)
onReceiveMessage is callback function that will be called when some client sends message to actual uuid. This function works in pair with talkTo. onReceiveMessage is receiving callback and talkTo sender function. In this example message is sent to itself.
```javascript
function onWeioReady() {
    var myName = getMyUuid();
    data = {};
    data.info = "hello to myself";
    talkTo(myName, data);
}

function onReceiveMessage(data) {
    console.log("Received from ", data.from);
    console.log("Contents ", data.data);
}
```

### genericMessage(eventName, data)
This function is the WeIO Remote Procedure Call, is used to send messages from JavaScript to Python. To use it you need to previously define in python side which function call when corresponding message is received with **attach.event()** function.
<br></br>
When you send a genericMessage Tornado server gets this message from WebSocket that is constantly open between frontend (browser) and backend (Tornado server), decodes it, sees function name "eventName", gets "data" and calls function that you have previously defined in python.


```python
def setup():
    attach.event("msgFromJStoPy", myFunction)

def myFunction(data):
	if(data == 1):
    	digitalWrite(18,HIGH)
```

```javascript
function pushButton() {
	genericMessage("msgFromJStoPy", 1);
}
```