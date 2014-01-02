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


$( document ).ready(function() {
    
    // Get country list
    $.getJSON('countries.json', function(data) {
            var confFile = data;
            //console.log(confFile[0][1]);
            
            $("#countries").empty();
            for (var i=0; i<confFile.length; i++) {
                $("#countries").append('<option value="'+confFile[i][1]+'">'+confFile[i][0]+'</option>');
            }
            
    });
});


/**
 * Wifi SockJS object, Web socket for scaning and changing wifi parameters
 */
var fistTimeSocket = new SockJS('http://' + location.host + '/firstTime');

function sendData() {
    
    var rq = { "request": "runWeio", 
               "fullName":$("#fullName").val(),
               "password1":$("#password1").val(),
               "password2":$("#password2").val(),
               "dnsName": $("#dnsName").val(),
               "countryCode": $("#countries").val()
    };
    fistTimeSocket.send(JSON.stringify(rq));
}


//CALLBACKS////////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var callbacksFt = {
    "error": showError,
    "runWeio": runWeio,
    "getBasicInfo": updateInfo,
    
};

function showError(data) { 
    $("#error").html(data.data);
};

function runWeio(data) {
    location.reload();
};


function updateInfo(data) {
    
    $("#dnsName").attr("placeholder", data.dnsName);
    $("#ip").html(" on " + data.ip);
    $("#dnsName1").html(data.dnsName);
    
    $("#dnsName").attr("value", data.dnsName);
    
};

//////////////////////////////////////////////////////////////////////////////////////////////////// SOCK JS WIFI        
    
/*
* On opening of ft web socket
*/
fistTimeSocket.onopen = function() {
    console.log('FT Web socket is opened');
    var rq = { "request": "getBasicInfo"};
    fistTimeSocket.send(JSON.stringify(rq));
    
   
};

/*
* Ft web socket parser, what we got from server
*/
fistTimeSocket.onmessage = function(e) {
    //console.log('Received: ' + e.data);

    // JSON data is parsed into object
    data = JSON.parse(e.data);
    console.log(data);

    if ("requested" in data) {
          // this is instruction that was echoed from server + data as response
          instruction = data.requested;  
            
          if (instruction in callbacksFt) 
              callbacksFt[instruction](data);
      } else if ("serverPush" in data) {
             // this is instruction that was echoed from server + data as response
             
             instruction = data.serverPush;  
             if (instruction in callbacksFt) 
                 callbacksFt[instruction](data);
      }
};

fistTimeSocket.onclose = function() {
    console.log('FT Web socket is closed');
};
