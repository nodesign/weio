/*
 * ACE Editor, there is only one editor that travels thru DOM space
 * It appears at good strip at good time
 * Only thing that is change is Ace Session inside editor
 */
var editor;

/*
 * Data related to files that are opened
 * name, type, data, id, path
 */
var editorsInStack = [];

/*
 * Current focused file
 * String variable that contains file path
 */
var focusedFile = null;


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

    updateConsoleHeight();

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
      scaleIt();
                                  
        
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
        
       scaleIt();
                                   

    });
                
      
   //window.setInterval("autoSave()",autoSaveInterval); 
                   
                  
  $('.accordion').click(function(e){
        
        // Remove strip                
        if ($(e.target).hasClass('icon-remove')){
            
            // Get Id from file
            var currentStrip = $($(e.target).parents('.accordion-group')).attr('id');
                        
            //var killIndex = $.inArray(currentStrip, currentlyOpened);
                        
            //currentlyOpened.splice(currentlyOpened.indexOf(currentStrip),1);
                        

            for (var i in editorsInStack) {
                        
                        if (editorsInStack[i].path == currentStrip) {
                            editorsInStack[i].data = editor.getValue();
                            saveFile(currentStrip);
                            editorsInStack.splice(i,1);
                            if (editorsInStack.length == 0) focusedFile = null;
                            //console.log(editorsInStack[i].name);
                            break;
                        }
            }
            
            // save editor in safe house before
            
            $(".safeHome").html('').append($('#codeEditorAce'));
            $(".safeHome").hide();
            
            //console.log($(e.target).parents('.accordion-group'), $(e.target).parent('.accordion-group'));
            
            $(e.target).parents('.accordion-group').remove();
            focusedFile==null;
        
        }
    });
                  

  // Ace editor creation
  createEditor();
  
    
   //console.log(window.innerHeight); 
   //console.log(editorData.editors.length);
  //window.top.setStatus(null, "Gimme some good code!");
   
}); /* end of document on ready event */



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
    
    editor.getSession().on('change', function() {
                           codeHasChanged = true;
                           var currentName = $("a.accordion-toggle").html();
                           var o = getEditorObjectFromPath(focusedFile);
                           if (o != null) {
                            if (o.name == currentName) {
                               // $("a.accordion-toggle").html(o.name+ "*");
                            }
                           }
                  
                        });
    
    editor.gotoLine(0);
}

function scaleIt(){
    var bigH = $(document).height();
    var hOthers = 0;
    
    var f = bigH - 60 - (38 * $('.accordion-group').length);
    
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

function play() {
    var rq = { "request": "play"};
    editorSocket.send(JSON.stringify(rq));
}



//EDITOR////////////////////////////////////////////////////////////////////////////////////////////////////////


/**
 * Milliseconds interval for autosave
 */
var autoSaveInterval = 4000;

/**
 * Do I have to autosave project? This is evaluated by on change event from Ace editor
 */
var codeHasChanged = false;


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

function getEditorObjectFromAccId(accId) {
    var id = accId.split("acc_");
    
    
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



/**
 * Save file on the server 
 */
function saveFile(path) {
    var obj = getEditorObjectFromPath(path);
    //console.log("SAVE " + obj.name);
    var rq = { "request": "saveFile", "data":obj};
    editorSocket.send(JSON.stringify(rq));
    
}

/**
 * Save focused file on the server 
 */
function saveFocusedFile() {
    if (focusedFile!=null) {
        var obj = getEditorObjectFromPath(focusedFile);
        //console.log("SAVE " + obj.name);
        var rq = { "request": "saveFile", "data":obj};
        editorSocket.send(JSON.stringify(rq));
    }
}


/**
 * Auto save if there were changes
 */
function autoSave() {
    if (codeHasChanged) saveFile(focusedFile);
    codeHasChanged = false;
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
            "path" : "."
            };
    
        var rq = { "request": "createNewFile", "data" : data};
        editorSocket.send(JSON.stringify(rq));
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
    editorSocket.send(JSON.stringify(rq));
    toBeDeleted = "";
}

//CALLBACKS////////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var callbacksEditor = {
    "getFileTreeHtml" : updateFileTree,
    "status" : updateStatus,
    "stdout" : updateConsoleOutput,
    "stderr" : updateConsoleError,
    "sysConsole" : updateConsoleSys,
    "getFile": insertNewStrip,
    "saveFile": fileSaved,
    "createNewFile": refreshFiles,
    "deleteFile": fileRemoved,
   
}

function fileSaved(data) {
//    var o = getEditorObjectFromPath(focusedFile);
//    var currentName = $("a.accordion-toggle").html();
//    if (currentName.indexOf(o.name)!=-1) {
      //  $("a.accordion-toggle").html(o.name);
//    }
 
    updateStatus(data);
}

/*
 * Insterts HTML code for file tree into sidebar
 * Attaches tree event listener
 */
function updateFileTree(data) {
    $("#tree").html(data.data);
    
    // Events for tree
    
    $('.tree').click(function(e){
                              //     console.log($(this).parents());                      
                                   // prepareToDeleteFile  
                     
         if ($(e.target).hasClass('icon-remove')){
                     // kill existing file
                     
                     
                     console.log("GORCHAAA");
         } else if ($(e.target).hasClass('fileTitle')) {
                            
               // Path extraction                        
               var path = $(e.target).attr('id');
               //console.log(path);
                
               var doesExist = false;
                                       
               // Adding strip if don't exists already
               for (var i in editorsInStack) {
               
               if (editorsInStack[i].path == path) {
                           doesExist = true;
                    }
               }

               if (!doesExist){
                                       
                   // asks server to retreive file that we are intested in
                   var rq = { "request": "getFile", "data":path};
                   editorSocket.send(JSON.stringify(rq));
                                       
                   // It's more sure to add to currentlyOpened array from
                   // websocket callback than here in case that server don't answer
               }
      
        }
                                   
    });
//    
//
//    
//    
//    $('.tree li.file a.fileTitle').click(function(){
//       
//       // Where we clicked?                       
//       var idEl = $('.tree a.fileTitle').toArray().indexOf(this);
//       
//       // Path extraction                        
//       var path = $(this).attr('id');
//        
//       
//       var doesExist = false;
//                               
//       // Adding strip if don't exists already
//       for (var i in editorsInStack) {
//       
//       if (editorsInStack[i].path == path) {
//                   doesExist = true;
//            }
//       }
//
//       if (!doesExist){
//                               
//           // asks server to retreive file that we are intested in
//           var rq = { "request": "getFile", "data":path};
//           editorSocket.send(JSON.stringify(rq));
//                               
//           // It's more sure to add to currentlyOpened array from
//           // websocket callback than here in case that server don't answer
//       }
//   });
//    
    
    
       
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
                                                                      var o = getEditorObjectFromAccId(acc_id);
                                                                          //console.log("MMM ", $($(this).parents('.accordion-body')));
                                                                      //   console.log("DATA " , o);
                                                                      if (o!=null) {
                                                                          editor.setValue(o.data);
                                                                          editor.getSession().setMode("ace/mode/"+ o.type);
                                                                          
                                                                          editor.gotoLine(0);
                                                                          focusedFile = o.path;
                                                                      }
                                                                           
                                                                          //console.log("SHOW");
                                                                      
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
                                   
                                   //console.log("GGGGGGGG ", $(this).parent().attr('id'));
                                   var o = getEditorObjectFromPath(path);

                                   if (o != null) {
                                    o.data = editor.getValue();
                                    setEditorObjectToPath(path, o);
                                    saveFile(path);
                                   }
                                   $('#codeEditorAce').appendTo($(showMe).find('.accordion-inner'));
                                   scaleIt();
                                   $(showMe).find('.accordion-inner').animate({opacity:1},300,'linear');
                                  
                                   //console.log("HIDE");
                                    })

    
    // Showing accordion
    $(showMe).find('.collapse').collapse('show');
}

/**
 * Inserts existing editor in new strip if file is on the server
 */ 

function insertNewStrip(data) {

    var e = {};
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
    var el = $('<div />').html('<div class="accordion-heading"><a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#'+'acc_'+idEl+'">'+title+'</a><div class="actions"><a role="button" id="closeButton"><i class="icon-remove"></i></a></div></div><div id="acc_'+idEl+'" class="accordion-body collapse"><div class="accordion-inner"></div></div>').addClass('accordion-group').attr("id", data.data.path);
    
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
    
    // Update height
    scaleIt();
     
}


function updateStatus(data) {
//    console.log(data);
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



function refreshFiles(data) {
    updateStatus(data);
    // refresh html filetree 
    var rq = { "request": "getFileTreeHtml"};
    editorSocket.send(JSON.stringify(rq));
}

function fileRemoved(data) {
    updateStatus(data);
    // refresh html filetree 
    var rq = { "request": "getFileTreeHtml"};
    editorSocket.send(JSON.stringify(rq));
    
    // delete strip if opened
//    filename = data.path;
//    fileId = 0;
//    // check if file is already opened
//    var exists = false;
//    for (var editor in editorData.editors) {
//        if (filename==editorData.editors[editor].path) {
//            exists = true;
//            fileId = editorData.editors[editor].id;
//            break;
//        } else {
//            exists = false;
//        }
//    }
//    
//    if (exists==true) {
//        
//        for (var editor in editorData.editors) {
//            if (editorData.editors[editor].id==fileId) {
//                // kill element in JSON
//                editorData.editors.splice(editor, 1);
//                break;
//            }
//        }
//        
//        renderEditors();
//        refreshEditors();
//        updateEditorHeight();
//    } 
}


//////////////////////////////////////////////////////////////// SOCK JS DASHBOARD        
     
/*
 * SockJS object, Web socket
 */
var editorSocket = new SockJS('http://' + location.host + '/editor/editorSocket');
/*
 * On opening of wifi web socket ask server to scan wifi networks
 */
editorSocket.onopen = function() {
    console.log('editor Web socket is opened');
    // get files
    var rq = { "request": "getFileTreeHtml"};
    editorSocket.send(JSON.stringify(rq));
    
    var rq = { "request": "getPlatform"};
    editorSocket.send(JSON.stringify(rq));
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


