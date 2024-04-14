let angle = 20

function setup() {
    // get browser window width and height
    windowWidth = window.innerWidth
    windowHeight = window.innerHeight
    createCanvas(windowWidth, windowHeight);
    background(33);

    // request the l-system garden from the server
    // comma delimited list of plant strings
    fetch('/get_garden').then(response => response.text()).then(data => {
        // parse the response
        plants = data.split(',');
        drawGarden(plants, windowWidth, windowHeight)
    })
}

function drawGarden(plants, width, height) {
    // draw each l-system plant in a dynamically-sized grid
    // bsaed on the number of plants and the window size
    let numPlants = plants.length;
    let numRows = Math.ceil(Math.sqrt(numPlants));
    let numCols = Math.ceil(numPlants / numRows);
    let plantWidth = width / numCols;
    let plantHeight = height / numRows;
    let x = 0;
    let y = 0;
    let padX = plantWidth / 2
    let padY = plantHeight

    for (let i = 0; i < plants.length; i++) {
        let plant = plants[i];
        console.log(plant.length)
        drawPlant(plant, x + padX, y + padY, plantWidth, plantHeight);
        x += plantWidth;
        if (x >= width) {
            x = 0;
            y += plantHeight;
        }
    }
}

function drawPlant(plant, x, y, w, h) {
    // draw the plant with p5.js
    // set the stroke color to green
    stroke(0, 255, 0)

    // set the stroke weight to 2
    strokeWeight(2)

    // length of each line segment as a fn of width and height
    let len = Math.min(w, h) / ((log(plant.length) + 1) ** 2)

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
