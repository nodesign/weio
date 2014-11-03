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

 /**
* Wifi SockJS object, Web socket for scaning and changing wifi parameters */


$(document).ready(function () {

    $.getJSON('config.json', function(data) {
            confFile = data;

/////////////////////////////// SOCK JS SETTINGS  /////////////////////

            var http_prefix = "http://";

            if (confFile.https == "YES") {
                http_prefix = "https://";
            }
            else {
                http_prefix = "http://";
            }
    
    settingsSocket = new SockJS(http_prefix + location.host + '/settings');
 

    settingsSocket.onopen = function() {
        console.log("settingsSocket is opened")
    }

    settingsSocket.onmessage = function(e) {
        data = JSON.parse(e.data);
        console.log(data + " " + "OVDEEEEEEEEEEE");
    }
});

/* Save new user data */
function updateUserData() {

};

