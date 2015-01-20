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
var editorSocket;

/*
 * ACE Editor, there is only one editor that travels thru DOM space
 * It appears at good strip at good time
 * Only thing that is change is Ace Session inside editor
 */
var editor;

/*
 * Sets active project ROOT path
 */
var projectRoot;

/*
 * Delete button clicked
 */
var deleteButtonClicked = false;

/*
 * Data related to files that are opened
 * name, type, data, id, path
 */
var editorsInStack = [];

/*
 * Tree interaction lock, avoid massive click and bugs
 */
var treeLock = false;

/**
 * Milliseconds interval for autosave
 */
var autoSaveInterval = 4000;

/**
 * Play is activated from dashboard,
 */
var playPushed = false;

/**
 * Autosave lock, deblock on keyup event in editor
 */
var activeAutoSave = false;

/*
 * User server port
 */
var userServerPort = 0;

/*
 * Read only mode message in editor (example projects files)
 */
var readOnlyModeMsg = '';

/**
 * Global configuration
 */
var confFile;

/*
 * When all DOM elements are fully loaded
 */
$(document).ready(function () {

     hideAlert();

    /*
     * left and right sidebar width when opened
     * DON'T MODIFY these parameters thay are hard
     * coded and hardcoded in weio.less file as well
     */
    var leftSideBarWidth = "199px";
    var rightSideBarWidth = "495px";

    /*
     * Closed sidebar (left or right) width
     * DON'T MODIFY these parameters thay are hard
     * coded and hardcoded in weio.less file as well
     */
    var closedSideBarWidth = "15px";

    updateConsoleHeight();

    $("#consoleTabs").hide();

    $("#leftSideBarButton").click(function(){

        if ($(this).is(".opened")) {
            $(".editorContainer").animate( {left: closedSideBarWidth},
                { queue: false, duration: 100, step:function(){$('.ace_content').css('width','100%')} } );
            $(".leftSideBar").animate({width: closedSideBarWidth}, {queue: false, duration: 100});
            $("#leftSideBarButton").animate({left: "-5px"}, {queue: false, duration: 100});
            $("#leftSideBarButton").attr("class", "closed");
            $("#leftSideBarButton i").attr("class", "icon-chevron-right");
            $(".tree").hide();
            $(".bottomButtons").hide();
        } else {
            $(".editorContainer").animate( {left: leftSideBarWidth},
                { queue: false, duration: 100, step:function(){$('.ace_content').css('width','100%')} } );
            $(".leftSideBar").animate({width: leftSideBarWidth}, {queue: false, duration: 100});
            $("#leftSideBarButton").animate({left: "177px"}, {queue: false, duration: 100});
            $("#leftSideBarButton").attr("class", "opened");
            $("#leftSideBarButton i").attr("class", "icon-chevron-left");
            $(".tree").show();
            $(".bottomButtons").show();
        }
      scaleIt();
    });

    $("#rightSideBarButton").click(function(){

        if ($(this).is(".opened")) {

            $(".editorContainer").animate( { right: closedSideBarWidth },
                { queue: false, duration: 100, step:function(){$('.ace_content').css('width','100%')}  });

            $(".rightSideBar").animate( { width: closedSideBarWidth }, { queue: false, duration: 100 });
            $("#rightSideBarButton").animate( { left: "-5px"}, { queue: false, duration: 100 });
            $("#rightSideBarButton").attr("class", "closed");
            $("#rightSideBarButton i").attr("class", "icon-chevron-left");
            $("#trashConsole").hide();
            $("#consoleTabs").hide();

        } else {

            $(".editorContainer").animate( { right: rightSideBarWidth }, { queue: false, duration: 100 });

            $(".rightSideBar").animate( { width: rightSideBarWidth }, { queue: false, duration: 100 });
            $("#rightSideBarButton").animate( { left: "0px"}, { queue: false, duration: 100 });
            $("#rightSideBarButton").attr("class", "opened");
            $("#rightSideBarButton i").attr("class", "icon-chevron-right");
            $("#trashConsole").show();
            $("#consoleTabs").show();

        }
       scaleIt();
    });

    $("#rightSideBarButton").trigger("click");
    window.setInterval("autoSave()",autoSaveInterval);


    $('.accordion').click(function(e){
        // Remove strip
        if ($(e.target).hasClass('icon-remove')){
            //console.log("fjdhsgjhfgsjkhfdgsjk");
            // Get Id from file
            var currentStrip = getEditorObjectFromParsedId("file_", $($(e.target).parents('.accordion-group')).attr('id'));
            currentStrip = currentStrip.path;
            //console.log("JHGJKHGJKKJGHKJHJGGHJK ", currentStrip);
            //var killIndex = $.inArray(currentStrip, currentlyOpened);

            if ($(e.target).parents('.accordion-group').find('#codeEditorAce').length > 0) {
                $(".safeHome").html('').append($('#codeEditorAce'));
                $(".safeHome").hide();
            }
            if($('.accordion-group').length <= 1 && $('#codeEditorAce').parents('.safeHome').length < 1){
                $(".safeHome").html('').append($('#codeEditorAce'));
                $(".safeHome").hide();

            }

            var iOBJ = findObjectInArray($(e.target).parents('.accordion-group').attr('id').split("_")[1]);
            // Save
            saveFile(editorsInStack[iOBJ]);

            // Remove from array
            editorsInStack.splice(iOBJ,1);

            // Remove DIV
            $(e.target).parents('.accordion-group').remove();
            scaleIt();
        }
    });

    $('#tree').bind(
        'tree.select',
        function(event) {
            if (event.node) {
                // node was selected
                var node = event.node;

                var runTree = true;
                path = node.name;
                var lastNode = node;

                // run thru the tree structure to find all parents. Path will be exported
                while(runTree) {
                    if (lastNode.parent.name != undefined) {
                      path = lastNode.parent.name + "/" + path;
                      lastNode = lastNode.parent;
                    } else {
                        runTree = false;
                    }
                }
                path = projectRoot + path;


                if (!treeLock) {
                    // console.log($(this).parents());
                    // prepareToDeleteFile
                    // console.log("FILE ", $(e.target).is("#deleteFileButton"));
                    // console.log("FOLDER ", $(e.target).is("#deleteProjectButton"));
                    //if ($(e.target).hasClass('icon-remove')){
                        var doesExist = false;

                        // Do I have to delete file or I have to open file?
                        if (deleteButtonClicked==false) {


                            // Adding strip if don't exists already
                            for (var i in editorsInStack) {
                                if (editorsInStack[i].path == path) {
                                    doesExist = true;
                                }
                            }

                            if (!doesExist){
                                // asks server to retreive file that we are intested in
                                // regular files
                                if ((path.indexOf(".css") != -1) || (path.indexOf(".py") != -1) || (path.indexOf(".js") != -1) ||
                                    (path.indexOf(".html") != -1) || (path.indexOf(".txt") != -1) || (path.indexOf(".md") != -1) ||
                                    (path.indexOf(".json") != -1) || (path.indexOf(".xml") != -1) || (path.indexOf(".less") != -1) ||
                                    (path.indexOf(".cofee") != -1) || (path.indexOf(".svg") != -1) ||
                                    // images
                                    (path.indexOf(".png") != -1) || (path.indexOf(".jpg") != -1) || (path.indexOf(".bmp") != -1) ||
                                    (path.indexOf(".gif") != -1)
                                    ){

                                   var rq = { "request": "getFile", "data":path};
                                   editorSocket.send(JSON.stringify(rq));
                                   treeLock = true; // LOCK TREE INTERACTION HERE
                               }    else {
                                   // tar archives
                                   if (path.indexOf(".tar") != -1) {
                                        console.log("GET TAR ARCHIVE!!!!!!!!!!!!!!!!!!!!!!!!!!!", path);
                                        var target = path.split("www/")[1];
                                        //console.log("GET TAR ARCHIVE!!!!!!!!!!!!!!!!!!!!!!!!!!!", target);

                                        var _addr = location.host;
                                        var a = _addr.split(":");
                                        //console.log("TAAAAAR", a);
                                        /** Get global configuration */
                                        $.getJSON('config.json', function(data) {
                                                confFile = data;

                                                var http_prefix = "http://"

                                                if (confFile.https == "YES") {
                                                    http_prefix = "https://";
                                                }
                                                else {
                                                    http_prefix = "http://";
                                                }
                                                _addr = http_prefix + a[0] + ':' + a[1];

                                                //console.log("GET TAR ARCHIVE!!!!!!!!!!!!!!!!!!!!!!!!!!!", _addr +"/"+target);
                                                //window.open(_addr +"/"+target);
                                                window.location.href = _addr +"/"+target;
                                        }); /** getJSON */  
                                    }
                                }
                                
                                treeLock = false;


                               // It's more sure to add to currentlyOpened array from
                               // websocket callback than here in case that server don't answer
                            } // if (!doesExist)

                       } else { // delete file here! and don't open strip
                           prepareToDeleteFile(path);
                       }
               } // if (!treeLock)


                //console.log(prjPath);
               // alert(node.name);
            }
            else {
                // event.node is null
                // a node was deselected
                // e.previous_node contains the deselected node
            }
        }
    );

    // Ace editor creation
    createEditor();


    //////////////////////////////////////////////////////////////// SOCK JS EDITOR

    /** Get global configuration */
    $.getJSON('config.json', function(data) {
                confFile = data;

                if (confFile.https == "YES") {
                    http_prefix = "https://";
                }
                else {
                    http_prefix = "http://";
                }

                /*
                * SockJS object, Web socket
                */
                editorSocket = new SockJS(http_prefix + location.host + '/editorSocket');
                /*
                * On opening of wifi web socket ask server to scan wifi networks
                */
                editorSocket.onopen = function() {
                    console.log('editor Web socket is opened');
                    // get files

                    editorPacket = new Array();

                    var rq = { "request": "getFileTree"};
                    //editorSocket.send(JSON.stringify(rq));

                    editorPacket.push(rq);

                    rq = { "request": "getPlatform"};
                    //editorSocket.send(JSON.stringify(rq));

                    editorPacket.push(rq);


                    rq = { "request": "getUserPortNumber"};
                    //editorSocket.send(JSON.stringify(rq));

                    editorPacket.push(rq);


                    rq = { "request" : "packetRequests", "packets":editorPacket};
                    console.log("EDITOR: sending editor packets together ", rq);

                    editorSocket.send(JSON.stringify(rq));
                    //setTimeout(function(){editorSocket.send(JSON.stringify(rq))},1000);
                };

                /*
                * Dashboard parser, what we got from server
                */
                editorSocket.onmessage = function(e) {
                    //console.log('Received: ' + e.data);

                    // JSON data is parsed into object
                    data = JSON.parse(e.data);
                    console.log(data);

                    // switch
                if ("requested" in data) {
                    // this is instruction that was echoed from server + data as response
                    instruction = data.requested;
                    if (instruction in callbacksEditor)
                        callbacksEditor[instruction](data);
                } else if ("serverPush" in data) {
                        // this is instruction that was echoed from server + data as response
                        instruction = data.serverPush;
                        if (instruction in callbacksEditor)
                            callbacksEditor[instruction](data);
                }
                };

                editorSocket.onclose = function() {
                    // turn on red light if disconnected
                    console.log('Dashboard Web socket is closed');
                };
    }); /** getJSON */  

    //////////////// CONSOLE TABS
    $("#tabConsole").click(function(e) {
        stopDataViz();
        // reset side bar size to default value
        rightSideBarWidth = "495px";
        resizeRightSideBar(rightSideBarWidth);
        $(".editorContainer").animate( { right: rightSideBarWidth }, { queue: false, duration: 100 });

    });

    $("#tabBoard").click(function(e) {
        stopDataViz();
        connectToBoard();
        // reset side bar size to default value
        rightSideBarWidth = "495px";
        resizeRightSideBar(rightSideBarWidth);
        $(".editorContainer").animate( { right: rightSideBarWidth }, { queue: false, duration: 100 });

  
    });

    $("#tabStats").click(function(e) {
        startDataViz();
        // reset side bar size to default value
        rightSideBarWidth = "495px";
        resizeRightSideBar(rightSideBarWidth);
        $(".editorContainer").animate( { right: rightSideBarWidth }, { queue: false, duration: 100 });

    });

    $("#tabDocumentation").click(function(e) {
        flatdocInit('docApi.md');
        stopDataViz();
        // resize side bar for documentatio preview
        rightSideBarWidth = "800px";
        resizeRightSideBar(rightSideBarWidth); 
        $(".editorContainer").animate( { right: rightSideBarWidth }, { queue: false, duration: 100 });

    });
    
    $("#tabJavascript").click(function(e) {
        flatdocInit('weioJS.md');
    });
    
    $("#tabPython").click(function(e) {
        flatdocInit('weioPY.md');
    });
    
   var flatdocInit = function(file){
        Flatdoc.run({
          fetcher: Flatdoc.file(file)
        });
    };
  
    // On flatdoc load, scroll to top of section
   $(document).on('flatdoc:ready', function() {
     $('#flatdoc-container').animate({
        scrollTop: $('#flatdoc-container').offset().top
        }, 500);
    }); 

    ////////////////////// ADD FILES EVENT
    $('#updateFiles').change(function(evt){
         handleFileSelect(evt);
    });

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

    // Loop through the FileList and render image files as thumbnails.
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
                         addNewFile(data);
                         };
                         })(f);

        // Read in the image file as a data URL (base64)
        var fileName = f.name;
        if ((fileName.indexOf(".html") != -1) || (fileName.indexOf(".py") != -1) || (fileName.indexOf(".json") != -1) ||
            (fileName.indexOf(".css") != -1) || (fileName.indexOf(".txt") != -1) || (fileName.indexOf(".js") != -1) ||
            (fileName.indexOf(".md") != -1) || (fileName.indexOf(".svg") != -1) || (fileName.indexOf(".xml") != -1) ||
            (fileName.indexOf(".less") != -1) || (fileName.indexOf(".coffee") != -1)) {
            reader.readAsText(f);
        } else {
            reader.readAsDataURL(f);
        }

    }
}

function createEditor(){
    editor = ace.edit("codeEditorAce");
    editor.setTheme("ace/theme/dawn");
    editor.getSession().setMode("ace/mode/javascript");
    editor.setValue("", 0);
    editor.setFontSize("11px");

    editor.getSession().setTabSize(4);
    editor.getSession().setUseSoftTabs(true);
    editor.getSession().setUseWrapMode(true);
    editor.setShowPrintMargin(false);

    // On chage content
    $('#codeEditorAce').keyup(function(e){
          // exclude arrowkeys
          if ((e.keyCode!=38) && (e.keyCode!=40) && (e.keyCode!=37) && (e.keyCode!=39)) {

            // Remove previous change note
            $('#codeEditorAce').parents('.accordion-group')
            .find('.accordion-toggle')
            .find('span.hasChanged').remove();

            // Add change note
            $('#codeEditorAce').parents('.accordion-group')
            .find('.accordion-toggle')
            .append($('<span />')
            .addClass('hasChanged')
            .text('*'));

            var iOBJ = findObjectInArray($('#codeEditorAce').parents('.accordion-group').attr('id').split("_")[1]);
            editorsInStack[iOBJ].data = editor.getValue();

            //activeAutoSave = true;
          }

        });

    editor.gotoLine(0);
}

// Pronalazimo objekat u nizu koji je vezan za file na kojem radimo
function findObjectInArray(objectID){
    for (var i=0; i<editorsInStack.length; i++){
        if(editorsInStack[i].id == objectID){
            return i;
        }
    }
}

function scaleIt(){
    var bigH = $(document).height();
    var hOthers = 0;

    var f = bigH - 30 - (38 * $('.accordion-group').length);

    // Put editor height
    $('.accordion-inner').height(f-19);

    // Resize
    $(editor).resize();
}


$(window).resize(function() {
    scaleIt();
    updateConsoleHeight();
});


function updateConsoleHeight() {
    var viewportHeight = $(window).height();
    $("#consoleOutput").css("height", viewportHeight-60);
}




//EDITOR////////////////////////////////////////////////////////////////////////////////////////////////////////


function clearConsole() {
    $('#consoleOutput').empty();
}


function getEditorObjectFromPath(path) {
    for (var i in editorsInStack) {

        if (editorsInStack[i].path == path) {
            return editorsInStack[i];
        }
    }
    return null;
}

function getEditorObjectFromParsedId(prefix, accId) {
    var id = accId.split(prefix);


    for (var i in editorsInStack) {

        if (editorsInStack[i].id == parseInt(id[1])) {
            return editorsInStack[i];
        }
    }
    return null;
}



function setEditorObjectToPath(path, obj) {
    for (var i in editorsInStack) {

        if (editorsInStack[i].path == path) {
            editorsInStack[i] = obj;
            break;
        }
    }
}

function getFileIdFromPath(path) {
    for (var i in editorsInStack) {

        if (editorsInStack[i].path == path) {
            return editorsInStack[i].id;
        }
    }
    return null;
}

function hideAlert() {
    $("#errorAlert").hide();
    scaleIt();
}

function showAlert(data) {
    $("#errorAlertContent").empty();
    $("#errorAlertContent").append("Error in file : "+ data.file + "</br>");
    $("#errorAlertContent").append(data.reason);

    $("#errorAlert").show();
    scaleIt();
}

function clearErrorAnnotations() {
    editor.getSession().clearAnnotations();
}


/**
 * Save file on the server
 */
function saveFile(data) {

    //var obj = getEditorObjectFromPath(path);
    //console.log("SAVE " + obj.name);
    var rq = { "request": "saveFile", "data":data};
    editorSocket.send(JSON.stringify(rq));

}

/**
 * Save all opened files on the server
 */
function saveAll() {
    if (editorsInStack.length > 0) {
        /*
        for (var i=0; i <  editorsInStack.length; i++) {
            var toUtf = encodeURI(editorsInStack[i].data);
            editorsInStack[i].data = toUtf;
        }
        */
        var rq = { "request": "saveAll", "data":editorsInStack};
        editorSocket.send(JSON.stringify(rq));
    }
}

/**
 * Play mode
 */
function play() {
    if (editorsInStack.length>0) {
        playPushed = true;
        saveAll();
    } else {
        window.top.play();
    }
}

/**
 * Auto save if there were changes
 */
function autoSave() {
    if (activeAutoSave) {
        saveAll();

        for (var i=0; i<editorsInStack.length; i++){

            // Save file on server
            //saveFile(editorsInStack[i]);

            // Remove change indicator
            $('#file_'+editorsInStack[i].id).find('span.hasChanged').animate({
                opacity:0
                },300, function(){
                    $(this).remove();
                    })
        }
    }
    activeAutoSave = false;
}



/*
 * MODAL CREATE NEW FILE
 */

/**
 * Stores file type from modal view before creation
 * Default type is html
 */
var newfileType = "html"; // default value if nothing selected

/**
 * Selecting file type from modal view before creation
 * default value has to be html
 */
function setFileType(type) {
    newfileType = type;
    //console.log("file " + type);
}

/**
 * Creates new file into server and opens it inside editor
 */
function createNewFile() {
    // add more key if needed here, like directory etc...
    var name = $("#newFileName").val();

    // Checks for strings that are either empty or filled with whitespace
    if((/^\s*$/).test(name)) {
        alert("I can't make file with empty name!");
    } else {

        var data = {
            "name" : name + "." + newfileType,
            "path" : ".",
            "data" : ""
            };

        var rq = { "request": "createNewFile", "data" : data};
        editorSocket.send(JSON.stringify(rq));
    }
}
/**
 * This is same request as createNewFile but is not sourced from modal view
 */
function addNewFile(data){
    var rq = { "request": "createNewFile", "data" : data};
    editorSocket.send(JSON.stringify(rq));
}


var toBeDeleted = ""; // filename to be deleted
function prepareToDeleteFile(filename) {
    $("#myModalDeleteFileLabel").html("Delete " + filename + "?");
    $('#deleteFile').modal('show');
    toBeDeleted = filename;
}

function prepareToDeleteProject() {
    $('#windowTitleDialog').modal('show');
}

function deleteFile() {
    var pr = toBeDeleted.split(projectRoot);
     
    if (pr[1].split("/").length==1) { // delete project
        deleteProject();
    } else { // delete only one file
        var rq = { "request": "deleteFile", "path":toBeDeleted};
        editorSocket.send(JSON.stringify(rq));
        toBeDeleted = "";
    }  
}

function deleteProject() {
    window.top.deleteProject();
}

/*
 * These functions will be called from dashboard
 */
var consoleLineCounter  = 0;
var consoleLastPageBuffer = new Array();
function updateConsoleOutput(data) {
    var stdout = data.data;
    var phrase = stdout + "<br>";

    // Bufferize last page
    if (consoleLastPageBuffer.length > 400)
        consoleLastPageBuffer.shift();

    consoleLastPageBuffer.push(phrase);

    // empty DOM element
    if (consoleLineCounter > 800) {
        $('#consoleOutput').empty();
        var p = consoleLastPageBuffer.join("") + phrase;
        phrase = p;
        consoleLineCounter = consoleLastPageBuffer.length;
        // destroy
        consoleLastPageBuffer = new Array();
    }

    $('#consoleOutput').append(phrase);
    scrollConsoleToBottom();

    consoleLineCounter++;
}

function updateConsoleError(data) {

    var stderr = data.data;
    //$('#consoleOutput').append("<a id='stderr'>" + stderr + "<br></a>");
    $('#consoleOutput').append("<div class='alert alert-error'>" + stderr + "<br></div>");
    scrollConsoleToBottom();
}

function updateConsoleSys(data) {
    var sys = data.data;
    //$('#consoleOutput').append("<a id='sys'>" + sys + "<br></a>");
    $('#consoleOutput').append("<div class='alert alert-info'>" + sys + "<br></div>");
    scrollConsoleToBottom();
}

function updateError(data) {

    var d = data.data;
    //TODO correct path here
    // Path extraction
    /*
    var projectName = $('.tree label[for=folder]').text();
    var splitedFile = d[(d.length-1)].file.split("/");
    console.log(splitedFile);
    var path = 'userProjects/' + projectName + '/'+splitedFile[(splitedFile.length -1)];
    */
    var lastErrorObj = d[(d.length-1)]

    var doesExist = false;

    console.log('error in file : ',path);

    // Adding strip if don't exists already
    for (var i in editorsInStack) {
        if (editorsInStack[i].path == path) {
            doesExist = true;
        }
    }

    if (!doesExist){
        var rq = { "request": "getFile", "data":path};
        editorSocket.send(JSON.stringify(rq));
        treeLock = true; // LOCK TREE INTERACTION HERE
    }
    console.log('error in line :',lastErrorObj.line)

    showAlert(lastErrorObj);
    editor.focus();
    setTimeout(function(){

               editor.getSession().setAnnotations([{
                                                   row: lastErrorObj.line-1,
                                                   column: 0,
                                                   text: lastErrorObj.reason,
                                                   type: "error" // also warning and information
                                                   }]);

        // TODO if it's inside this file. If file is not in project don't do anything
        editor.gotoLine(lastErrorObj.line);
        window.top.stop();

    },1000);
    scrollConsoleToBottom();

}

/*
 * Scrolling till bottom of console
 * In that way we see always the last info
 */
function scrollConsoleToBottom(){
    var elem = document.getElementById('consoleOutput');
    elem.scrollTop = elem.scrollHeight;
}


//CALLBACKS////////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var callbacksEditor = {
    "getFileTree" : updateFileTree,
    "status" : updateStatus,
    "stdout" : updateConsoleOutput,
    "stderr" : updateConsoleError,
    "sysConsole" : updateConsoleSys,
    "getFile": insertNewStrip,
    "getImage": previewImage,
    "saveFile": fileSaved,
    "createNewFile": refreshFiles,
    "deleteFile": fileRemoved,
    "saveAll": allFilesSaved,
    "errorObjects": updateError,
    "getUserPortNumber":setUserPortNumber
}

function setUserPortNumber(data){
    userServerPort = data.data;
}
function previewImage(data) {
    //console.log("IMAGE",data.data.name);
    $("#previewImage").css("width", "364px");
    $("#previewImageTitle").html(data.data.name);
    $("#imageToPreview").attr("src", data.data.data);
    $("#previewImage").modal("show");

    treeLock = false;
}

function allFilesSaved(data) {

    if (playPushed==true) {
        // finally call play in dashboard
        window.top.play();
    }

    playPushed = false;
  }

function fileSaved(data) {
    updateStatus(data);

}

/*
 * Insterts HTML code for file tree into sidebar
 * Attaches tree event listener
 */
function updateFileTree(data) {
    $(".icon-remove.delButton").unbind("click");
    deleteButtonClicked = false;
    
    projectRoot = data.projectRoot;
    // If example project is loaded, disable editing! 
    if(projectRoot.split("/")[1] === 'examples'){
        console.log("This is example project, read only mode acitvated");
        editor.setReadOnly(true);
        activeAutoSave = false;
        readOnlyModeMsg = 'Read only';
    } else {
        editor.setReadOnly(false);
        activeAutoSave = true;
        readOnlyModeMsg = '';
    }

    //$("ul.jqtree_common.jqtree-tree").html("");
    $("#tree").html();

    $('#tree').tree({
        // we have to give it array of dictionaries
        data: data.data,
        autoOpen: true
    });

    //$('#tree1').tree('reload');

    $('#tree').tree('loadData', data.data);
    // when tree is loaded then add x buttons
    //$('#tree1').load(addDeleteButtons());
    var tag = "<i class='icon-remove delButton' id='deleteButton' role='button' data-toggle='modal'></i>";
    $(tag).appendTo("div.jqtree-element.jqtree_common");
 
    $(".icon-remove.delButton").bind("click", clickDeleteButton);


    // $(".icon-remove.delButton").click(function(){
   //   console.log("deleteButton clicked!");
   //   deleteButtonClicked = true;
   //  });

}

function clickDeleteButton(){
     console.log("deleteButton clicked!");
     deleteButtonClicked = true;
}

function addDeleteButtons() {
    var tag = "<i class='icon-remove delButton' id='deleteButton' role='button' data-toggle='modal'></i>";
    $(tag).appendTo("div.jqtree-element.jqtree_common");
    $(".icon-remove.delButton").click(function(){
     console.log("deleteButton clicked!");
     deleteButtonClicked = true;
    });
}

function reloadEditor() {
    window.top.reloadIFrame(null);
}

function fixedCollapsing(showMe) {
    // Open new element and hide others

    // Collapse all
    $('.accordion-group').each(function(index, element) {
                               if ($(element).find('.collapse').hasClass('in')){
                               $(element).find('.collapse').collapse('hide');
                               }
                               });

    // Hidding inner div
    $(showMe).find('.collapse').on('show', function () {
                               $(showMe).find('.accordion-inner').animate({opacity:0},300,'linear',function(){
                                                                      //Get coresponding data and put to editor
                                                                      var acc_id = $($(this).parents('.accordion-body')).attr('id');
                                                                      var o = getEditorObjectFromParsedId("acc_",acc_id);

                                                                      var iOBJ = findObjectInArray($($(this).parents('.accordion-body')).attr('id').split("_")[1]);
                                                                      editor.setValue(editorsInStack[iOBJ].data);
                                                                      console.log(iOBJ);
                                                                      editor.getSession().setMode("ace/mode/"+editorsInStack[iOBJ].type);
                                                                      editor.gotoLine(0);

                                                                      console.log(editorsInStack[iOBJ].type, editor.getSession().getMode());


                                                                      });
                               })

    // Showing inner div and inserting editor
    $(showMe).find('.collapse').on('shown', function () {
                               $('#codeEditorAce').appendTo($(showMe).find('.accordion-inner'));
                               scaleIt();
                               $(showMe).find('.accordion-inner').animate({opacity:1},300,'linear');
                                  // console.log("SHOWN");

                               })

    // Showing inner div and inserting editor
    $(showMe).find('.collapse').on('hide', function () {
                                   // Get contents and put to array
                                   var path = $(this).parent().attr('id');

                                   // Pronadji objekat koji mu treba
                                   var iOBJ = findObjectInArray($(this).parent().attr('id').split("_")[1]);

                                   editorsInStack[iOBJ].data = editor.getValue();
                                   console.log('sacuvan data');

                                   var o = getEditorObjectFromPath(path);

                                   /*if (o != null) {
                                    o.data = editor.getValue();
                                    setEditorObjectToPath(path, o);
                                    saveFile(path);
                                   }*/

                                   $('#codeEditorAce').appendTo($(showMe).find('.accordion-inner'));
                                   scaleIt();
                                   $(showMe).find('.accordion-inner').animate({opacity:1},300,'linear');

                    })


    // Showing accordion
    $(showMe).find('.collapse').collapse('show');
}

/**
 * Inserts existing editor in new strip if file is on the server
 */

function insertNewStrip(data) {

    var e = {};
    //e.data = unescape(decodeURIComponent(data.data.data));
    e.data = data.data.data;
    e.name = data.data.name;
    e.path = data.data.path;
    e.type = data.data.type;
    e.id = data.data.id;

    // add to array of current opened files

    editorsInStack.push(e);

    // it has been already checked if this file already exists
    // so just insert it straight

    var title = data.data.name;
    idEl = data.data.id;

    // Element
    var el = $('<div />').html('<div class="accordion-heading"><a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" id="att_' +
            idEl + '" href="#'+'acc_'+idEl+'">'+title+'</a><div class="actions"><a class="read-only-msg">' + readOnlyModeMsg + '</a><a role="button" id="closeButton"><i class="icon-remove"></i></a></div></div><div id="acc_'
            + idEl + '" class="accordion-body collapse"><div class="accordion-inner"></div></div>').addClass('accordion-group').attr("id", "file_" + data.data.id);

    // Add new strip here
    $('#accordion2').append(el);


    fixedCollapsing(el);


    $('.accordion-toggle').click(function(){
                                 fixedCollapsing(this);
                                 });

    //currentlyOpened.push(data.data.path);

    if (editorsInStack.length == 1){
        $(el).find('.accordion-inner').html('').append($('#codeEditorAce'));
        $('#codeEditorAce').css({'display':'block'});
    }

    // Pronadji
    /*var iOBJ = findObjectInArray(idEl);
    editor.setValue(editorsInStack[iOBJ].data);
    editor.getSession().setMode("ace/mode/"+editorsInStack[iOBJ].type);
    editor.gotoLine(0);
    console.log(iOBJ)*/


    // Update height
    scaleIt();

    treeLock = false; // UNLOCK TREE INTERACTION
}


function updateStatus(data) {
    //console.log(data);
    window.top.setStatus(null, data.status);
}


function refreshFiles(data) {
    updateStatus(data);
    // refresh html filetree
    var rq = { "request": "getFileTree"};
    editorSocket.send(JSON.stringify(rq));
}

function fileRemoved(data) {
    updateStatus(data);
    // refresh html filetree
    var rq = { "request": "getFileTree"};
    editorSocket.send(JSON.stringify(rq));
    // delete strip if opened
    var path = data.path;
    var doesExist = false;

    // Adding strip if don't exists already
    for (var i in editorsInStack) {

        if (editorsInStack[i].path == path) {
            doesExist = true;
        }
    }

    if (doesExist){ // kill strip

        var currentStrip = path;
        var currentId = 0;

        for (var i in editorsInStack) {

            if (editorsInStack[i].path == currentStrip) {
                currentId = editorsInStack[i].id;
                editorsInStack.splice(i,1);
                break;
            }
        }

        // save editor in safe house before

        $(".safeHome").html('').append($('#codeEditorAce'));
        $(".safeHome").hide();

        //console.log($(e.target).parents('.accordion-group'), $(e.target).parent('.accordion-group'));

        $("#file_"+currentId).remove();
    }
}

/*
 * Checks if index.html exists in project
 */
function isIndexExists() {
    console.log("DEBUG ", $("#tree").find("a"));

    var files = $(".tree").find("a");

    for (var i=0; i<files.length; i++) {
        var file = files[i];
        if ($(file).html()== "index.html") {
            return true;
        } else {
            return false;
        }
    }
}

/*
 * Checks if main.py exists in project
 */

function isMainExists() {
    var files = $(".tree").find("a");

    for (var i=0; i<files.length; i++) {
        var file = files[i];
        if ($(file).html()== "main.py") {
            return true;
        } else {
            return false;
        }
    }
}

/* Resize right side bar for better documentation preview */
function resizeRightSideBar(size) {
    $(".rightSideBar").animate({width:size}, 100);
  
};


