/**
 * JSON file, entering point for editors and tree - list of files
 */
var editorData = {editors:[]};

/* EXAMPLE
var editorData = {
editors:[
{name:"weioMain.py", id:"0", type : "python", data : "a = 10"}
]
};
*/

/*
 * When all DOM elements are fully loaded
 */
$(document).ready(function () {
    
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


    $("#leftSideBarButton").click(function(){

        if ($(this).is(".opened")) {

            $(".editorContainer").animate( { left: closedSideBarWidth }, { queue: false, duration: 100 });

            $(".leftSideBar").animate( { width: closedSideBarWidth }, { queue: false, duration: 100 });
            $("#leftSideBarButton").animate( { left: "-5px"}, { queue: false, duration: 100 });
            $("#leftSideBarButton").attr("class", "closed");
            $("#leftSideBarButton i").attr("class", "icon-chevron-right");
            $(".tree").hide();
            $(".bottomButtons").hide();

        } else {

            $(".editorContainer").animate( { left: leftSideBarWidth }, { queue: false, duration: 100 });

            $(".leftSideBar").animate( { width: leftSideBarWidth }, { queue: false, duration: 100 });
            $("#leftSideBarButton").animate( { left: "177px"}, { queue: false, duration: 100 });
            $("#leftSideBarButton").attr("class", "opened");
            $("#leftSideBarButton i").attr("class", "icon-chevron-left");
            $(".tree").show();
            $(".bottomButtons").show();

        }

    });

    $("#rightSideBarButton").click(function(){

        if ($(this).is(".opened")) {

            $(".editorContainer").animate( { right: closedSideBarWidth }, { queue: false, duration: 100 });

            $(".rightSideBar").animate( { width: closedSideBarWidth }, { queue: false, duration: 100 });
            $("#rightSideBarButton").animate( { left: "-5px"}, { queue: false, duration: 100 });
            $("#rightSideBarButton").attr("class", "closed");
            $("#rightSideBarButton i").attr("class", "icon-chevron-left");
            $("#trashConsole").hide();


        } else {

            $(".editorContainer").animate( { right: rightSideBarWidth }, { queue: false, duration: 100 });

            $(".rightSideBar").animate( { width: rightSideBarWidth }, { queue: false, duration: 100 });
            $("#rightSideBarButton").animate( { left: "0px"}, { queue: false, duration: 100 });
            $("#rightSideBarButton").attr("class", "opened");
            $("#rightSideBarButton i").attr("class", "icon-chevron-right");
            $("#trashConsole").show();

        }


    });
                
   initEditor();
   updateConsoleHeight();
 
   
   //console.log(window.innerHeight); 
   //console.log(editorData.editors.length);
  //window.top.setStatus(null, "Gimme some good code!");
   
}); /* end of document on ready event */

$(window).resize(function() {
   updateEditorHeight();
   updateConsoleHeight();
});


/**
 * Can be recalled when adding a new stripe to recalculate max height value
 */
function updateEditorHeight() {

    // Get windows size, get number of collapse elements and calculate maximum height to fill the column
    var viewportHeight = $(window).height();

    var numRows = $('.codebox').length;
    var finalheight = viewportHeight - (numRows  * 40) - (numRows * 15) - 15;
    $('.code_wrap').css('min-height', finalheight);
    console.log("rows : " + numRows + " array elements " + viewportHeight + " viewport height " + finalheight + " calculated height");
    // $('.fullheight').css('height', widgetheight);
    // $('#consoleAccordion').css('max-height', viewportHeight - (2  * 40) - 75);
}

function updateConsoleHeight() {
    var viewportHeight = $(window).height();
    $("#consoleOutput").css("height", viewportHeight-60);
}



/**
 * Renderer Editors
 * Call this function each time when change occurs in editors that has to be rendered
 */
function renderEditors() {
    $('div.accordion').render(editorData, compiledEditor);
}



//EDITOR////////////////////////////////////////////////////////////////////////////////////////////////////////


/**
 * Stores compiled template that can be rendered with JSON file
 * to re-render just call renderEditor(), compilation occurs only one inside
 * ready function
 */
var compiledEditor;

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
            // '#playStopButton@style' : function getter(arg) {return (arg.item.name == "weioMain.py") ? "display:true;" : "display:none;"},
            // close button
            'i.icon-remove@onclick' : function getter(arg) {return "saveAndClose('" + arg.item.id + "')"},

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


function clearConsole() {
    $('#consoleOutput').empty();
}

function initEditor() {
    // EDITOR ZONE
    updateEditorHeight();
    compiledEditor = $('div.accordion').compile(directiveEditors);
    renderEditors();
    //insertEditors();

    // collapseAllExceptFocusedOne();

    // FILE TREE SIDEBAR ZONE
    // compiledTree = $('ol.tree').compile(directiveFileTree);
    // renderFileTree();    
}

/**
 * Inserts existing editor in new strip if file is on the server
 * It asks server to send file. As server response insertNewEditor 
 * is called
 */ 

function addNewEditorStrip(filename) {

    // check if file is already opened
    var exists = false;
    for (var editor in editorData.editors) {
        if (filename==editorData.editors[editor].path) {
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
        var rq = { "request": "getFile", "data":filename};
        dashboard.send(JSON.stringify(rq));
    } 

    // in every case, put focus on that file
    //    focusedOne = newData.name;
    //    collapseAllExceptFocusedOne();
}


/**
 * Collapse all strips except one, that is focused. focusedOne is variable that stores
 * focused strip index in editorData.editors array
 */

function collapseAllExceptFocusedOne(id) {

    for (var editor in editorData.editors) {
        if (editorData.editors[editor].name!=id) {
            var name = editorData.editors[editor].name;
            $('#' + name).collapse("hide");
        } 
    }

}

/**
 * Save file on the server and close strip. 
 * Strip is destroyed after and new render is applied
 */
function saveAndClose(id) {
    
    var file = {};
    
    for (var editor in editorData.editors) {
        if (editorData.editors[editor].id==id) {
            var obj = editorData.editors[editor];
            file.data = obj.editorJs.getValue();
            file.name = obj.name;
            file.path = obj.path;
            
            // kill element in JSON
            editorData.editors.splice(editor, 1);
            break;
        }
    }
    console.log(file);
    var rq = { "request": "saveFile", "data":file};
    dashboard.send(JSON.stringify(rq));
    
    refreshEditors();
}

/**
 * Save all opened files on the server. This is used 
 * when launching play or passing to preview mode
 */
function saveAll() {
    
    var file = {};
    
    for (var editor in editorData.editors) {
        
        var obj = editorData.editors[editor];
        file.data = obj.editorJs.getValue();
        file.name = obj.name;
        file.path = obj.path;
        
        var rq = { "request": "saveFile", "data":file};
        dashboard.send(JSON.stringify(rq));
    }
}



function refreshEditors() {
    renderEditors();
    for (var i=0; i<editorData.editors.length;i++) {

        var editor = ace.edit(editorData.editors[i].name);
        editor.setTheme("ace/theme/dawn");
        editor.getSession().setMode("ace/mode/" + editorData.editors[i].type);
        editor.setValue(editorData.editors[i].data, 0);

        editor.getSession().setTabSize(4);
        editor.getSession().setUseSoftTabs(true);
        editor.getSession().setUseWrapMode(true);
        editor.setShowPrintMargin(false);
        
        editorData.editors[i]["editorJs"] = editor;
    }
    updateEditorHeight();
    
}

/*
 * MODAL CREATE NEW FILE
 */
 
/**
 * Stores file type from modal view before creation
 * Default type is html
 */
var newfileType = ".html"; // default value if nothing selected

/**
 * Selecting file type from modal view before creation
 * default value has to be html
 */
function setFileType(type) {
    newfileType = type;
    //console.log("file " + type);
    newfileType = ".html";
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
            "path" : "."
            };
    
        var rq = { "request": "createNewFile", "data" : data};
        dashboard.send(JSON.stringify(rq));
    }
    
}


var toBeDeleted = ""; // filename to be deleted
function prepareToDeleteFile(filename) {
    $("#myModalDeleteFileLabel").html("Delete " + filename + "?");
    $('#deleteFile').modal('show');
    toBeDeleted = filename;
}

function deleteFile() {
    var rq = { "request": "deleteFile", "path":toBeDeleted};
    dashboard.send(JSON.stringify(rq));
    toBeDeleted = "";
}

//CALLBACKS////////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var callbacks = {
    "getFileTreeHtml" : updateFileTree,
    "status" : updateStatus,
    "stdout" : updateConsoleOutput,
    "stderr" : updateConsoleError,
    "sysConsole" : updateConsoleSys,
    "getFile": insertNewStrip,
    "saveFile": updateStatus,
    "createNewFile": refreshFiles,
    "deleteFile": fileRemoved,
   
}

/*
 * Insterts HTML code for file tree into sidebar
 */
function updateFileTree(data) {
    $("#tree").html(data.data);
}

function updateStatus(data) {
    window.top.setStatus(null, data.status);
}

function updateConsoleOutput(data) {
    var stdout = data.data;
    $('#consoleOutput').append(stdout + "<br>");
}

function updateConsoleError(data) {
    var stderr = data.data;
    $('#consoleOutput').append("<a id='stderr'>" + stderr + "<br></a>");
}

function updateConsoleSys(data) {
    var sys = data.data;
    $('#consoleOutput').append("<a id='sys'>" + sys + "<br></a>");
}

function insertNewStrip(data) {

    // it has been already checked if this file already exists
    // so just insert it straight

    fileInfo = data.data;
    editorData.editors.push(fileInfo);
    
    refreshEditors();
    
    //console.log = (editorData);
    
    $('#' + fileInfo.id).collapse("show");
    $('#' + fileInfo.id).css("height", "100%");

}

function refreshFiles(data) {
    updateStatus(data);
    // refresh html filetree 
    var rq = { "request": "getFileTreeHtml"};
    dashboard.send(JSON.stringify(rq));
}

function fileRemoved(data) {
    updateStatus(data);
    // refresh html filetree 
    var rq = { "request": "getFileTreeHtml"};
    dashboard.send(JSON.stringify(rq));
}


//////////////////////////////////////////////////////////////// SOCK JS DASHBOARD        
     
/*
 * SockJS object, Web socket
 */
var dashboard = new SockJS('http://' + location.host + '/dashboard');
/*
 * On opening of wifi web socket ask server to scan wifi networks
 */
dashboard.onopen = function() {
    console.log('editor Web socket is opened');
    // get files
    var rq = { "request": "getFileTreeHtml"};
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

    // switch
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
    
};


