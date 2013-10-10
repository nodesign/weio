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
var _weio;


//CALLBACKS//////////////////////////////////////////////////////////////////////////////////////////////////////// 
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var weioCallbacks = {};
var _addr;

$(document).ready(function() {

    /*
     * Identify server address and port to open websocket
     */
    _addr = location.host;
    if (_addr.indexOf(":")!=-1) {
        var a = _addr.split(":");
        _addr = 'http://' + a[0] + ':8082/api';
    } else {
        var a = 'http://' + _addr + ':8082/api';
        _addr = a;
    }
    console.log("WebSocket connecting to " + _addr);

    /*
     * WebSocket openning
     */
    _weio = new SockJS(_addr);

    _weio.onopen = function() {
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
                weioCallbacks[instruction](data);
            
        }

    };

    _weio.onclose = function() {
      console.log('socket is closed for editor');
    };

});



/* 
 * GLOBALS
 */
var HIGH = 1;
var LOW = 0;

/*
 * Unique UUID number of this session
 * Will be generated on oppening of websocket and will be sent with
 * every message to server 
 */
var uuid;

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
}



function isWeioReady() {
    return _weio.readyState;
}

/* 
 * Low level electronics instructions from JS
 */
function digitalWrite(pin, value) {
  genericMessage("digitalWrite", [pin,value]);
};

function pinMode(pin, mode) {
  genericMessage("pinMode", [pin,mode]);
};

function analogRead(pin, callback) { 
    // create new callback call
    var fName = callback.name;
    //console.log("callback name:" + fName);
    weioCallbacks[fName] = callback
    genericMessage("analogRead", [pin,fName]);
    //console.log("Callbacks", weioCallbacks);
};


/*
 * Generic handler for sending messages to server
 */
function genericMessage(instruction, data) {
    // avoid sending messages to websocket that is not yet opened
    if (isWeioReady() != 0) {
        var askWeio = { "request": instruction, "data" : data, "uuid" : uuid };
        _weio.send(JSON.stringify(askWeio));
    } else {
        console.log("Warning, message tried to be sent when websocket was not completely opened");
    }
}

