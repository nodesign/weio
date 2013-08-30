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

            $(".editorContainer").animate( { left: closedSideBarWidth }, { queue: false, duration: 100, step:function(){$('.ace_content').css('width','100%')}  });

            $(".leftSideBar").animate( { width: closedSideBarWidth }, { queue: false, duration: 100 });
            $("#leftSideBarButton").animate( { left: "-5px"}, { queue: false, duration: 100 });
            $("#leftSideBarButton").attr("class", "closed");
            $("#leftSideBarButton i").attr("class", "icon-chevron-right");
            $(".tree").hide();
            $(".bottomButtons").hide();
            
        } else {

            $(".editorContainer").animate( { left: leftSideBarWidth }, { queue: false, duration: 100, step:function(){$('.ace_content').css('width','100%')}  });

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

            $(".editorContainer").animate( { right: closedSideBarWidth }, { queue: false, duration: 100, step:function(){$('.ace_content').css('width','100%')}  });

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
        
        }   
   
                        
    });
                  
                  
                  
    // Events for tree
      $('.tree').click(function(e){
            e.preventDefault(); 
            console.log(treeLock);
            if (!treeLock) {
                       //     console.log($(this).parents());                      
                       // prepareToDeleteFile  
                       
                      // console.log("FILE ", $(e.target).is("#deleteFileButton"));
                      // console.log("FOLDER ", $(e.target).is("#deleteProjectButton"));
                   //if ($(e.target).hasClass('icon-remove')){
                   if ($(e.target).is("#deleteFileButton")) {
                       // kill existing file
                         //  console.log($(e.target).parents('li.file'));
                           
                           var m = $(e.target).parents('li.file');
                           var path = $(m).children('a.fileTitle').attr('href');
                           
                           prepareToDeleteFile(path);
                       
                       } else if ($(e.target).is("#deleteProjectButton")) {
                       
                           prepareToDeleteProject();
                       
                       } else if ($(e.target).hasClass('fileTitle')) {
                           
                       // Path extraction                        
                       var path = $(e.target).attr('href');
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
                           treeLock = true; // LOCK TREE INTERACTION HERE
                       
                       // It's more sure to add to currentlyOpened array from
                       // websocket callback than here in case that server don't answer
                       }
                       
                   }
           }
                       
   });
                  

  // Ace editor creation
  createEditor();
  
   
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
    
    // On chage content
    $('#codeEditorAce').keyup(function(){
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

function prepareToDeleteProject() {
    $('#windowTitleDialog').modal('show');
}

function deleteFile() {
    var rq = { "request": "deleteFile", "path":toBeDeleted};
    editorSocket.send(JSON.stringify(rq));
    toBeDeleted = "";
}

function deleteProject() {
    window.top.deleteProject();
}

/*
 * These functions will be called from dashboard
 */
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

function updateError(data) {
	
	var d = data.data;
    	
	// Path extraction
	var projectName = $('.tree label[for=folder]').text();
	var splitedFile = d[(d.length-1)].file.split("/");
	console.log(splitedFile);
	var path = 'userProjects/' + projectName + '/'+splitedFile[(splitedFile.length -1)];
	
	var line = d[(d.length-1)].line
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
    console.log('error in line :',line)
    editor.focus();
    setTimeout(function(){
		editor.gotoLine(line);
		},1000)
    
}



//CALLBACKS////////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Define callbacks here and request keys
 * Each key is binded to coresponding function
 */
var callbacksEditor = {
    "getFileTreeHtml" : updateFileTree,
    "status" : updateStatus,
    //"stdout" : updateConsoleOutput,
    //"stderr" : updateConsoleError,
    //"sysConsole" : updateConsoleSys,
    "getFile": insertNewStrip,
    "saveFile": fileSaved,
    "createNewFile": refreshFiles,
    "deleteFile": fileRemoved,
    "saveAll": allFilesSaved
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
    
    $("#tree").html();
    $("#tree").html(data.data);
  
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
    var el = $('<div />').html('<div class="accordion-heading"><a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" id="att_'+ idEl+'" href="#'+'acc_'+idEl+'">'+title+'</a><div class="actions"><a role="button" id="closeButton"><i class="icon-remove"></i></a></div></div><div id="acc_'+idEl+'" class="accordion-body collapse"><div class="accordion-inner"></div></div>').addClass('accordion-group').attr("id", "file_"+data.data.id);
    
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
    var rq = { "request": "getFileTreeHtml"};
    editorSocket.send(JSON.stringify(rq));
}

function fileRemoved(data) {
    updateStatus(data);
    // refresh html filetree 
    var rq = { "request": "getFileTreeHtml"};
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


