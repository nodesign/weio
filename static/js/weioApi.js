  
//var baseFiles = new SockJS(document.URL + '/baseFiles');
//var baseFiles = new WebSocket('ws://192.168.10.183:8081/' + 'editor/baseFiles');
  var weio = new SockJS('http://localhost:8081/' + 'api');


  var HIGH = "1";
  var LOW = "0";
  var OUTPUT = "out";
  var INPUT = "in";
  
  weio.onopen = function() {
      console.log('socket opened for weio API');
      
  };
  
  weio.onmessage = function(e) {
      data = JSON.parse(e.data);
      
  };
  
  weio.onclose = function() {
      console.log('socket is closed for editor');
      
  };
  
  
  function digitalWrite(pin, value) {
      var askWeio = { "request": "digitalWrite", "data" : [pin,value] };
      //	console.log(askWeio);
      weio.send(JSON.stringify(askWeio));
  };
  
  function pinMode(pin, mode) {
      var askWeio = { "request": "pinMode", "data" : [pin,mode] };
      weio.send(JSON.stringify(askWeio));
  };
