/**
*
* WEIO Web Of Things Platform
* Copyright (C) 2013 Nodesign.net, Uros PETREVSKI, Drasko DRASKOVIC
* All rights reserved
*
*               ##      ## ######## ####  #######  
*               ##  ##  ## ##        ##  ##     ## 
*               ##  ##  ## ##        ##  ##     ## 
*               ##  ##  ## ######    ##  ##     ## 
*               ##  ##  ## ##        ##  ##     ## 
*               ##  ##  ## ##        ##  ##     ## 
*                ###  ###  ######## ####  #######
*
*                    Web Of Things Platform
*
* WEIO is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* WEIO is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
* This file is part of WEIO.
*
* Authors :
* Uros PETREVSKI <uros@nodesign.net>
* Drasko DRASKOVIC <drasko.draskovic@gmail.com>
*
**/

/*
 * WeIO websocket object
 */
var _weio = null;

//CALLBACKS//////////////////////////////////////////////////////////////////////////////////////////////////////// 
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var weioCallbacks = {
    "inbox":callInbox,
    "attachInterrupt":weioExecuteInterrupt
};

/**
 * This is where callback names are stored behind pin numbers
*/
var weioInterrupts = [];

$(document).ready(function() {

    // Change this port when running on PC
    var port = "8082";
    $.getJSON('www/config.json', function(data) {
        confFile = data;
        port = confFile.userAppPort;

        /**
         * N.B. All the handling using the port must go inside .getJSON(),
         * otherwise Javascript handles things in parallel, while (and before) getting the JSON,
         * using undefined values for port
         */
        /*
         * Identify server address and port to open websocket
         */
        var _addr = location.host;
        if (location.port == "8080") {
            var a = _addr.split(":");
            _addr = 'http://' + a[0] + ':' + port + '/api';
        } else {
            var a = 'http://' + _addr + '/api';
            _addr = a;
        }
        console.log("WebSocket connecting to " + _addr);
        
        // init interrupts
        for (var i=0; i<32; i++) {
            weioInterrupts.push("");
        }

        /*
        * WebSocket openning
        */
                    
        (function() {
        // Initialize the socket & handlers
        var connectToServer = function() {
            _weio = new SockJS(_addr);
        
            _weio.onopen = function() {
            //clearInterval(connectRetry);
            console.log('socket opened for weio API');
                
            // Client info will be sent to server
            data = {};
            data.appCodeName = navigator.appCodeName;
            data.appName = navigator.appName;
            data.appVersion = navigator.appVersion;
            data.cookieEnabled = navigator.cookieEnabled;
            data.onLine = navigator.onLine;
            data.platform = navigator.platform;
            data.userAgent = navigator.userAgent;
                
            uuid = _generateUUID()
            data.uuid = uuid;
                
            // Say hello to server with some client data
            var rq = { "request": "_info", "data":data};
            _weio.send(JSON.stringify(rq));
                
            if(typeof onWeioReady == 'function'){
                onWeioReady();
            }
        
            };
        
            _weio.onmessage = function(e) {
                // JSON data is parsed into object
                data = JSON.parse(e.data);
                console.log(data);
                
                if ("requested" in data) {
                    // this is instruction that was echoed from server + data as response
                    instruction = data.requested;  
                    if (instruction in weioCallbacks) 
                        weioCallbacks[instruction](data);
                } else if ("serverPush" in data) {
                    // this is instruction that was echoed from server + data as response

                    instruction = data.serverPush;  
                    if (instruction in weioCallbacks) 
                        weioCallbacks[instruction](data.data);

                }
            };
        
            _weio.onclose = function() {
            //clearInterval(connectRetry);
            //connectRetry = setInterval(connectToServer, 500);
            console.log('socket is closed or not opened for weioApi');
        
            };
        
        };
        //var connectRetry = setInterval(connectToServer, 500);
        connectToServer();
        })();
               
    }); /* getJSON */
}); /* document.ready() */


/* 
 * GLOBALS
 */
// GPIO directions


// GPIO directions
var INPUT = 0
var OUTPUT = 1

// GPIO resistors
var NONE = 2
var PULL_UP = 3
var PULL_DOWN = 4

// GPIO events
var LOW = 0
var HIGH = 1
var CHANGE = 2
var RISE = 3
var FALL = 4

/*
 * Unique UUID number of this session
 * Will be generated on oppening of websocket and will be sent with
 * every message to server 
 */
var uuid = null;

function getMyUuid() {
    return uuid;
};

/* 
 * Generate unique UUID number, uuid4 conforms to standard
 */
function _generateUUID(){
    var d = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x7|0x8)).toString(16);
    });
    return uuid;
};



function isWeioReady() {
    if (_weio!=null)
        return _weio.readyState;
    else
        return false;
};

/* 
 * Low level electronics instructions from JS
 */
function pinMode(pin, mode) {
    genericMessage("pinMode", [pin,mode], null);
};

function digitalWrite(pin, value) {
	genericMessage("digitalWrite", [pin,value], null);
};

function digitalRead(pin, callback) {
    // create new callback call
    var fName = callback.name;
    //console.log("callback name:" + fName);
    weioCallbacks[fName] = callback
    genericMessage("digitalRead", [pin],fName);
};

function portWrite(port, value) {
    genericMessage("portWrite", [port, value], null);
};

function portRead(port, callback) {
    // create new callback call
    var fName = callback.name;
    //console.log("callback name:" + fName);
    weioCallbacks[fName] = callback
    genericMessage("portRead", [port],fName);
};

function portMode(port, value) {
    genericMessage("portMode", [port, value], null);
};

function dhtRead(pin, callback) {
    var fName = callback.name;
    weioCallbacks[fName] = callback
    genericMessage("dhtRead", [pin], fname);
};

function analogRead(pin, callback) { 
    // create new callback call
    var fName = callback.name;
    //console.log("callback name:" + fName);
    // add callback function to be called when data arrives
    weioCallbacks[fName] = callback
    genericMessage("analogRead", [pin], fName);
    //console.log("Callbacks", weioCallbacks);
};

function setPwmPeriod(pin, period){
    genericMessage("setPwmPeriod", [pin,period], null);
};

function setPwmLimit(limit){
    genericMessage("setPwmLimit", [limit], null);
};

function pwmWrite(pin, value) {
    genericMessage("pwmWrite", [pin,value], null);
};

function analogWrite(pin, value) {
    genericMessage("pwmWrite", [pin,value], null);
};

function proportion(value, istart, istop, ostart, ostop){
    return ostart + (ostop-ostart) * ((value -istart) / (istop - istart))
    
};

function delay(period){
	genericMessage("delay",[period], null);
};

function tone(pin, frequency, duration) {
    if(typeof duration !== "undefined"){
    	genericMessage("tone", [pin,frequency,duration], null);
    }
	else{
		genericMessage("tone", [pin,frequency], null);
	}
};

function notone(pin) {
	genericMessage("notone", [pin], null);
};

function constrain(x, a, b) {
    if(x > a){
        if(x < b){
            return a
		}
	}
    if(x < a){
        return a
	}
    if(x > b){
        return b
	}
};

function millis(callback) {
    console.log("millis");
 	var fName = callback.name;
	weioCallbacks[fName] = callback
	genericMessage("millis", fName);
};

function getTemperature(callback) {
     console.log("temperature");
	 var fName = callback.name;
	 weioCallbacks[fName] = callback;
	 genericMessage("getTemperature", null, fName);
		
};

function getConnectedUsers(callback) {
    // create new callback call
    var fName = callback.name;
    //console.log("callback name:" + fName);
    weioCallbacks[fName] = callback
    genericMessage("getConnectedUsers", null, fName);
    //console.log("Callbacks", weioCallbacks);
};

function talkTo(uuid, data){
    genericMessage("talkTo", [uuid, data], null);
};

function callInbox(data) {
    if(typeof onReceiveMessage == 'function'){
        onReceiveMessage(data.data);
    }
};

function attachInterrupt(pin, mode, callback) {
    var fName = callback.name;
    weioInterrupts[pin] = fName;
    weioCallbacks[fName] = callback;
    genericMessage("attachInterrupt", [pin, mode], null);
}

function weioExecuteInterrupt(data) {
    console.log("INTERRUPR",data);
}

function detachInterrupt(pin) {
    delete weioCallbacks[weioInterrupts[pin]];
    weioInterrupts[pin] = "";
    genericMessage("detachInterrupt", [pin], null);
}

/*
 * Generic handler for sending messages to server
 */
function genericMessage(instruction, data, clbck) {
    // avoid sending messages to websocket that is not yet opened
    if (isWeioReady() != 0) {
        var askWeio;
        
        if (clbck == null)
             askWeio = { "request": instruction, "data" : data }; //, "uuid" : uuid };
         else 
             askWeio = { "request": instruction, "data" : data, "callback": clbck }; //, "uuid" : uuid };
         
        _weio.send(JSON.stringify(askWeio));
    } else {
        console.log("Warning, message tried to be sent when websocket was not completely opened");
    }
};
