let angle = 30

let windowWidth = window.innerWidth * .4
let windowHeight = window.innerHeight * .5

function setup() {
    angleMode(DEGREES)
    // get browser window width and height

    let canvas = createCanvas(windowWidth, windowHeight);
    canvas.parent("plantContainer");
    // background(33);

    // request the l-system garden from the server
    // comma delimited list of plant strings
    fetch('/').then(response => response.text()).then(data => {
        // draw plant back to user
        console.log(data)
        drawPlant(data, windowWidth / 2, windowHeight / 2, windowWidth, windowHeight)
    })
}

function drawPlant(plant, x, y, w, h) {
    // draw the plant with p5.js
    // set the stroke color to green
    stroke(0, 255, 0)

    // set the stroke weight to 2
    strokeWeight(2)

    // length of each line segment as a fn of width and height
    // let len = Math.min(w, h) / ((log(plant.length) + 1) ** 2)
    let fcount = plant.match(/F/g).length
    let len = Math.min(w, h) / (log(fcount) + 1) ** 2

    push()
    
    // translate to the grid position
    translate(x, y)
    for (let i = 0; i < plant.length; i++) {
        let current = plant[i];

        switch (current) {
        case 'F':
            line(0, 0, 0, -len);
            translate(0, -len);
            break;
        case '+':
            rotate(angle);
            break;
        case '-':
            rotate(-angle);
            break;
        case '[':
            push();
            break;
        case ']':
            pop();
            break;
        default:
            break;
        }
    }

    pop()
}

function draw() {
    
}
