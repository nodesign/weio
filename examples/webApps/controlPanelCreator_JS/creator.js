var pinFlags = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
var activePins = [];  
var activeDigPins = []; 
var weioFunctions = ['digitalRead','digitalWrite','analogRead','pwmWrite']; 

function onWeioReady() {
    setInterval(function(){getInputs()}, 500);
}

function getInputs() {
    for (var pinA in activePins) {
        analogRead(activePins[pinA], fromAdc);
    }
    for (var pinD in activeDigPins) {
        digitalRead(activeDigPins[pinD], fromDig);
    }  
} 

function fromAdc(data) {
    $("#aR"+data.pin).html("analogRead pin"+ data.pin +": "+ data.data);
}

function fromDig(data) {
    $("#dR"+data.pin).html("digitalRead pin"+ data.pin + ": "+ data.data);
}

// create button
function creator(func, pin) {
    
    // Disable pin item in all functions menus
    for (var i = 0; i < weioFunctions.length; i++) {
        $("#"+weioFunctions[i]+pin).addClass('disabled');
        $("#"+weioFunctions[i]+pin).off('click');
        $("#"+weioFunctions[i]+pin).css('background-color','#E0E0E0');
    }
    
    if(func=='digitalRead'){
        pinMode(parseInt(pin),PULL_DOWN);
        var dR = document.createElement('div');
        dR.className = 'col-xs-12 col-md-6';
        dR.id = "dR" + pin;
        dR.style.backgroundColor = "#FF6666";
        activeDigPins[activeDigPins.length] = parseInt(pin);
        document.body.appendChild(dR);
    }    
    else if(func=='analogRead'){
        var aR = document.createElement('div');
        aR.className = 'col-xs-12 col-md-6';
        aR.id = "aR" + pin;
        aR.style.backgroundColor = "#3366FF";
        activePins[activePins.length] = parseInt(pin);
        document.body.appendChild(aR);
    }
    else if(func=='digitalWrite'){
        var button = document.createElement('div');
        button.innerHTML = func + " pin" + pin + ": LOW";
        button.className = 'col-xs-12 col-md-6';
        button.onclick=function(){
            if( !pinFlags[pin] ) {
                digitalWrite(parseInt(pin), HIGH);
                pinFlags[pin] = 1;
                button.style.backgroundColor = "#33EE66";
                button.style.color = "black";
                button.innerHTML = func + " pin" + pin + ": HIGH";
            }
            else {
                digitalWrite(parseInt(pin), LOW);
                pinFlags[pin] = 0;
                button.style.backgroundColor = "black";
                button.style.color = "white";
                button.innerHTML = func + " pin" + pin + ": LOW";
            }
        };
        document.body.appendChild(button);
    }
    else if(func=='pwmWrite'){
        // create div to display duty cycle value
        var valDiv = document.createElement('div');
        valDiv.className = 'col-xs-4 col-md-2';
        valDiv.innerHTML = "PWM pin"+ pin +": 0%";
        
        // create div for range input
        var sliderDiv = document.createElement('div');
        sliderDiv.className = 'col-xs-8 col-md-4';
        
        // create range input
        var slider = document.createElement('input');
        slider.type = 'range';
        slider.value = 0;
        slider.step = 1;
        slider.oninput = function(){
            pwmWrite(parseInt(pin),parseInt(slider.value));
            valDiv.innerHTML = "PWM pin"+ pin +": "+ slider.value +"%";
        };   
        sliderDiv.appendChild(slider);
        document.body.appendChild(valDiv);
        document.body.appendChild(sliderDiv);
    }
}