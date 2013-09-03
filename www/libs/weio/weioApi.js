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


var _weio;
var addr = location.host;
if (addr.indexOf(":")!=-1) {
    var a = addr.split(":");
    addr = 'http://' + a[0] + ':8082/api';
} else {
    var a = 'http://' + addr + ':8082/api';
    addr = a;
}
console.log(addr);
_weio = new SockJS(addr);

var HIGH = "1";
var LOW = "0";
var OUTPUT = "out";
var INPUT = "in";

_weio.onopen = function() {
  console.log('socket opened for weio API');
};





//CALLBACKS////////////////////////////////////////////////////////////////////////////////////////////////////////x  
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var callbacks = {}

_weio.onmessage = function(e) {
    // JSON data is parsed into object
    data = JSON.parse(e.data);
    console.log(data);
    
    if ("requested" in data) {
        // this is instruction that was echoed from server + data as response
        instruction = data.requested;  
        if (instruction in callbacks) 
            callbacks[instruction](data);
    } else if ("serverPush" in data) {
        // this is instruction that was echoed from server + data as response
        
        instruction = data.serverPush;  
        if (instruction in callbacks) 
            callbacks[instruction](data);
        
    }

};

_weio.onclose = function() {
  console.log('socket is closed for editor');
};

function digitalWrite(pin, value) {
  genericMessage("digitalWrite", [pin,value]);
};

function pinMode(pin, mode) {
  genericMessage("pinMode", [pin,mode]);
};

function genericMessage(instruction, data) {
    var askWeio = { "request": instruction, "data" : data };
    _weio.send(JSON.stringify(askWeio));
}

