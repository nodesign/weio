var nAdcs = 8;
var pinStartNumber = 25;
var adcs = {};

function onWeioReady() {
    
    // add logo
    $(".menu").append('<li class="logo"><img src="smallLogo.png" id="logo"></img></li>');
    
    // create menu
    for (var i=0; i<nAdcs; i++) {
       $(".menu").append('<li class="txt">pin '+ String(i + pinStartNumber) + '</li>');
    }   
    
    // menu interaction, add elements
    $(".txt").click(function(){
       txt = jQuery(this).html();
       txt = txt.split("pin ")[1];
       
       if (!(txt in adcs)) {
            $(".content").append('<div class="dataViz" id="oscilo'+txt+'"><canvas id="ADC'+txt+'" class="oscilo"></canvas><p class="value" id="valueFor'+txt+'">0</p><p class="pin">pin '+txt+'</p><i class="icon-remove" id="pin'+txt+'"></i></div></div>');
            adcs[txt] = new Chart(document.getElementById("ADC"+txt).getContext("2d"));
            
           
        // Add remove handler
        // remove elements
         $(".icon-remove").click(function(){
           pin = jQuery(this).attr("id");
           pin = pin.split("pin")[1];
           delete adcs[pin];
           $("#oscilo"+pin).remove();
        });
       }
       
    });
   
   // ask server continousely for data
  setInterval(function(){askForADC()}, 100);
   
}

function askForADC() {
    
    var activePins = Object.keys(adcs);
    
    for (var pin in activePins) {
        analogRead(parseInt(activePins[pin],10), fromAdc);
    }
 
}

function fromAdc(data) {
    
    var pieData = [
    {
        value: data.data,
        color: "#000000"
    },
    {
        value : 1023-data.data,
        color : "#888"
    }
    ];
    
    var pinNumber = data.pin;
    adcs[pinNumber].Doughnut(pieData,potarDefs);
    $("#valueFor"+pinNumber).html(data.data);
}

var potarDefs = {
	//Boolean - Whether we should show a stroke on each segment
	segmentShowStroke : false,
	
	//String - The colour of each segment stroke
	segmentStrokeColor : "#333",
	
	//Number - The width of each segment stroke
	segmentStrokeWidth : 0,
	
	//The percentage of the chart that we cut out of the middle.
	percentageInnerCutout : 70,
	
	//Boolean - Whether we should animate the chart	
	animation : false,
	
	//Number - Amount of animation steps
	animationSteps : 100,
	
	//String - Animation easing effect
	animationEasing : "easeOutBounce",
	
	//Boolean - Whether we animate the rotation of the Doughnut
	animateRotate : true,

	//Boolean - Whether we animate scaling the Doughnut from the centre
	animateScale : false,
	
	//Function - Will fire on animation completion.
	onAnimationComplete : null
};