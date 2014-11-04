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

var settingsSocket;
/* Server response with instruction success message  */
var msg_success = "msg_success";
/* Server response with instruction fail message  */
var msg_fail = "msg_fail";
/* UI elements state  */
var ui_disabled = false;
/* Client action , passed from submit settings button, each settings section has unique action.
    We need this for modal dialog confirmation */
var clientAction = null;


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

    currnetSettingsData(confFile);
   
    settingsSocket = new SockJS(http_prefix + location.host + '/settings');
    
    settingsSocket.onopen = function() {
        console.log("settingsSocket is opened")
    };
    
    settingsSocket.onmessage = function(e) {
        data = JSON.parse(e.data);
        if ("requested" in data) {
        // this is instruction that was echoed from server + data as response
            instruction = data.requested;
            if (instruction in callbacks)
                callbacks[instruction](data);
        }
    };

    settingsSocket.onclose = function() {
        console.log('Settings Web socket is closed');
    };

 }); /** getJSON */

}); 


function currnetSettingsData(data) {
    var dns_name = data.dns_name.split(".")[0]; //split string to remove domain name.
        play_composition_on_server_boot = "";
        auto_to_ap = "";

    $("body").find("#userName").val(data.user);
    $("body").find("#networkBoardName").val(dns_name);

    if (data.play_composition_on_server_boot == "YES"){
        play_composition_on_server_boot = true
    } else {
        play_composition_on_server_boot = false
    }
    $("body").find("#userLatestProjectOnBoot").prop("checked", play_composition_on_server_boot);

    if (data.auto_to_ap == "YES") {
        auto_ap_mode = true
    } else {
        auto_ap_mode = false
    }
    $("body").find("#networkAutoApMode").prop("checked", auto_ap_mode);
};


/* Function will trigger modal dialog with reload message, 
  after confirmation we trigger appropriate function and pass clientAction to execute command.
*/

function openModal(action) {
    $("#resetBoardModal").modal("show");
    clientAction = action;
};

    $("#resetBoardModal").on('click', '#confirmAction', function(e) {
        $("#resetBoardModal").modal("hide");
        settingsAction(clientAction);        
    });

function settingsAction(command) {
    switch (command) {
        case 'UserData':
            updateUserData();
            break;
        case 'NetworkData':
            updateNetworkData();
            break;
    }
};

/* Save new user data */
function updateUserData() {
    if (!ui_disabled) {
        var user = $("body").find("#userDataForm #userName").val();
            password = $("body").find("#userDataForm #userPass").val();
            re_password = $("body").find("#userDataForm #reUserPass").val();
            latest_project_on_boot = $("body").find("#userDataForm #userLatestProjectOnBoot").is(':checked');
       
        if(latest_project_on_boot){
            latest_project_on_boot = "YES"
        } else {
            latest_project_on_boot = "NO"
        }
        // Check user password matching 
        if(password != re_password){
            ui_disabled = true;
            $("body").find("#reponseMsg").append("<div class='alert alert-message alert-error'>Passwords do not match!</div>").hide().slideToggle( "slow" );
            
        } else {
            updateData = {"request": "updateSettings", "data": {"user": user, "password": password, "play_composition_on_server_boot" : latest_project_on_boot}};
            console.log(updateData);
            settingsSocket.send(JSON.stringify(updateData));
        }
        $(".alert-message").delay(5000).slideToggle("slow", function () { $(this).remove(); ui_disabled = false });
        
    }
};

/* Save new network data */
function updateNetworkData() {
    if(!ui_disabled){
        var board_name = $("body").find("#networkBoardName").val().split(".")[0]; // split string to avoid domain name (e.g avoid .locale)
            auto_ap_mode = $("body").find("#networkAutoApMode").is(":checked");

        if(auto_ap_mode) {
            auto_ap_mode = "YES"
        } else {
            auto_ap_mode = "NO"
        }
        
            updateData = {"request": "updataNetwork", "data": {"dns_name": board_name, "auto_to_ap": auto_ap_mode }};
            console.log(updateData);
        
        settingsSocket.send(JSON.stringify(updateData));
    }
};


function reponse_msg(data) {
    if(data.data == msg_success){
        $("body").find("#reponseMsg").append("<div class='alert alert-message alert-success'>Bord settings successfully saved!</div>").hide().slideToggle( "slow" );
    } else {
        $("body").find("#reponseMsg").append("<div class='alert alert-message alert-error'>Oops something went wrong!</div>").hide().slideToggle( "slow" );
    }
    ui_disabled = true; // Disable  settings saving, until alert message is present.
    $(".alert-message").delay(5000).slideToggle("slow", function () { $(this).remove(); ui_disabled = false });
};


//CALLBACKS////////////////////////////////////////////////////////////////////////////////////////////////////////x
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var callbacks = {
    "updateSettings": reponse_msg,
    "updataNetwork": reponse_msg
}