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

        main_container_width();

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

    // JSON file, entering point for editors and tree - list of files
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

    // this is directive for templating editors with Pure JS
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
                'i.icon-remove@onclick' : function getter(arg) {return "prepareToClose('" + arg.item.name + "')"},

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






// this is directive for templating tree with Pure JS
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

// call this function each time when change occurs in editors that has to be rendered
function renderEditors() {
    $('div.accordion').render(editorData, compiledEditor);
}

// call this function each time when change occurs in tree that has to be rendered
function renderFileTree() {
    $('ol.tree').render(editorData, compiledTree);
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
        }
        
        // this function selects name of file that will be deleted
        function prepareToDelete(name) {
            console.log("preparing to delete " + name);
            selectedName = name;
            $('#myModalDeleteFileLabel').html("Delete " + selectedName + " file?");
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
        
        function deleteFile() {
            console.log("file to delete " + selectedName);
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
        }


        function stop() {


            var askForFileListRequest = { "request": "stop"};
            baseFiles.send(JSON.stringify(askForFileListRequest));
            isPlaying = false;
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

            //console.log(storeProject);
        }
        

        // This function sets coresponding icon and message inside statusBar in the middle of header. Icon is string format defined in font
        // awesome library, message is string format
        // If icon is not desired you can pass null as argument : setStatus(null, "hello world");
        
        // Icons are only used when synchronization is active or weio_main is running
        // set status is always activated from server push messages, never from client, except when closed socket is detected!

        function setStatus(icon, message) {

            if (icon!=null) 
            $( "#statusBar" ).html('<p id="statusBarText"><i id="statusIcon" class="' + icon + '"></i>' + message + '</p>');
            else 
            $( "#statusBar" ).html('<p id="statusBarText">' + message + '</p>');


        }
        
        // This function clears console output
        function clearConsole(){
            consoleData = [];
            $('#consoleOutput').html("");
        }


        //////////////////////////////////////////////////////////////// SOCK JS


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

                    window.location.href = "/preview";


                } else if (instruction == "saveFile") {
                    // nothing

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
