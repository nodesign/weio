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


  var weio = new SockJS('http://' + location.hostname + ':8082/api');

  var HIGH = "1";
  var LOW = "0";
  var OUTPUT = "out";
  var INPUT = "in";

  weio.onopen = function() {
      console.log('socket opened for weio API');

  };

  weio.onmessage = function(e) {
      data = JSON.parse(e.data);

  };

  weio.onclose = function() {
      console.log('socket is closed for editor');

  };


  function digitalWrite(pin, value) {
      genericMessage("digitalWrite", [pin,value]);
            //
            // var askWeio = { "request": "digitalWrite", "data" : [pin,value] };
            // //   console.log(askWeio);
            // weio.send(JSON.stringify(askWeio));
  };

  function pinMode(pin, mode) {

      genericMessage("pinMode", [pin,mode]);

      // var askWeio = { "request": "pinMode", "data" : [pin,mode] };
      //       weio.send(JSON.stringify(askWeio));
  };

  function genericMessage(instruction, data) {
    var askWeio = { "request": instruction, "data" : data };
    weio.send(JSON.stringify(askWeio));
  }

