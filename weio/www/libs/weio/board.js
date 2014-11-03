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
