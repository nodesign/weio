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
var dashboard;
/*
 * When all DOM elements are fully loaded
 */
$(document).ready(function () {
    updateIframeHeight();

    // generate random number to prevent loading page from cache
    var randomNumber = Math.random();
      
    $(".iframeContainer").attr("src", "editor.html?" + randomNumber);
                  
   runEditor();
                  
   dashboard = new SockJS('http://' + location.host + '/dashboard');
                  
//////////////////////////////////////////////////////////////// SOCK JS DASHBOARD        
        
/*
 * On opening of wifi web socket ask server to scan wifi networks
 */
    dashboard.onopen = function() {
        console.log('Dashboard Web socket is opened');
        // turn on green light if connected
        // get ip address
        
        isEditorActive = true;
        
        var dashboardPacket = new Array();
        
        var rq = { "request": "getIp"};
        //dashboard.send(JSON.stringify(rq));
        
        dashboardPacket.push(rq);
        
        rq = { "request": "getLastProjectName"};
        //dashboard.send(JSON.stringify(rq));
        
        dashboardPacket.push(rq);
        
        
        rq = { "request": "getUserProjetsFolderList"};
        //dashboard.send(JSON.stringify(rq));
        
        dashboardPacket.push(rq);
        
        rq = { "request": "getUser"};
        //dashboard.send(JSON.stringify(rq));
        
        dashboardPacket.push(rq);
        
        rq = { "request" : "packetRequests", "packets":dashboardPacket};
        console.log("sending dashboard packets together ", rq);
        dashboard.send(JSON.stringify(rq));
        //setTimeout(function(){dashboard.send(JSON.stringify(rq))},1000);

        
        
        /*
        var rq = { "request": "getPlatform"};
        dashboard.send(JSON.stringify(rq));
        */
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
    
    //$(".iframeContainer").show();
    $(".iframeContainer").animate( { "margin-top": "60px" }, { queue: false, duration: 500 });
    $(".iframeContainerIndex").animate( { "margin-top": screen.height+60+"px" }, { queue: false, duration: 500 });
    
    //$(".iframeContainerIndex").hide();

    $("#editorButtonHeader").attr("class", "top_tab selected");
    $("#previewButtonHeader").attr("class", "top_tab");

    isEditorActive = true;    
}


/*
 * Run preview mode
 */
function runPreview() {
    
    if (isEditorActive)
        document.getElementById("weioIframe").contentWindow.saveAll();
    
    play();
    
    
    $.getJSON('config.json', function(data) {
              var confFile = data;
              // generate random number to prevent loading page from cache
              var randomNumber = Math.random();
              
              $(".iframeContainerIndex").attr("src", "userProjects/" + confFile.last_opened_project + "index.html?"+randomNumber);
              // console.log(confFile.weio_lib_path);
              $(".iframeContainerIndex").css("height", screen.height-60 + "px");
              $(".iframeContainerIndex").css("margin-top", screen.height+60 + "px");
              
              //$(".iframeContainer").hide();
              });
    
    //$(".iframeContainers").animate( { "margin-top": -screen.height }, { queue: false, duration: 500 });
    $(".iframeContainer").animate( { "margin-top": -screen.height }, { queue: false, duration: 500 });
    $(".iframeContainerIndex").animate( { "margin-top": "40px" }, { queue: false, duration: 500 });
    
    $("#editorButtonHeader").attr("class", "top_tab");
    $("#previewButtonHeader").attr("class", "top_tab selected");
    
    isEditorActive = false;
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
 * 
 * setStatus(line, "hello world");
 * Line represents first or second line to display msg 0 or 1
 *
 */
function setStatus(line, message) {
    if (line == 0)
        $( "#statusBarText1" ).html(message);
    else
        $( "#statusBarText2" ).html(message);
}

function prepareToPlay() {
    if (isEditorActive) {
        document.getElementById("weioIframe").contentWindow.play();
        document.getElementById("weioIframe").contentWindow.hideAlert();
        document.getElementById("weioIframe").contentWindow.clearErrorAnnotations();
    } else {
        play();
    }
}

function play(){
    var rq = { "request": "play"};
    dashboard.send(JSON.stringify(rq));
    document.getElementById("weioIframe").contentWindow.clearConsole();
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
function updateError(data) {
	console.log(data)
	if (isEditorActive)
		document.getElementById("weioIframe").contentWindow.updateError(data);
}

/**
 * Deletes current project, this function was called from inside editor iFrame
 */
function deleteProject() {
    var rq = { "request": "deleteProject"};
    dashboard.send(JSON.stringify(rq));
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
    "deleteProject" : projectDeleted,
    "errorObjects": updateError
}

/**
 * After deletation of project reset project list and choose another to open
 */
function projectDeleted(data) {
    //console.log("delete project here");
    
    if (data.data == "reload page") {
        randomNumber = Math.random();
        var url = 'http://' + location.host + '/editor?'+ randomNumber; 
        window.location = url;
    }
}

/**
 * Shows local ip address on the screen
 */
function showIpAddress(data){
    setStatus(0, data.status);
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
    setStatus(1, data.status);
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
        $("#playButton").attr("class", "top_tab active");
    } else {
        $("#playButton").attr("class", "top_tab");
        
    }
    updateStatus(data);
}

function stopped(data) {
    $("#playButton").attr("class", "top_tab");
    updateStatus(data);
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
    
    changeProject(data.path);
}



