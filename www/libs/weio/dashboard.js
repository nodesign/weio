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
 * Preview port number, user server port
 */
var userServerPort = 0;

/*
 * storage + project name
 */
var projectName = "";


/*
 * This variable stores last selected storage unit
 */
var selectedStorageUnit = null;

/**
 * Global configuration
 */
var confFile;

/**
 * Variable stores server state in order to provide ping/pong circle and 
   detect when client lose connection with server and server not responding, e.g Network down etc...
 */
var serverChechIn = true;

var serverChechInInterval = 10000;

/*
 * Time when last time stop or play has been pressed
*/
var stopTag;

/*
 * When all DOM elements are fully loaded
 */

// Message about low flash space (show one time per session)
var lowFashSpaceMsg = false;

// play/stop buttons enable/disable (prevent double clicking etc..)
var playButtonDisabled = false;
var stopButtonDisabled = false;
var disableTime = 3000;

$(document).ready(function () {
    updateIframeHeight();

    // generate random number to prevent loading page from cache
    var randomNumber = Math.random();
    $(".iframeContainer").attr("src", "editor.html?" + randomNumber);

    runEditor();

    weioProgress = new Chart(document.getElementById("weioProgress").getContext("2d"));

    /** Get global configuration */
    $.getJSON('config.json', function(data) {
            confFile = data;

            //////////////////////////////////////////////////////////////// SOCK JS DASHBOARD

            var http_prefix = "http://";

            if (confFile.https == "YES") {
                http_prefix = "https://";
            }
            else {
                http_prefix = "http://";
            }
            dashboard = new SockJS(http_prefix + location.host + '/dashboard');

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


                rq = { "request": "getPreviewPortNumber"};
                //dashboard.send(JSON.stringify(rq));

                dashboardPacket.push(rq);

                rq = { "request" : "packetRequests", "packets":dashboardPacket};
                console.log("DASHBOARD: sending dashboard packets together ", rq);
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

                var lostContact = "Browser lost connection with WeIO! Try to simply reload this page. " +
                    "If problem still remains push WeIO reset button."
                setTestament(lostContact);

            };
    }); /** getJSON */


    $('#importProjectUploader').change(function(evt){
            handleFileSelect(evt);
    });
    
    window.setInterval(function() {
        if (serverChechIn != false) {
            dashboard.send(JSON.stringify({'request': 'ping'}));
            serverChechIn = false; // reset server checkin state
        } else {
            dashboard.close(); // Close connection
        }
    }, serverChechInInterval);

    stopTag = new Date();

}); /* end of document on ready event */


 // Pong server callback from keep alive ping

function pingServer(pong) {
    if (!pong.response){
        dashboard.close(); // Close connection

    } else if (pong.low_disk_space && !lowFashSpaceMsg) { // Check for low flash space notification
        serverChechIn = true;
        setTestament("You are running out of free space on flash memory, only " + pong.low_disk_space + "MB is available. Clear flash space and use sd card as storage device.");
        lowFashSpaceMsg = true;

    } else{
        serverChechIn = true;
    }
    console.log(pong);
};

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
    var rq = { "request": "addNewProjectFromArchive", "data" : data, "storageUnit":selectedStorageUnit};
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
    $(".iframeContainerIndex").animate( { "margin-top": screen.height+60+"px" },
            { queue: false, duration: 500 });
    $(".iframeContainerIndex").css("display","none");
    $(".iframeContainer").css("display", "block");
    

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

    // generate random number to prevent loading page from cache
    var randomNumber = Math.random();

    var _addr = location.host;
    var a = _addr.split(":");

    var http_prefix = "http://";

    if (confFile.https == "YES") {
        http_prefix = "https://";
    }
    else {
        http_prefix = "http://";
    }
    
    if (userServerPort==80) {
        _addr = http_prefix + a[0];
    } else {
        _addr = http_prefix + a[0] + ':' + userServerPort;
    }
    
    var path = projectName;
    $(".iframeContainerIndex").attr("src", _addr + "/" + path + "/index.html?" + randomNumber);
    // console.log(confFile.weio_lib_path);
    $(".iframeContainerIndex").css({
        "display" : "block",
        "height" : screen.height-60 + "px"
        });
    $(".iframeContainerIndex").css("margin-top", screen.height+60 + "px");
    
    //$(".iframeContainer").hide();

    //$(".iframeContainers").animate( { "margin-top": -screen.height }, { queue: false, duration: 500 });
    $(".iframeContainer").animate( { "margin-top": -screen.height }, { queue: false, duration: 500 });
    $(".iframeContainer").css("display", "inline");
    $(".iframeContainerIndex").animate( { "margin-top": "40px" }, { queue: false, duration: 500 });

    $("#editorButtonHeader").attr("class", "top_tab");
    $("#previewButtonHeader").attr("class", "top_tab selected");

    isEditorActive = false;
}


/*
 * Run settings mode
 */
function runSettings() {
    console.log("=========>> runSettings() CALLED")
    updateIframeHeight();
    
    // generate random number to prevent loading page from cache
    var randomNumber = Math.random();
    $(".iframeContainer").attr("src", "settings.html?" + randomNumber);

    $("#editorButtonHeader").attr("class", "top_tab");
    $("#previewButtonHeader").attr("class", "top_tab");
}

function createNewProject() {
    projectName = $("#newProjectName").val();
    var rq = { "request": "createNewProject", "path":projectName, "storageUnit":selectedStorageUnit};
    console.log("STORAGE UNIT CREATE NEW PROJECT", selectedStorageUnit);
    dashboard.send(JSON.stringify(rq));
}

function duplicateProject() {
    projectName = $("#duplicatedProjectName").val();
    var rq = { "request": "duplicateProject", "path":projectName, "storageUnit":selectedStorageUnit};
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
    if(!playButtonDisabled){
        playButtonDisabled = true;
        if (isEditorActive) {
            document.getElementById("weioIframe").contentWindow.play();
            document.getElementById("weioIframe").contentWindow.hideAlert();
            document.getElementById("weioIframe").contentWindow.clearErrorAnnotations();
        } else {
            play();
        }
         setTimeout(function () { // Enable play after some time
            playButtonDisabled = false;  
        }, disableTime);
    }
}

function play(){
    var d = new Date();
    var inTime = 1500;
    var diff = d-stopTag;

    if (diff > inTime) {
        sendPlayToServer();
        document.getElementById("weioIframe").contentWindow.clearConsole();
        playCounter = setInterval(function(){countTillPlay()},4);
        $( "#weioProgress" ).fadeTo( "fast", 100 );
        console.log("play");

    } else {
        var delta = inTime-diff;
        setTimeout(function(){sendPlayToServer();}, delta);
        document.getElementById("weioIframe").contentWindow.clearConsole();
        playCounter = setInterval(function(){countTillPlay()},10);
        $( "#weioProgress" ).fadeTo( "fast", 100 );
        console.log("play differ");
    }

}

function sendPlayToServer() {
    var rq = { "request": "play"};
    dashboard.send(JSON.stringify(rq));
    stopTag = new Date();
}

function stop(){
    if(!stopButtonDisabled){
        stopButtonDisabled = true;
        stopTag = new Date();

        var rq = { "request": "stop"};
        dashboard.send(JSON.stringify(rq));
        $( "#weioProgress" ).fadeTo( "slow", 0 );
        clearInterval(playCounter);
        readyToPlay = 0;

        setTimeout(function () { // Enable stop after some time
            stopButtonDisabled = false;  
        }, disableTime);
    }
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
        updateWeioProgressWheel(0);
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
    "archiveProject": projectArchived,
    "getPreviewPortNumber": setPreviewPort,
    "ping": pingServer
}

/**
 * Set port number for preview
 */
function setPreviewPort(data){
   userServerPort =  data.data;
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

    var http_prefix = "http://";

    if (confFile.https == "YES") {
        http_prefix = "https://";
    }
    else {
        http_prefix = "http://";
    }

    if (data.data == "reload page") {
        randomNumber = Math.random();
        var url = http_prefix + location.host + '/?'+ randomNumber;
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
    projectName = data.data;
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
    
    var tag = "";
    tag+='<li><a tabindex="-1" href="#createNewProject" role="button" data-toggle="modal">Create new project</a></li>';
    tag+='<li><a tabindex="-1" href="#importProject" role="button" data-toggle="modal">Import existing project</a></li>';
    tag+='<li class="divider"></li>';
    tag+='<li><a tabindex="-1" href="#duplicateProject" role="button" data-toggle="modal">Duplicate active project</a></li>';
    tag+='<li><a tabindex="-1" href="#downloadProject" role="button" data-toggle="modal">Archive active project</a></li>';
    tag+='<li class="divider"></li>';

    // Parse example projects
   $.each( data.examples, function( idx, val ) {
        tag+='<li class="dropdown-submenu">\n';
        tag+='<a tabindex="-1" href="#">' + val.storageName + '</a>\n';
        tag+='<ul class="dropdown-menu" id="' + val.storageName + 'UserProjects">\n';
        
        if (val.projects.length==0) {
            tag += '<li><a class="cells" tabindex="-1" href="#createNewProject" role="button" data-toggle="modal">Create new project</a></li>\n';
        }
          $.map(val.projects, function(examples, key) {
                // Get directory structure
                $.each(examples, function(dir, idx){ 
                    tag+='<li class="dropdown-submenu scroll-menu">\n';
                    tag+='<a href="#">' + dir + '</a>\n';
                    tag+='<ul class="dropdown-menu">\n';
                    tag+='<ul class="dropdown-menu scroll-menu id="' + dir + 'UserProjects"">\n';
                    
                    // Get subdirectory structure
                    $.each(idx, function(subdir){
                        var s ="'" + val.storageName + "/" + String(dir) + '/' + String(subdir) + "'\n";
                        tag+= '<li><a class="cells" tabindex="-1" href="javascript:changeProject('+s+')">' + subdir + '</a></li>\n';
                    });
                    tag+= '</ul></ul></li>\n';
                });

                    // $.each(examples, function(dir, idx){
                    //     var s ="'" + val.storageName + "/" + String(dir) + "'\n";
                    //     tag+= '<li><a class="cells" tabindex="-1" href="javascript:changeProject('+s+')">' + dir + '</a></li>\n';
                    // });
            });
        tag+='</ul></li>\n';
    });
    
    tag+='<li class="dropdown-submenu">\n';
    tag+='<a tabindex="-1" href="#">myProjects</a>\n';
    tag+='<ul class="dropdown-menu" id="UserProjects">\n';
    
    // Parse user projects structure
    $.each( data.data, function( idx, val ) {
             tag+='<li class="dropdown-submenu scroll-menu">\n';
             tag+='<a href="#">' + val.storageName + '</a>\n';

            $.map(val.projects, function(examples, key) {
                tag+='<ul class="dropdown-menu">\n';
                tag+='<ul class="dropdown-menu scroll-menu id="' + val.storageName + 'UserProjects"">\n';
                if (jQuery.isEmptyObject(examples)) {
                    tag += '<li><a class="cells" tabindex="-1" href="#createNewProject" role="button" data-toggle="modal">Create new project</a></li>\n';
                } 
                $.each(examples, function(dir, idx){ 
                    var s ="'" + val.storageName + "/" + String(dir) + "'\n";
                    tag+= '<li><a class="cells" tabindex="-1" href="javascript:changeProject('+s+')">' + dir + '</a></li>\n';
                });
            tag+= '</ul></ul></li>\n';
            });
    });
    tag+='</ul></li>\n';

    $("#userProjectsList").empty();
    $("#userProjectsList").append(tag);

    tag = "";

    tag+='<ul class="nav nav-pills">';

    for (var i=0; i<data.data.length; i++) {
        if (i==0) 
            tag+='<li class="active" id="' + data.data[i].storageName +
                    'StorageUnit'+'"><a href="#">' + data.data[i].storageName + '</a></li>';
        else
            tag+='<li id="' + data.data[i].storageName + 'StorageUnit' + '"><a href="#">' + data.data[i].storageName + '</a></li>';
    }
    tag+='</ul>';

    $(".storageUnitChooser").empty();
    $(".storageUnitChooser").append(tag);

    if (selectedStorageUnit==null)
        selectedStorageUnit = data.data[0].storageName;

    $(".storageUnitChooser").on('click', 'li', function(e) {
       //alert($(this).attr("id"));
       $( ".storageUnitChooser li" ).each(function() {
           $( this ).attr( "class","notActive" );
       });
       $( this ).attr( "class", "active" );

       console.log($(this).attr("id").split("StorageUnit")[0]);
       changeSelectedStorageUnit($(this).attr("id").split("StorageUnit")[0]);

    });
}

function changeSelectedStorageUnit(unit) {
    selectedStorageUnit = unit;
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
    rq = { "request": "getLastProjectName"};
    dashboard.send(JSON.stringify(rq));
    reloadIFrame();

}

