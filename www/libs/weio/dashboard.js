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
 * WeIO is updating or not
 */
var updateMode = false;

/*
 * Count till play percent of progress bar
 */
var readyToPlay = 0;

/*
 * Play counter interval event
 */
var playCounter;

/*
 * Does weio player playing user scripts?
 */
var isPlaying = false;

/*
 * When all DOM elements are fully loaded
 */
$(document).ready(function () {
    updateIframeHeight();

    // generate random number to prevent loading page from cache
    var randomNumber = Math.random();
      
    $(".iframeContainer").attr("src", "editor.html?" + randomNumber);
                  
   runEditor();
    
    weioProgress = new Chart(document.getElementById("weioProgress").getContext("2d"));
                        
                                    
//////////////////////////////////////////////////////////////// SOCK JS DASHBOARD        
                  
    dashboard = new SockJS('http://' + location.host + '/dashboard');
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
                  
                  
        rq = { "request": "getPlayerStatus"};
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
        
        var lostContact = "Browser lost connexion with WeIO! Try to simply reload this page. If problem still remains push WeIO reset button."
        setTestament(lostContact);
        
    };   
    
    
   
    
}); /* end of document on ready event */

   function updateProgress(evt) {
       // evt is an ProgressEvent.
       if (evt.lengthComputable) {
           var percentLoaded = Math.round((evt.loaded / evt.total) * 100);
           // Increase the progress bar length.
           if (percentLoaded < 100) {
               window.top.updateWeioProgressWheel(percentLoaded);
               //console.log(percentLoaded + '%');
           }
       }
   }

   function transferEnded(evt) {
      // console.log("end");
       window.top.updateWeioProgressWheel(100);
   }

   function errorFile(evt) {
       switch(evt.target.error.code) {
           case evt.target.error.NOT_FOUND_ERR:
               alert('File Not Found!');
               break;
           case evt.target.error.NOT_READABLE_ERR:
               alert('File is not readable');
               break;
           case evt.target.error.ABORT_ERR:
               break; // noop
           default:
               alert('An error occurred reading this file.');
       };
   }

function handleFileSelect(evt) {
   var files = evt.target.files; // FileList object
    //console.log("FILE");
   
   
   for (var i = 0, f; f = files[i]; i++) {

       /*
       // Only process image files.
       if (!f.type.match('image.*')) {
           continue;
       }
       */
       var reader = new FileReader();

       reader.onprogress = updateProgress;
       reader.onloadend = transferEnded;
       reader.onerror = errorFile;

       // Closure to capture the file information.


       reader.onload = (function(theFile) {
                        return function(e) {
                        //console.log("FILE ", theFile.name, " ", e.target.result);
                        data = {}
                        data.name = theFile.name;
                        data.data = e.target.result;
                        addNewProjectFromArchive(data);
                        };
                        })(f);

        reader.readAsDataURL(f);
  
   }
}

/*
 * Add new project from TAR archive
 */ 
function addNewProjectFromArchive(data){
   var rq = { "request": "addNewProjectFromArchive", "data" : data};
   dashboard.send(JSON.stringify(rq));
}

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

function setTestament(data) {
    if (updateMode == false) {
        $("#testament").html(data);
        $("#imDead").modal("show");
    }
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
    
    if (!isPlaying)
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

function duplicateProject() {
    projectName = $("#duplicatedProjectName").val();
    var rq = { "request": "duplicateProject", "path":projectName};
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
    playCounter = setInterval(function(){countTillPlay()},63);
    $( "#weioProgress" ).fadeTo( "fast", 100 );

}

function stop(){
    var rq = { "request": "stop"};
    dashboard.send(JSON.stringify(rq));
    $( "#weioProgress" ).fadeTo( "slow", 0 );
    clearInterval(playCounter);
    readyToPlay = 0;

}

function countTillPlay() {
    updateWeioProgressWheel(readyToPlay);
    readyToPlay+=2;
}

function updateWeioProgressWheel(data) {
    $( "#weioProgress" ).css( "opacity", "100%" );
    /*
     * CHART JS prefs
     */
    var defs = {
        //Boolean - Whether we should show a stroke on each segment
        segmentShowStroke : false,
        
        //String - The colour of each segment stroke
        segmentStrokeColor : "#000",
        
        //Number - The width of each segment stroke
        segmentStrokeWidth : 0,
        
        //The percentage of the chart that we cut out of the middle.
        percentageInnerCutout : 60,
        
        //Boolean - Whether we should animate the chart	
        animation : false,
        
        //Number - Amount of animation steps
        animationSteps : 100,
        
        //String - Animation easing effect
        animationEasing : "easeOutBounce",
        
        //Boolean - Whether we animate the rotation of the Doughnut
        animateRotate : true,
        
        //Boolean - Whether we animate scaling the Doughnut from the centre
        animateScale : false,
        
        //Function - Will fire on animation completion.
        onAnimationComplete : null
    }
    

    
    var wheel = [
                   // CPU
                   {
                   value: data,
                   color : "#3CDDF7"
                   },
                   {
                   value : 100-data,
                   color:"#444"
                   }
                   ];
    
    weioProgress.Doughnut(wheel, defs);
    if (data==100) {
        readyToPlay = false;
        clearInterval(playCounter); 
        // fade out wheel
        $( "#weioProgress" ).fadeTo( "slow", 0 );
    }
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
    "play": setPlayerStatus,
    "stop": stopped,
    "getUserProjetsFolderList" : updateProjects,
    "changeProject":reloadIFrame,
    "getUser": updateUserData,
    "sysConsole" : updateConsoleSys,
    "stdout" : updateConsoleOutput,
    "stderr" : updateConsoleError,
    "createNewProject" : newProjectIsCreated,
    "deleteProject" : projectDeleted,
    "errorObjects": updateError,
    "getPlayerStatus": playerStatus,
    "archiveProject": projectArchived
}


/**
 * Notify user that project has been archived and refresh file tree
 */
function projectArchived(data) {
    setStatus(1, data.status);
    reloadIFrame(data);
}

/**
 * This is player status demanded at the beginings play or stop state on player
 */
function playerStatus(data) {
    if (data.status!=false)
        $("#playButton").attr("class", "top_tab active");
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
    /*
    $("#userProjectsList").empty();
    $("#userProjectsList").append('<li><a tabindex="-1" href="#createNewProject" role="button" data-toggle="modal">Create new project</a></li>');
    $("#userProjectsList").append('<li><a tabindex="-1" id="activateProjectUpload">Import existing project</a></li>');
    $("#userProjectsList").append('<li class="divider"></li>');
    $("#userProjectsList").append('<li><a tabindex="-1" href="#duplicateProject" role="button" data-toggle="modal">Duplicate active project</a></li>');
    $("#userProjectsList").append('<li><a tabindex="-1" href="#downloadProject" role="button" data-toggle="modal">Archive active project</a></li>');
    $("#userProjectsList").append('<li class="divider"></li>');
   */
   
    // IMPORT PROJECT
   
    $('#activateProjectUpload').click(function(){
        $('#uploadProject').click();
    });
   
    $('#uploadProject').change(function(evt){
        handleFileSelect(evt);
    });
    
    for (var folder in data.data) {
        var s = "'"+String(data.data[folder])+"'";    
        $("#examplesUserProjects").append('<li><a class="cells" tabindex="-1" href="javascript:changeProject('+s+')">' + data.data[folder] + '</a></li>') 
    }
    
}

/**
 * Make tar archive of active project
 */
function archiveProject() {
    var rq = { "request": "archiveProject"};
    dashboard.send(JSON.stringify(rq));
}

function reloadIFrame(data) {
    document.getElementById('weioIframe').contentWindow.location.reload();
}

function setPlayerStatus(data) {
    if (data.state!="error") {
        isPlaying = true;
        $("#playButton").attr("class", "top_tab active");
        
    } else {
        isPlaying = false;
        $("#playButton").attr("class", "top_tab");
        
    }
    updateStatus(data);
}

function stopped(data) {
    isPlaying = false;
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


