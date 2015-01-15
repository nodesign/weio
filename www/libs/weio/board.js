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
* This file is part of WEIO and is published under BSD license.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
* 1. Redistributions of source code must retain the above copyright
*    notice, this list of conditions and the following disclaimer.
* 2. Redistributions in binary form must reproduce the above copyright
*    notice, this list of conditions and the following disclaimer in the
*    documentation and/or other materials provided with the distribution.
* 3. All advertising materials mentioning features or use of this software
*    must display the following acknowledgement:
*    This product includes software developed by the WeIO project.
* 4. Neither the name WeIO nor the
*    names of its contributors may be used to endorse or promote products
*    derived from this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY WEIO PROJECT AUTHORS AND CONTRIBUTORS ''AS IS'' AND ANY
* EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL WEIO PROJECT AUTHORS AND CONTRIBUTORS BE LIABLE FOR ANY
* DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*
* Authors : 
* Uros PETREVSKI <uros@nodesign.net>
* Drasko DRASKOVIC <drasko.draskovic@gmail.com>
*
**/

var boardSocket;
var socketOpened = false;



function connectToBoard() {
    // connection example
     //   dashboard = new SockJS('http://' + location.host + '/dashboard');

     console.log("Opening board");
    if (socketOpened==false) {

        /*
         * Identify server address and port to open websocket
         */
        var port = "8082";
        $.getJSON('config.json', function(data) {
            var getInfoFromBoard;
            confFile = data;
            port = confFile.userAppPort;

            var _addr = location.host;
            if (location.port == "8080") {
                var a = _addr.split(":");
                _addr = 'http://' + a[0] + ':' + port + '/api';
            } else {
                var a = 'http://' + _addr + '/api';
                _addr = a;
            }

            /*
             * WebSocket openning
             */

            //boardSocket = new WebSocket(_addr);
            boardSocket = new SockJS(_addr);

            //////////////////////////////////////////////////////////////// BOARD JS STATS

            /*
             * On opening of wifi web socket ask server to scan wifi networks
             */
            boardSocket.onopen = function() {
                console.log('Board Web socket is opened');
                socketOpened = true;
                getInfoFromBoard = setInterval(getInfo, 500);
            };
            
            function getInfo(){
                console.log("GETTING BOARD INFO");
                var rq = { "request": "pinsInfo", "data":"", "callback":"pinsInfo"};
                boardSocket.send(JSON.stringify(rq));
            }

            /*
             * Dashboard parser, what we got from server
             */
            boardSocket.onmessage = function(e) {
                //console.log('Received: ' + e.data);

                // JSON data is parsed into object
                data = JSON.parse(e.data);
                console.log(data);

                // switch
                if ("requested" in data) {
                    // this is instruction that was echoed from server + data as response
                    instruction = data.requested;
                    if (instruction in callbacksBoard)
                        callbacksBoard[instruction](data);
                } else if ("serverPush" in data) {
                    // this is instruction that was echoed from server + data as response
                    instruction = data.serverPush;
                    if (instruction in callbacksBoard)
                        callbacksBoard[instruction](data);
                }
            };

            boardSocket.onclose = function() {
                console.log('Board Web socket is closed');
                socketOpened = false;
                clearInterval(getInfoFromBoard);
            };


        });

    } else {
        var rq = { "request": "pinsInfo", "data":"","callback":"pinsInfo"};
        boardSocket.send(JSON.stringify(rq));
    }

}

function boardData(data) {
    console.log("DATA BOARD ", data.data);

    for (var i=0; i<32; i++) {
     if (data.data.data[i] != -1 ) {
         $("#pin"+String(i)).attr("class", "pin_on");
     } else {
         $("#pin"+String(i)).attr("class", "pin");
        }
    }

}

//CALLBACKS////////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var callbacksBoard = {
    "pinsInfo": boardData
}
