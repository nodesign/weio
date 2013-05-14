//var baseFiles = new SockJS(document.URL + '/baseFiles');
//var baseFiles = new WebSocket('ws://192.168.10.183:8081/' + 'editor/baseFiles');
var baseFiles = new SockJS('http://localhost:8081/' + 'editor/baseFiles');


// Global function. Can be recalled when adding a new stripe to recalculate max height value
function update_height() {
    
    // Get windows size, get number of collapse elements and calculate maximum height to fill the column
	var viewportHeight = $(window).height();
    
	var numRows = $('.codebox').length;
	//console.log("rows : " + numRows + " array elements " + editors.length);
	var finalheight = viewportHeight - (numRows * 40) - 95;
	var widgetheight = viewportHeight - 140;
	$('.code_wrap').css('min-height', finalheight);
	$('.fullheight').css('height', widgetheight);
	
	$('#consoleAccordion').css('max-height', viewportHeight - (2 * 40) - 75);
	
}

// Global function. This calculate the main_container value depending on window size
function main_container_width() {
    
    // Get windows size, get number of collapse elements and calculate maximum height to fill the column
	var viewportWidth = $(window).width();
    
	
	//console.log("rows : " + numRows + " array elements " + editors.length);
	var finalwidth = viewportWidth - 200;
	
	$('#main_container').css('width', finalwidth);
	
}

// ace code editors are stored in this array
var editors = [];

// this is variable that selects correct index when code strips are manipulated
var selectedName = -1;

// this variable stores compiled template that can be rendered with JSON file
// to re-render just call renderTree(), compilation occurs only one inside
// ready function
var compiledTree;

// this variable stores compiled template that can be rendered with JSON file
// to re-render just call renderEditor(), compilation occurs only one inside
// ready function
var compiledEditor;

// this variable stores currentely focused strip index in editorData.editors array
var focusedOne = "weio_main.py";


// this variable informs if weio_main.py is running on Weio board
var isPlaying = false;

// this is console data array, stout and stderr
var consoleData = [];

// maximum lines in console
var MAX_LINES_IN_CONSOLE = 1000;

// first initialization and compilation of templates, compilation only occurs
// once, here.
// function update_height() is called to recalculate strip dimensions
// it has to be recalled each time change occurs

$(document).ready(function () {
	
	updatePlayStatus();
	main_container_width();
	
	$(window).resize(function() {
		update_height();
		main_container_width();
	});
});



function updatePlayStatus() {
	if (isPlaying) {
		setStatus("icon-spinner icon-spin", "Running weio_main");
	} else {
		setStatus("icon-stop", "weio_main stopped");
		window.setTimeout("setStatus(null, 'Ready')", 3000);
	}
}

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

// JSON file, entering point for editors and tree - list of files
var editorData = {editors:[], tree:[]};


// This function collapse all strips except one, that is focused. focusedOne is variable that stores
// focused strip index in editorData.editors array
function collapseAllExceptFocusedOne() {
	
	for (var editor in editorData.editors) {
		if (editorData.editors[editor].name!=focusedOne) {
			var name = editorData.editors[editor].id;
			$('#' + name).collapse("hide");
		} 
	}
	
}

// // this function implements ace editors and dispach data inside empty strips
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

function saveToJSON() {
	
	for (var editor in editors) {
		var content = editors[editor].getValue();
		editorData.editors[editor].data = content;
		var line = editors[editor].selection.getCursor().row;
		//console.log(line);
		editorData.editors[editor].lastLinePosition = line;
	}
	
}

// this function implements ace editors and dispach data inside empty strips
function refreshEditors() {
	saveToJSON();
	for (var editor in editors) {
		//console.log(editorData.editors[editor].name);
		
		var e = ace.edit(editorData.editors[editor].name); // attach to specific #id
		e.setTheme("ace/theme/textmate"); // design theme
		e.getSession().setMode("ace/mode/" + editorData.editors[editor].type); // editor language (html, python, css,...)
		e.setValue(editorData.editors[editor].data); // code to be insered in editor
		
		e.getSession().setTabSize(4);
		e.getSession().setUseSoftTabs(true);
		e.getSession().setUseWrapMode(true);
		e.setShowPrintMargin(false);
		
		e.gotoLine(editorData.editors[editor].lastLinePosition);
		editors[editor] = e;
		
		//editors.push(e); // add editor to array of editors
	}
}



function insertNewEditor(fileInfo) {
	
	saveToJSON();
	//console.log(fileInfo.name + " " + fileInfo.data);
	//console.log(editorData.editors[editor].name);
	var e = ace.edit(fileInfo.name); // attach to specific #id
	e.setTheme("ace/theme/textmate"); // design theme
	e.getSession().setMode("ace/mode/" + fileInfo.type); // editor language (html, python, css,...)
	e.setValue(fileInfo.data); // code to be insered in editor
	
	e.getSession().setTabSize(4);
	e.getSession().setUseSoftTabs(true);
	e.getSession().setUseWrapMode(true);
	e.setShowPrintMargin(false);
	
	e.gotoLine(0);
	editors.push(e); // add editor to array of editors

}

// this function selects name of editor and strip that will be used to close it
function prepareToClose(name) {
    console.log("preparing to close " + name);
	selectedName = name;
	saveAndClose(true);
	setStatus("icon-refresh icon-spin", "Sync");
}

function save(name) {
	saveToJSON();
	var rawdata = getFileDataByNameFromJson(name);
	var content = editors[rawdata.index].getValue();

	var askForFileListRequest = { "request": "saveFile", "data" : rawdata.data};
	baseFiles.send(JSON.stringify(askForFileListRequest));
	
}

// This function is called from modal view, it's role is to save file to the server and
// to close strip. Strip is destroyed and new render is necessary
function saveAndClose(saveFile) {
	console.log("closing ");
	if (selectedName!=-1) {
		
		saveToJSON(); // save only to memory
		
		var data = getFileDataByNameFromJson(selectedName);
		
		// TODO save function goes here
		if (saveFile==true) {
			save(selectedName);
		} 
		// element to kill
		
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

	selectedName = -1;
}

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
	updatePlayStatus();
	
}


function stop() {
    
    
	var askForFileListRequest = { "request": "stop"};
	baseFiles.send(JSON.stringify(askForFileListRequest));
	isPlaying = false;
	updatePlayStatus();
}

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
// this function makes backup of all opened files, saves them then lauch preview screen
function runPreview() {
    
    backupOpenedFiles();
    
    //console.log(nameList);

    // when storing is confirmed than preview will be activated
    setStatus("icon-refresh icon-spin", "Sync")
    //console.log(storeProject);
}

// This function sets coresponding icon and message inside statusBar in the middle of header. Icon is string format defined in font
// awesome library, message is string format
// If icon is not desired you can pass null as argument : setStatus(null, "hello world");

function setStatus(icon, message) {
    
    if (icon!=null) 
        $( "#statusBar" ).html('<p id="statusBarText"><i id="statusIcon" class="' + icon + '"></i>' + message + '</p>');
     else 
        $( "#statusBar" ).html('<p id="statusBarText">' + message + '</p>');
    
    
}


//////////////////////////////////////////////////////////////// SOCK JS


var fileList;

baseFiles.onopen = function() {
	console.log('socket opened for editor');
	var askForFileListRequest = { "request": "getFileList" };
	baseFiles.send(JSON.stringify(askForFileListRequest));
	setStatus("icon-link", "Connected");
	window.setTimeout("setStatus(null, 'Ready')",1000);
	console.log('sending... ' + JSON.stringify(askForFileListRequest));
};

baseFiles.onmessage = function(e) {
	//console.log('Received: ' + e.data);
	data = JSON.parse(e.data);
	
	
	// switch
	
	
	
	if ("requested" in data) {
		
		// this is instruction that was echoed from server + data as response
		instruction = data.requested;
		if (instruction == "getFileList") {
			
			fileList = data.data; 
			console.log(fileList.allFiles);
			
			
			editorData.tree = fileList.allFiles; 
			initEditor();
			
			// install first index.html
			addNewStrip("index.html");
			
			
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
            
            setStatus(null, "Ready");
            window.location.href = "/preview";
 		    

 		} else if (instruction == "saveFile") {
            if (isPlaying==false) setStatus(null, "Ready");
            
        }
 		
		
	} else if ("serverPush" in data) {
		
		demand = data.serverPush;
		if (demand == "stdout") {
			
			
			stdout = data.data;
			
			consoleData.push(stdout);
			
			if (consoleData.length>MAX_LINES_IN_CONSOLE) {
			    consoleData.shift();
			}
			
			
			consoleOutput = "";
			
			for (var i=0; i<consoleData.length; i++) {
			    consoleData[i] = consoleData[i].replace("\n", "<BR>");
			    consoleOutput+=consoleData[i];
			}
			$('#consoleOutput').html(consoleOutput);
			
			console.log(stdout);
			
			//statusBar("icon-eye-open", "Console output");
			
			
		} else if (demand == "stderr") {
			
			stderr = data.data;
			
			consoleData.push('<font color="red">' + stderr + '</font>');
			
			if (consoleData.length>MAX_LINES_IN_CONSOLE) {
			    consoleData.shift();
			}
			
			consoleOutput = "";
			
			for (var i=0; i<consoleData.length; i++) {
			    consoleData[i] = consoleData[i].replace("\n", "<BR>");
			    consoleOutput+=consoleData[i];
			}
			$('#consoleOutput').html(consoleOutput);
			
			//errorInFile = data.errorInFile;
			//errInLine = data.errInLine;
			statusBar("icon-eye-open", "Console output : Error");
			
			console.log(stderr);
		} else if (demand == "stopped") {
			console.log("execution of weio_main.py stopped");
			isPlaying = false;
			updatePlayStatus();
		}
		
		
	} 
	
	
	//console.log('Received: ' + data.raw);
	//editor1.setValue(data.raw);
	
}

baseFiles.onclose = function() {
    console.log('socket is closed for editor');
    setStatus("icon-ban-circle", "Connection closed")
        
};
