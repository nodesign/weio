var pinFlags = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
var activePins = [];  
var activeDigPins = []; 
var weioFunctions = ['digitalRead','digitalWrite','analogRead',
                     'pwmWrite','attachInter']; 
var aIcounter = 0;
var aIpinFlags = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

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

function callback(data){
    // increment the interrupt counter
    aIcounter = aIcounter + 1;
    // update displayed phrases
    $("#counter"+data.data).html("COUNTER: "+String(aIcounter));
    $("#pinP"+data.data).html("PIN: " + data.data);
    $("#type"+data.data).html("TYPE: " + data.eventType);
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
        var dWbutton = document.createElement('div');
        dWbutton.innerHTML = func + " pin" + pin + ": LOW";
        dWbutton.className = 'col-xs-12 col-md-6';
        dWbutton.onclick=function(){
            if( !pinFlags[pin] ) {
                digitalWrite(parseInt(pin), HIGH);
                pinFlags[pin] = 1;
                dWbutton.style.backgroundColor = "#33EE66";
                dWbutton.style.color = "black";
                dWbutton.innerHTML = func + " pin" + pin + ": HIGH";
            }
            else {
                digitalWrite(parseInt(pin), LOW);
                pinFlags[pin] = 0;
                dWbutton.style.backgroundColor = "#B0B0B0";
                dWbutton.style.color = "white";
                dWbutton.innerHTML = func + " pin" + pin + ": LOW";
            }
        };
        document.body.appendChild(dWbutton);
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
    else if(func=='attachInter'){
        
        // create div to display attach/detach button
        var aIButton = document.createElement('div');
        aIButton.className = 'col-xs-6 col-md-3';
        aIButton.innerHTML = "NO INTERRUPT ATTACHED TO PIN " + pin;
        aIButton.onclick=function(){
            // attach RISING interrupt and update displayed phrases
            if( !aIpinFlags[pin] ) {
                attachInterrupt(parseInt(pin), RISING, callback);
                aIpinFlags[pin] = 1;
                aIButton.style.backgroundColor = "#FFFF99";
                aIButton.style.color = "black";
                aIButton.innerHTML ="RISING INTERRUPT ATTACHED TO PIN "+pin;
            }
            // detach interrupt and update displayed phrases
            else {
                detachInterrupt(parseInt(pin));
                aIpinFlags[pin] = 0;
                aIButton.style.backgroundColor = "#B0B0B0";
                aIButton.style.color = "white";
                aIButton.innerHTML = "NO INTERRUPT ATTACHED TO PIN " + pin;
            }
        };
        
        // create div to display callback data
        var aI = document.createElement('div');
        aI.className = 'col-xs-6 col-md-3';
        aI.id = "aI" + pin;
        aI.style.backgroundColor = "#CC6699";
        
        // create p
        var counter = document.createElement('p');
        counter.id = "counter" + pin;
        counter.innerHTML = "COUNTER: 0";
        var pinP = document.createElement('p');
        pinP.id = "pinP" + pin;
        pinP.innerHTML = "PIN: ";
        var type = document.createElement('p');
        type.id = "type" + pin;
        type.innerHTML = "TYPE: ";
        aI.appendChild(counter);
        aI.appendChild(pinP);
        aI.appendChild(type);
        
        document.body.appendChild(aI);
        document.body.appendChild(aIButton);
    }
}