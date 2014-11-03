function onWeioReady() {
 console.log("WeIO is loaded!");
 
 // Define callback that will execute when "refreshImage" is received
 weioCallbacks.refreshImage = refreshWebCam;
}

function refreshWebCam(data) {
    $("#webCam").attr("background", data.data);
    console.log(data.data);
}