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
 * Can be recalled when adding a new stripe to recalculate max height value
 */
function update_height() {

    // Get windows size, get number of collapse elements and calculate maximum height to fill the column
    var viewportHeight = $(window).height();

    var numRows = $('.codebox').length;
    //console.log("rows : " + numRows + " array elements " + editors.length);
    var finalheight = viewportHeight - (numRows  * 40) - 95;
    var widgetheight = viewportHeight - 140;
    $('.code_wrap').css('min-height', finalheight);
    $('.fullheight').css('height', widgetheight);

    $('#consoleAccordion').css('max-height', viewportHeight - (2  * 40) - 75);

}

/**
 * Calculate the main_container (editor + console) value depending on window size
 */

function main_container_width() {

    // Get windows size, get number of collapse elements and calculate maximum height to fill the column
    var viewportWidth = $(window).width();

    //console.log("rows : " + numRows + " array elements " + editors.length);
    var finalwidth = viewportWidth - 200;

    $('#main_container').css('width', finalwidth);

}

/*
 * SockJS object, Web socket
 */
var baseFiles = new SockJS('http://' + location.host + '/editor/baseFiles');

/**
 * Wifi SockJS object, Web socket for scaning and changing wifi parameters
 */
var wifiSocket = new SockJS('http://' + location.host + '/wifi');


/*
 * First time initialisation of editors
 */
var firstTime = true;

/**
 * ace code editors are stored in this array
 */
var editors = [];

/**
 * Selects correct index when code strips are manipulated
 */
var selectedName = -1;

/* * 
 * Stores compiled template that can be rendered with JSON file
 * to re-render just call renderTree(), compilation occurs only one inside
 * ready function
 */
var compiledTree;

/**
 * Stores compiled template that can be rendered with JSON file
 * to re-render just call renderEditor(), compilation occurs only one inside
 * ready function
 */
var compiledEditor;

/**
 * Stores currentely focused strip index in editorData.editors array
 */
var focusedOne = "weio_main.py";


/**
 * Informs if weio_main.py is running on Weio board
 */
var isPlaying = false;

/**
 * Console data array, stout and stderr
 */
var consoleData = [];

/**
 * maximum lines in console
 */
var MAX_LINES_IN_CONSOLE = 1000;


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
var wifiCurrentMode = "STA"; // "STA" or "AP"

/**
 * Wifi network identifier that Weio is currently connected to.
 * We can't distinguish wifis only by their essid because there can be
 * two networks that have same name
 */
var connectedToWifiId = "";

/* * 
 * Wifi cell object that has been selected to be joined
 * not to confound with connectedToWifiId
 */
var selectedCell = -1;

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
    
    $("#wifiNetworks").append('<li><a tabindex="-1" href="#">Connect to another network</a></li>');
    $("#wifiNetworks").append('<li><a tabindex="-1" href="#">Create network</a></li>');
    $("#wifiNetworks").append('<li><a tabindex="-1" href="#" onclick="scanWifiNetworks()">Rescan wifi networks</a></li>');
    $("#wifiNetworks").append('<li class="divider"></li>');
    
    for (var cell in wifi) {

        // update current connected object
        if (wifi[cell].connected == true) connectedToWifiId = wifi[cell].mac;

        var secureWifi = (wifi[cell].opened==false) ? '<i class="icon-lock" id="wifiIcons"></i>' : '';

        // detect where is my current network
        var currentConnection = (wifi[cell].mac==connectedToWifiId) ? '<i class="icon-check" id="wifiPrefixIcons"></i>' : '';

        // transform wifiQuality object into html
        var wifiQuality = '<img src="img/wifi' + getCellQuality(wifi[cell]) + '.png" id="wifiIcons"></img>';
        
        $("#wifiNetworks").append('<li><a tabindex="-1" onclick="prepareToChangeWifi('+ wifi[cell].mac + ')" role="button" data-toggle="modal">' + currentConnection + wifi[cell].essid  + wifiQuality + secureWifi + '</a></li>');
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
}


/*
 * Ask server to scan wifi networks
 */
function scanWifiNetworks() {
    var scanWifi = { "request": "scan"};
    wifiSocket.send(JSON.stringify(scanWifi));
}

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
    if (id!=connectedToWifiId) { 
        for (var cell in wifi) {

            if (wifi[cell].mac == id) {
                // gotcha selected cell
                cell = wifi[cell];
                break;
            }
        }

        $("#myModalChangeWifiLabel").html("Join " + cell.essid + " wireless network?");
       
        // if password is required add password field 
        if (cell.opened==false) {
             $("#wifiPassword").css("display", "block");
        }else {
            $("#wifiPassword").css("display", "none");
        }
        
        // put selected cell into object that will be used
        // in changeWifiNetwork()
        // in the case that modal is confirmed
        selectedCell = cell;

        $("#changeWifi").modal("show");
    }
}

/**
 * Send back chosen wifi network. Network has been previously chosed
 * by prepareToChange(id) function and stored in selectedCell object
 */

function changeWifiNetwork() {
    
    var changeWifi = 0;
    if (selectedCell.opened==false) {
        var password = $("#wifiPassword").val();
    
        // Checks for strings that are either empty or filled with whitespace
        if((/^\s*$/).test(password)) { 
            alert("Password field can't be empty!");
        } else {
            selectedCell.password = password;
            changeWifi = { "request": "changeWifi", "data" : selectedCell};
            console.log(changeWifi);
            wifiSocket.send(JSON.stringify(changeWifi));
        }
    
    } else {
        
        changeWifi = { "request": "changeWifi", "data" : selectedCell};
        console.log(changeWifi);
        wifiSocket.send(JSON.stringify(changeWifi));
    }
    
    selectedCell = -1; // reset selection
}


/**
 * First initialization and compilation of templates, compilation only occurs
 * once, here.
 * function update_height() is called to recalculate strip dimensions
 * it has to be recalled each time change occurs
 */

$(document).ready(function () {

    main_container_width();

    //console.log(wifi.cells.length);

    $(window).resize(function() {
        update_height();
        main_container_width();
    });
    
});

function initEditor() {
    // EDITOR ZONE
    update_height();
    compiledEditor = $('div.accordion').compile(directiveEditors);
    renderEditors();
    //insertEditors();

    collapseAllExceptFocusedOne();

    // FILE TREE SIDEBAR ZONE
    compiledTree = $('ol.tree').compile(directiveFileTree);
    renderFileTree();	
};

/**
 * JSON file, entering point for editors and tree - list of files
 */
var editorData = {editors:[], tree:[]};

/* EXAMPLE
var editorData = {
editors:[
{name:"weio_main.py", id:"0", type : "python", data : "a = 10"}
]
};
*/

/* EXAMPLE
var fileTreeData = {
tree:[
{name:"weio_main.py", id:"0", type : "python"},
{name:"index.html", id:"1", type : "html"},
{name:"test.py", id:"2", type : "python"},
{name:"new.py", id:"3", type : "python"}
]
};
*/

/**
 * Directive for templating editors with Pure JS
 */
var directiveEditors = {
    'div.accordion-group' :{
        'editor<-editors' : {
            'a.accordion-toggle' : 'editor.name',
            'a.accordion-toggle@href' : function getter(arg) {return '#'+ arg.item.id;},
            'div.accordion-body@id' : 'editor.id',
            'div.editor@id' : 'editor.name',

            // save button
            //'i.icon-download-alt@onclick' : function getter(arg) {return "save('" + arg.item.name + "')"},

            //playStopButton
            '#playStopButton@style' : function getter(arg) {return (arg.item.name == "weio_main.py") ? "display:true;" : "display:none;"},
            // close button
            'i.icon-remove@onclick' : function getter(arg) {return "saveAndClose('" + arg.item.name + "')"},

            /*
            'i.icon-remove@onclick' : function getter(arg) {return "prepareToClose('" + arg.item.name + "')"},

// modals
'h3.removeModalPhrase' : function getter(arg) {return 'Close file ?';},
'p.removeModalPhrase' : function getter(arg) {return 'Do you want to save the changes you made in the current document ?';},
'button.btn-primary@onclick' : function getter(arg) {return "saveAndClose(true)"},
'#dontSave@onclick' : function getter(arg) {return "saveAndClose(false)";}
 */
}

}
};






/**
 * Directive for templating tree with Pure JS
 */
var directiveFileTree = {
    'li.file' :{
        'file<-tree' : {
            'a@onclick' : function getter(arg) {return 'addNewStrip("' + arg.item.name + '")';},
            'a' : 'file.name',
            '#deleteFileButton@onclick' : function getter(arg) {return 'prepareToDelete("' + arg.item.name + '")';}

            //'#deleteConfirmed@onclick' : function getter(arg) {return 'deleteFile("' + arg.item.name + '")';}
        }
    }
};


/* Example for return function use in templating
'div.accordion-inner' : function makeEditorDiv(arg) {
//console.log(arg.item.name); // don't delete cos this shit is not documented
//console.log(arg.items);
return '<div class="editor" id="' + arg.item.name  + '"></div>';}
*/

/**
 * This function collapse all strips except one, that is focused. focusedOne is variable that stores
 * focused strip index in editorData.editors array
 */

function collapseAllExceptFocusedOne() {

    for (var editor in editorData.editors) {
        if (editorData.editors[editor].name!=focusedOne) {
            var name = editorData.editors[editor].id;
            $('#' + name).collapse("hide");
        } 
    }

}

/**
 * Renderer Editors
 * Call this function each time when change occurs in editors that has to be rendered
 */
function renderEditors() {
    $('div.accordion').render(editorData, compiledEditor);
}

/**
 * Renderer file tree
 * call this function each time when change occurs in tree that has to be rendered
 */
function renderFileTree() {
    $('ol.tree').render(editorData, compiledTree);
}

// // implements ace editors and dispach data inside empty strips
// 	function insertEditors() {
    // 
    // 		for (var editor in editorData.editors) {
        // 			//console.log(editorData.editors[editor].name);
        // 			var e = ace.edit(editorData.editors[editor].name); // attach to specific #id
        // 			e.setTheme("ace/theme/textmate"); // design theme
        // 			e.getSession().setMode("ace/mode/" + editorData.editors[editor].type); // editor language (html, python, css,...)
        // 			e.setValue(editorData.editors[editor].data); // code to be insered in editor
        // 			editors.push(e); // add editor to array of editors
        // 		}
        // 	}



/**
 * Implements ace editors and dispach data inside empty strips
 */
function refreshEditors() {
    saveToJSON();
    for (var editor in editors) {
        //console.log(editorData.editors[editor].name);

        var e = ace.edit(editorData.editors[editor].name); // attach to specific #id
        e.setTheme("ace/theme/tomorrow_night_eighties"); // design theme
        //e.setTheme("ace/theme/xcode"); // design theme
        e.getSession().setMode("ace/mode/" + editorData.editors[editor].type); // editor language (html, python, css,...)
        e.setValue(editorData.editors[editor].data); // code to be insered in editor
        e.setFontSize("11px");
        
        e.getSession().setTabSize(4);
        e.getSession().setUseSoftTabs(true);
        e.getSession().setUseWrapMode(true);
        e.setShowPrintMargin(false);

        e.gotoLine(editorData.editors[editor].lastLinePosition);
        editors[editor] = e;

        //editors.push(e); // add editor to array of editors
    }
}

/**
 * Takes data from editors and saves inside json object
 * Data is not send to the server by this function
 * It's local client save
 */
function saveToJSON() {

    for (var editor in editors) {
        var content = editors[editor].getValue();
        editorData.editors[editor].data = content;
        var line = editors[editor].selection.getCursor().row;
        //console.log(line);
        editorData.editors[editor].lastLinePosition = line;
    }

}


/**
 * Takes data from editors and saves them on server
 */
function backupOpenedFiles() {
    var nameList = [];

    // make list of files to be saved
    // and backup files on server
    for (var i=0; i<editorData.editors.length; i++) {
        nameList.push(editorData.editors[i].name);
        save(nameList[i]);
    }

    var storeProject = { "request": "storeProjectPreferences", "data" : nameList };
    baseFiles.send(JSON.stringify(storeProject));

}


/**
 * Saves opened file on the server
 * All opened editor files are saved localu to json structure
 */
function save(name) {
    saveToJSON();
    var rawdata = getFileDataByNameFromJson(name);
    var content = editors[rawdata.index].getValue();

    var askForFileListRequest = { "request": "saveFile", "data" : rawdata.data};
    baseFiles.send(JSON.stringify(askForFileListRequest));

}

/**
 * Save file on the server and close strip. 
 * Strip is destroyed after and new render is applied
 */
function saveAndClose(saveFile) {
    console.log("closing " + saveFile);
    
    saveToJSON(); // save only to memory

    var data = getFileDataByNameFromJson(saveFile);

    save(saveFile);

    // kill element in editor
    editors.splice(data.index, 1);

    // kill element in JSON
    editorData.editors.splice(data.index, 1);

    // render changes to HTML
    update_height();
    renderEditors();
    collapseAllExceptFocusedOne();
    refreshEditors();
        
}

/**
 * Stores file type from modal view before creation
 * Default type is html
 */
var newfileType = "html";

/**
 * Selecting file type from modal view before creation
 * default value has to be html
 */
function setFileType(ext) {
    newfileType = ext;
}

/**
 * Adds new file into server and opens it inside editor
 */
function addNewFile() {

    // add more key if needed here, like directory etc...
    var name = $("#newFileName").val();
    
    // Checks for strings that are either empty or filled with whitespace
    if((/^\s*$/).test(name)) { 
        alert("I can't make file with empty name!");
    } else {
        
        var data = {
            "name" : name + "." + newfileType
            };
    
        var askServer = { "request": "addNewFile", "data" : data};
        baseFiles.send(JSON.stringify(askServer));
    }
    
}


/**
 * Selects name of file that will be deleted
 * File is deleted only after modal view 
 * confirmation
 */
function prepareToDelete(name) {
    console.log("preparing to delete " + name);
    selectedName = name;
    $('#myModalDeleteFileLabel').html("Delete " + selectedName + " file?");
}

/**
 * Deletes file permanently from server and from local client json 
 * Normally called after modal view confirmation
 */
function deleteFile() {
    console.log("file to delete " + selectedName);
    
    var data = getFileDataByNameFromJson(selectedName);
    
    
    // kill element in editor
    editors.splice(data.index, 1);

    // kill element in JSON
    editorData.editors.splice(data.index, 1);

    // render changes to HTML
    update_height();
    renderEditors();
    collapseAllExceptFocusedOne();
    refreshEditors();
    
    var data = {
        "name" : selectedName
    };
    var askServer = { "request": "deleteFile", "data" : data};
    baseFiles.send(JSON.stringify(askServer));
    selectedName = -1;
}


/**
 * Get file contents from local json
 */
function getFileDataByNameFromJson(name) {
    var index = 0;
    for (index=0; index<editorData.editors.length; index++) {
        if (editorData.editors[index].name==name) {
            break;
        }
    }

    var data = {"data" : editorData.editors[index], "index" : index };
    return data;
}


/**
 * Inserts new strip with editor into the scene
 * Called from server response and injected to coresponding strip 
 * Setting editor caracteristics and language parameters needed
 * only once for each file
 */
function insertNewEditor(fileInfo) {

    saveToJSON();
    
    var e = ace.edit(fileInfo.name); // attach to specific #id
    e.getSession().setMode("ace/mode/" + fileInfo.type); // editor language (html, python, css,...)
    e.setValue(fileInfo.data); // code to be insered in editor
    
    
    e.gotoLine(0);
    editors.push(e); // add editor to array of editors

}
        
        
/**
 * Inserts existing editor in new strip if file is on the server
 * It asks server to send file. As server response insertNewEditor 
 * is called
 */ 

function addNewStrip(filename) {

    var newData;

    for (var file in editorData.tree) {
        if (editorData.tree[file].name==filename) {
            newData = editorData.tree[file];
            break;
        }
    }

    // check if file is already opened
    var exists = false;
    for (var editor in editorData.editors) {
        if (newData.name==editorData.editors[editor].name) {
            exists = true;
            break;
        } else {
            exists = false;
        }
    }

    // if file don't exists in the list than add it
    if (exists==false) {

        // send request to server to get raw file content
        // jump to section onmessage to see what happens

        //console.log(newData)
        var askForFileListRequest = { "request": "getFile", "data" : newData};
        baseFiles.send(JSON.stringify(askForFileListRequest));

    } 

    // in every case, put focus on that file
    focusedOne = newData.name;
    collapseAllExceptFocusedOne();


}

/**
 * Play weio_main.py standalone application
 */
function play() {
    // don't work, don't know why
    $('#playStopIcon').attr("class", "icon-stop");

    var nameList = [];
    // make list of files to be saved
    // and backup files on server
    for (var i=0; i<editorData.editors.length; i++) {
        nameList.push(editorData.editors[i].name);
        save(nameList[i]);
    }


    var askForFileListRequest = { "request": "play"};
    baseFiles.send(JSON.stringify(askForFileListRequest));
    isPlaying = true;
}

/**
 * Stop weio_main.py standalone application
 */
function stop() {
    var askForFileListRequest = { "request": "stop"};
    baseFiles.send(JSON.stringify(askForFileListRequest));
    isPlaying = false;
}

/**
 * Backup of all opened files on the server and launching of 
 * the preview screen
 */
function runPreview() {

    backupOpenedFiles();

    //console.log(nameList);

    //console.log(storeProject);
}


/**
 * Sets coresponding icon and message inside statusBar in the middle of header. 
 * Icon is string format defined in font awesome library, message is string format
 * If icon is not desired you can pass null as argument : setStatus(null, "hello world");
 *
 * Icons are only used when synchronization is active or weio_main is running
 * Set status is always activated from server push messages, never from client,
 * except when closed socket is detected!
 */
function setStatus(icon, message) {

    if (icon!=null) 
    $( "#statusBar" ).html('<p id="statusBarText"><i id="statusIcon" class="' + icon + '"></i>' + message + '</p>');
    else 
    $( "#statusBar" ).html('<p id="statusBarText">' + message + '</p>');


}

/**
 * This function clears console output
 */
function clearConsole(){
    consoleData = [];
    $('#consoleOutput').html("");
}


        //////////////////////////////////////////////////////////////// SOCK JS EDITOR


var fileList;

baseFiles.onopen = function() {
    console.log('socket opened for editor');
    var askForFileListRequest = { "request": "getFileList" };
    baseFiles.send(JSON.stringify(askForFileListRequest));
    setStatus("icon-link", "Connected");
    console.log('sending... ' + JSON.stringify(askForFileListRequest));
};

baseFiles.onmessage = function(e) {
    //console.log('Received: ' + e.data);
    
    // JSON data is parsed into object
    data = JSON.parse(e.data);

    // switch

    if ("requested" in data) {

        // this is instruction that was echoed from server + data as response
        instruction = data.requested;
        if (instruction == "getFileList") {

            fileList = data.data; 
            console.log(fileList.allFiles);

            
            editorData.tree = fileList.allFiles; 
            
            // init editors only once
            if (firstTime==true) {
                initEditor();
                // install first index.html
                addNewStrip("index.html");
                firstTime = false;
            }
            
            renderFileTree();
            

        } else if (instruction == "getFile") {

            fileInfo = data.data;

            editorData.editors.push(fileInfo);

            // render changes to HTML
            renderEditors();
            update_height();
            insertNewEditor(fileInfo);
            refreshEditors();
            collapseAllExceptFocusedOne();


        } else if (instruction == "play") {
            //std = 
            //$('#console').append(dssds);

        } else if (instruction == "storeProjectPreferences") {

            window.location.href = "/preview";


        } else if (instruction == "saveFile") {
            // nothing

        } else if (instruction == "addNewFile") {
            // We created a new file, OK now refresh file tree
            var askForFileListRequest = { "request": "getFileList" };
            baseFiles.send(JSON.stringify(askForFileListRequest));
            
        } else if (instruction == "deleteFile") {
            // We deleted one file, OK now refresh file tree
            var askForFileListRequest = { "request": "getFileList" };
            baseFiles.send(JSON.stringify(askForFileListRequest));
        }


    } else if ("serverPush" in data) {

        demand = data.serverPush;
        if (demand == "stdout") {


            stdout = data.data;
            //stdout = stdout.replace(/"/g, '');
            //stdout = stdout.replace(/\\n/g, '<BR>');
            
            
            //console.log(stdout); 
            //consoleData.push(stdout);


            ///XXX
            // DD:
            // DO THE EDITOR WRAPPING !!!
            //if (consoleData.length > MAX_LINES_IN_CONSOLE) {
            //   consoleData.shift();
            //}
           
            //consoleOutput = "";

            //for (var i=0; i<consoleData.length; i++) {
            //    consoleOutput+=consoleData[i];
            //}
            // this function outputs console to screen
            //$('#consoleOutput').html(consoleOutput);

            $('#consoleOutput').append(stdout + "<br>");

        } else if (demand == "stderr") {

            stderr = data.data;
            //stderr = stderr.replace(/"/g, '');
            stderr = stderr.replace(/\\n/g, '<BR>');
            
            console.log(stderr)
            
            consoleData.push('<font color="red">' + stderr + '</font>');
                                
            if (consoleData.length>MAX_LINES_IN_CONSOLE) {
                consoleData.shift();
            }

            consoleOutput = "";

            for (var i=0; i<consoleData.length; i++) {
                consoleOutput+=consoleData[i];
            }
            $('#consoleOutput').html(consoleOutput);

            //errorInFile = data.errorInFile;
            //errInLine = data.errInLine;
            
        } else if (demand == "stopped") {
            console.log("execution of weio_main.py stopped");
            isPlaying = false;
            
        }


    }
    
    // get Status message from server
    if ("status" in data) {
        setStatus(null, data.status);
    }

    //console.log('Received: ' + data.raw);
    //editor1.setValue(data.raw);

}

baseFiles.onclose = function() {
    console.log('socket is closed for editor');
    setStatus("icon-ban-circle", "Connection closed")

};
    
        //////////////////////////////////////////////////////////////// SOCK JS WIFI        
        
/*
 * On opening of wifi web socket ask server to scan wifi networks
 */
wifiSocket.onopen = function() {
    console.log('Wifi Web socket is opened');
    setTimeout(function(){scanWifiNetworks()},3000);
};

/*
 * Wifi web socket parser, what we got from server
 */
wifiSocket.onmessage = function(e) {
    //console.log('Received: ' + e.data);

    // JSON data is parsed into object
    data = JSON.parse(e.data);
    console.log(data);

    // switch

    if ("requested" in data) {
        // this is instruction that was echoed from server + data as response
        instruction = data.requested;
        if (instruction == "scan") {
            //console.log("gotchaaaa");
            var cellList = data.data;
            
            for (var cell in cellList) {
                if (cellList[cell].connected) {
                    $("#connectedWifiName").html('<img src="img/wifi' + getCellQuality(cellList[cell]) + '.png" id="wifiIcons"></img>' + cellList[cell].essid);
                }
                
            }
            
            wifi = cellList;
            injectWifiNetworksInDropMenu();
        }
        
    }
    
};

wifiSocket.onclose = function() {
    console.log('Wifi Web socket is closed');
};
