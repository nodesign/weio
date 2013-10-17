function onWeioReady() {
    var myName = getMyUuid();
    data = {};
    data.info = "hello to myself";
    talkTo(myName, data);
}

function onMyInbox(data) {
    console.log("Received from ", data.from);
    console.log("Contents ", data.data);
}