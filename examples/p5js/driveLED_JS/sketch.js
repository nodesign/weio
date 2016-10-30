var cnt = 0;
var state = true;

function setup() {
    // canvas size in pixels
    createCanvas(800, 600);
    // always put some frame rate, don't make suffer cpu or websockets
    frameRate(12);
}

function draw() {
    
    background(0);
    fill(255);
    ellipse(width/2, height/2, cnt, cnt);
    
    
    if (state===true) {
        if (cnt<100) cnt+=5; else state = false;
    } else {
        if (cnt>0) cnt-=5; else state = true;
    }

    // as LEDs has common V+ it's necessary to invert signal to get good colors
    // clors are expressed in percents, floating point is permited
    pwmWrite(18,100-cnt);
    pwmWrite(19,100-cnt);
    pwmWrite(20,100-cnt);

}