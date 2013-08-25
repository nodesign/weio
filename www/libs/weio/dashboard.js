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
 * SockJS object, Web socket
 */
var dashboard = new SockJS('http://' + location.host + '/dashboard');

/*
 * When all DOM elements are fully loaded
 */
$(document).ready(function () {
    updateIframeHeight();
    runEditor();
    
}); /* end of document on ready event */

/*
 * isEditorActive
 */
var isEditorActive = null;



$(window).resize(function() {
   updateIframeHeight();
   $('#weioIframe').find('#tree').empty();
});

function updateIframeHeight() {
    var iframeHeight = $(window).height() - 60;
    $(".iframeContainer").css("height", iframeHeight + "px");
}

/* 
 * Run Editor in targeted IFrame
 */ 
function runEditor() {
    $(".iframeContainer").attr("src", "editor.html");
    $("#editorButtonHeader").attr("class", "top_tab active");
    $("#previewButtonHeader").attr("class", "top_tab");
}


/*
 * Run preview mode
 */
function runPreview() {
    document.getElementById("weioIframe").contentWindow.saveFocusedFile();
    var confFile = "";
    
       $.getJSON('config.json', function(data) {
           confFile = data;
           
           $(".iframeContainer").attr("src", "userProjects/" + confFile.last_opened_project + "index.html");
          // console.log(confFile.weio_lib_path);
     });
     
     $("#editorButtonHeader").attr("class", "top_tab");
     $("#previewButtonHeader").attr("class", "top_tab active");
}

/*
 * Run settings mode
 */

function runSettings() {
    $(".iframeContainer").attr("src", "settings.html");
    $("#editorButtonHeader").attr("class", "top_tab");
    $("#previewButtonHeader").attr("class", "top_tab");
}

function createNewProject() {
    projectName = $("#newProjectName").val();
    var rq = { "request": "createNewProject", "path":projectName};
    dashboard.send(JSON.stringify(rq));
}

/**
 * Sets coresponding icon and message inside statusBar in the middle of header. 
 * Icon is string format defined in font awesome library, message is string format
 * If icon is not desired you can pass null as argument : setStatus(null, "hello world");
 *
 * Icons are only used when synchronization is active or weioMain is running
 * Set status is always activated from server push messages, never from client,
 * except when closed socket is detected!
 */
function setStatus(icon, message) {

    if (icon!=null) 
    $( "#statusBar" ).html('<p id="statusBarText"><i id="statusIcon" class="' + icon + '"></i>' + message + '</p>');
    else 
    $( "#statusBar" ).html('<p id="statusBarText">' + message + '</p>');
}

function play(){
    var rq = { "request": "play"};
    dashboard.send(JSON.stringify(rq));
}

function stop(){
    var rq = { "request": "stop"};
    dashboard.send(JSON.stringify(rq));
}

function changeProject(path) {
    var rq = { "request": "changeProject", "data": path};
    dashboard.send(JSON.stringify(rq));
}

function updateConsoleSys(data) {
    if (isEditorActive) 
        document.getElementById("weioIframe").contentWindow.updateConsoleSys(data);
}

function updateConsoleOutput(data) {
    if (isEditorActive)
        document.getElementById("weioIframe").contentWindow.updateConsoleOutput(data);
}

function updateConsoleError(data) {
    if (isEditorActive)
        document.getElementById("weioIframe").contentWindow.updateConsoleError(data);
}


//CALLBACKS////////////////////////////////////////////////////////////////////////////////////////////////////////x  
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var callbacks = {
    "getIp": showIpAddress,
    "getLastProjectName": showProjectName,
    "status" : updateStatus,
    "play": isPlaying,
    "stop": stopped,
    "getUserProjetsFolderList" : updateProjects,
    "changeProject":reloadIFrame,
    "getUser": updateUserData,
    "sysConsole" : updateConsoleSys,
    "stdout" : updateConsoleOutput,
    "stderr" : updateConsoleError,
    "createNewProject" : newProjectIsCreated,
    
}

/**
 * Shows local ip address on the screen
 */
function showIpAddress(data){
    setStatus(null, data.status);
}

/**
 * Shows project name on the dashboard
 */
function showProjectName(data){
    $("#projectTitle").empty();
    $("#projectTitle").append(data.data);
}

/**
 * Updates status of application from server
 */
function updateStatus(data){
    console.log("data.status");
    setStatus(null, data.status);
}

/**
 * Get project names and put it into dropbox menu
 */
function updateProjects(data) {
    
    $("#userProjectsList").empty();
    $("#userProjectsList").append('<li><a tabindex="-1" href="#createNewProject" role="button" data-toggle="modal">Create new project</a></li>');
    $("#userProjectsList").append('<li class="divider"></li>');
    
    for (var folder in data.data) {
        var s = "'"+String(data.data[folder])+"'";    
        $("#userProjectsList").append('<li><a class="cells" tabindex="-1" href="javascript:changeProject('+s+')">' + data.data[folder] + '</a></li>') 
    }
    
}

function reloadIFrame(data) {
    document.getElementById('weioIframe').contentWindow.location.reload();
}

function isPlaying(data) {
    if (data.state!="error") {
        $("#playButtonIcon").attr("src", "img/weio-play-green.png");
        $("#playButton").css("opacity", "1");
    } else {
        $("#playButtonIcon").attr("src", "img/weio-play-red.png");
        $("#playButton").css("opacity", "1");
    }
    updateStatus(data);
}

function stopped(data) {
    $("#playButtonIcon").attr("src", "img/weio-play.png"); 
    $("#playButton").css("opacity", "0.5");
    
}

/**
 * Get name of owner
 */
function updateUserData(data) {
    $("#user").html(data.name);
    
}

function newProjectIsCreated(data) {
    
    updateStatus(data);
    
    var rq = { "request": "getUserProjetsFolderList"};
    dashboard.send(JSON.stringify(rq));
    // TODO change project in editor
}


//////////////////////////////////////////////////////////////// SOCK JS DASHBOARD        
        
/*
 * On opening of wifi web socket ask server to scan wifi networks
 */
dashboard.onopen = function() {
    console.log('Dashboard Web socket is opened');
    // turn on green light if connected
    // get ip address
    isEditorActive = true;
    var rq = { "request": "getIp"};
    dashboard.send(JSON.stringify(rq));
    
    var rq = { "request": "getLastProjectName"};
    dashboard.send(JSON.stringify(rq));
    
    var rq = { "request": "getUserProjetsFolderList"};
    dashboard.send(JSON.stringify(rq));
    
    var rq = { "request": "getUser"};
    dashboard.send(JSON.stringify(rq));
    
    var rq = { "request": "getPlatform"};
    dashboard.send(JSON.stringify(rq));
    
};

/*
 * Dashboard parser, what we got from server
 */
dashboard.onmessage = function(e) {
    //console.log('Received: ' + e.data);

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


dashboard.onclose = function() {
    // turn on red light if disconnected
    console.log('Dashboard Web socket is closed');
    isEditorActive = false;
    $("#status").attr("class", "disconnected");
};