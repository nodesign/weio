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


/**
 * Wifi Json structure. Interesting keys are : 
 * essid (string), 
 * quality (0-70 integer),
 * opened (true - for networks without security)
 * connected (true if Weio is connected to that network)
 * password (always empty, to be filled by user)
 */

var wifi = 0;
 
/**
 * Weio can be in two modes Acess Point AP and STA mode (client of one wifi network)
 */
var wifiCurrentMode = "sta"; // "sta" or "ap"

/**
 * Wifi network identifier that Weio is currently connected to.
 * We can't distinguish wifis only by their essid because there can be
 * two networks that have same name
 */
var connectedToWifiId = "";
var wifiMode = "";

/* * 
 * Wifi cell object that has been selected to be joined
 * not to confound with connectedToWifiId
 */
var selectedCell = -1;

/**
 * Global configuration
 */
var confFile;



//////////////////////////////////////////////////////////////////////////////////////////////////// SOCK JS WIFI        


/**
 * Wifi SockJS object, Web socket for scaning and changing wifi parameters
 */
var wifiSocket;

$(document).ready(function() {

    /** Get global configuration */
    $.getJSON('config.json', function(data) {
                    console.log("BBB");
                    confFile = data;
                    console.log(confFile);


            var http_prefix = "http://";

            if (confFile.https == "YES") {
                http_prefix = "https://";
            }
            else {
                http_prefix = "http://";
            }

            wifiSocket = new SockJS(http_prefix + location.host + '/wifi');
                    
            /*
            * On opening of wifi web socket ask server to scan wifi networks
            */
            wifiSocket.onopen = function() {
                console.log('Wifi Web socket is opened');
                //setTimeout(function(){scanWifiNetworks()},5000);
                scanWifiNetworks();
            };

            /*
            * Wifi web socket parser, what we got from server
            */
            wifiSocket.onmessage = function(e) {
                //console.log('Received: ' + e.data);
                
                // JSON data is parsed into object
                data = JSON.parse(e.data);
                console.log(data);
                
                if ("requested" in data) {
                    // this is instruction that was echoed from server + data as response
                    instruction = data.requested;  
                    
                    if (instruction in callbacksWifi) 
                        callbacksWifi[instruction](data);
                } else if ("serverPush" in data) {
                    // this is instruction that was echoed from server + data as response
                    
                    instruction = data.serverPush;  
                    if (instruction in callbacksWifi) 
                        callbacksWifi[instruction](data);
                }
            };

            wifiSocket.onclose = function() {
                console.log('Wifi Web socket is closed');

            };


    }); /** getJSON */
                  
});


/**
 * Generates drop down menu for wifi networks
 * first line in drop down menu will be status line that informs
 * user what is happening in network detection
 * for example : Detecting wifi networks...
 * List of wifi networks is shown directely from cache memory
 * At the same time new scan is launched and will update list
 * when he gets new data
 */


function injectWifiNetworksInDropMenu() {
//{"mac": "7656757", "essid": "ddwifi", "quality" : "50/70", "encryption" : "WPA2 PSK (CCMP)", "opened" : True, "connected": False}
    $("#wifiNetworks").empty();

   // $("#wifiNetworks").append('<li class="disabled"><a tabindex="-1" href="#">Scanning networks <i class="icon-spinner icon-spin" id="wifiIcons"></i></a></li>');
   // $("#wifiNetworks").append('<li class="divider"></li>');
//    
    $("#wifiNetworks").append('<li><a tabindex="-1" href="#changeWifi" role="button" data-toggle="modal">Connect to another network</a></li>');
    $("#wifiNetworks").append('<li><a tabindex="-1" href="#createWifi" role="button" data-toggle="modal" >Create network</a></li>');
    $("#wifiNetworks").append('<li><a tabindex="-1" href="#" onclick="scanWifiNetworks()">Rescan wifi networks</a></li>');
    $("#wifiNetworks").append('<li class="divider"></li>');

    // Eliminate wifi doubles
    var wifiCellsFiltered = [];
    for (var cell in wifi) {
        var rawCell = wifi[cell];
        var cellExists = false;
        for (var fCell in wifiCellsFiltered) {
            var filteredCell = wifiCellsFiltered[fCell];
            if (rawCell.essid == filteredCell.essid) {
                var rawCellQuality = getCellQuality(rawCell);
                var filteredCellQuality = getCellQuality(filteredCell);
                
                if (rawCellQuality>filteredCellQuality) {
                    wifiCellsFiltered[fCell] = rawCell;
                }
                
                cellExists = true;
            } 
        }
        
        if (cellExists == false) {
            wifiCellsFiltered.push(rawCell);
        }
    }
    
    //console.log("CELLS filtered", wifiCellsFiltered);
    //console.log("CELLS raw", wifi);
    
    
    
    for (var cell in wifiCellsFiltered) {
        // update current connected object
        if (wifiCellsFiltered[cell].connected == true) {
            connectedToWifiId = wifiCellsFiltered[cell].essid;
        }

        wifiMode =  wifiCellsFiltered[cell].mode;
        
        var secureWifi = (wifiCellsFiltered[cell].opened==false) ? '<i class="icon-lock" id="wifiIcons"></i>' : '';

        // detect where is my current network
        var currentConnection = (wifiCellsFiltered[cell].essid==connectedToWifiId) ? '<i class="icon-caret-right" id="wifiPrefixIcons"></i>' : '';
        
        // transform wifiQuality object into html
        var wifiQuality = '<img src="img/wifi' + getCellQuality(wifiCellsFiltered[cell]) + '.png" id="wifiIcons"></img>';
        
        var formatedWifi = "'" + wifiCellsFiltered[cell].mac + "'";
        $("#wifiNetworks").append('<li><a tabindex="-1" onclick="prepareToChangeWifi('+ formatedWifi + ')" role="button" data-toggle="modal">' + currentConnection  + wifiQuality + wifiCellsFiltered[cell].essid+ secureWifi + '</a></li>');
    }
    
    
      
    // don't do it here avoid infinite loop
    // scan wifi networks 
   // scanWifiNetworks();
};


/*
 * Parsing cell quality, returning integer 0-3
 */
function getCellQuality(cell) {
    // parse quality signal, original examples : 4/70, 50/70
    var rawStringQuality = cell.quality;
    var n = rawStringQuality.split("/");
    var wifiQuality = n[0];
     
    //console.log(parseInt(wifiQuality) + " " + cell.quality);
   
    // wifi quality signals are from 0-70, we have icons for total of 4 levels (icons from 0-3). 3/70 = 0.042857142857143
    wifiQuality = Math.round(parseInt(wifiQuality) * 0.042857142857143);
    
    return wifiQuality;
};


/*
 * Ask server to scan wifi networks
 */
function scanWifiNetworks() {
    var scanWifi = { "request": "scan"};
    wifiSocket.send(JSON.stringify(scanWifi));
};

/**
 * Prepare to change Wifi : store selected wifi cell in selectedCell 
 * object then call modal view to confirm. Once confirmed, modal view will
 * call changeWifiNetwork() that will give final instruction to server
 * to change network
*
 */

function prepareToChangeWifi(id) {
    var cell = -1;
    
    // verify if you are already connected to this network
    if (id != connectedToWifiId) { 
        for (var cell in wifi) {
            if (wifi[cell].mac == id) {
                // gotcha selected cell
                cell = wifi[cell];
                break;
            }
        }
        
        // put selected cell into object that will be used
        // in changeWifiNetwork()
        // in the case that modal is confirmed
        selectedCell = cell;
        
        // if password is required add password field 
        if (cell.opened==false) {
            // $("#wifiPassword").css("display", "block");
            $("#myModalSimpleChangeWifiLabel").html(cell.essid + " needs password");
             $("#wifiPasswordPrompt").modal("show");
        } else {
            //$("#wifiPassword").css("display", "none");
            goSta();
        }
        
       
    }
};

/**
 * Go to AP mode 
 */

function goAp() {
    var essidAPuser = document.getElementById("wifiSSIDAP").value;
    var pass = document.getElementById("wifiPasswordAP").value;
    
    // Checks for strings that are either empty or filled with whitespace
    if((/^\s*$/).test(essidAPuser)) {
        alert("I can't accept empty essid name!");
    } else {
        changeWifi = { "request": "goAp", "data": {"essid": essidAPuser, "passwd": pass}};
//        console.log(changeWifi);
        wifiSocket.send(JSON.stringify(changeWifi));
        $('#createWifi').modal('hide');
        
        var lostContact = "Browser lost connection with WeIO! That's normal because WeIO goes to AP - Acess Point mode now. Please connect to " + essidAPuser + " wifi network and then reload this page";
        setTestament(lostContact);
    }
    
};


/**
 * Send back chosen wifi network. Network has been previously chosed
 * by prepareToChange(id) function and stored in selectedCell object
 */

function goSta() {
    var changeWifi = 0;
    // opened means no password
    if (selectedCell.opened == false) {
        var password = $("#wifiPasswordSimple").val();
        
        // Checks for strings that are either empty or filled with whitespace
        if ((/^\s*$/).test(password)) { 
            alert("Password field can't be empty!");
        } else {
            selectedCell.passwd = password;
            $("#wifiPasswordPrompt").modal("hide");
            
            changeWifi = { "request": "goSta", "data" : selectedCell};
            console.log("GoTo STA ", changeWifi);
            wifiSocket.send(JSON.stringify(changeWifi));

            var lostContact = "Browser lost connection with WeIO! That's normal because WeIO goes to STA mode now. Please connect to " + selectedCell.essid + " wifi network and then reload this page";
            setTestament(lostContact);

            selectedCell = -1; // reset selection
        }
    } else {
        
        selectedCell.passwd = "";
        
        changeWifi = { "request": "goSta", "data" : selectedCell};
        console.log("GoTo STA ", changeWifi);
        wifiSocket.send(JSON.stringify(changeWifi));
        
        var lostContact = "Browser lost connection with WeIO! That's normal because WeIO goes to STA mode now. Please connect to " + selectedCell.essid + " wifi network and then reload this page";
        setTestament(lostContact);

        selectedCell = -1; // reset selection
    }
    
    
};

// Connect to other network /  Hidden AP
function connectToNewWiFi(){
    var ssid = $("#wifiSSID").val(),
        pass = $("#wifiPassword").val(),
        encryption = $("#encryption").val();
    
    // Checks for strings that are either empty or filled with whitespace
    if ((/^\s*$/).test(pass)) { 
        alert("Password field can't be empty!");
    } else if (ssid == '') {
        alert("SSID field can't be empty!");
    
    } else if (encryption == '') {
        alert("Encryption field can't be empty!");    
    } else {
       
        data = {'essid': ssid, 'passwd':pass, 'encryption': encryption};
        changeWifi = { "request": "goSta", "data" : data};
        wifiSocket.send(JSON.stringify(changeWifi));

        var lostContact = "Browser lost connection with WeIO! That's normal because WeIO goes to STA mode now. Please connect to " + selectedCell.essid + " wifi network and then reload this page";
        setTestament(lostContact);
    }
};


//CALLBACKS////////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var callbacksWifi = {
    "scan": updateWifiCells,
    "mode": updateWifiMode,
    
};

function updateWifiCells(data) { 
 
   //console.log("gotchaaaa");
   var cellList = data.data;
   
   for (var cell in cellList) {
       if (cellList[cell].connected) {
           $("#connectedWifiName").html('<img src="img/wifi' + getCellQuality(cellList[cell]) + '.png" id="wifiIcons"></img>' + cellList[cell].essid);
           break;
       }
   }
   wifi = cellList;
   injectWifiNetworksInDropMenu();
  
};

function updateWifiMode(data) {
    wifiMode = data.mode;
    console.log(wifiMode);
    if (wifiMode=="ap") {
        console.log("WE ARE IN AP MODE");
        $("#connectedWifiName").html(data.APessid);
    }
};

