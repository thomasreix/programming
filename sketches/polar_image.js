let img;
let pixels = [];
let pixelSize = 1;
let cols, rows;

function preload() {
    img = loadImage("../assets/grid.png");
}

function setup() {
    createCanvas(960, 540);
    img.resize(width, height);

    cols = width / pixelSize;
    rows = height / pixelSize;

    for (let i = 0; i < cols; i++) {
        pixels[i] = [];
        for (let j = 0; j < rows; j++) {
            let x = (i / cols) * dist(0, 0, width / 2, height / 2);
            let y = (j / rows) * TWO_PI;

            let imageX = width / 2 + x * cos(y);
            let imageY = height / 2 + x * sin(y);

            pixels[i][j] = img.get(imageX, imageY);
        }
    }
}

function draw() {
    background(0);
    noStroke();
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            let x = i * pixelSize;
            let y = j * pixelSize;
            fill(pixels[i][j]);
            rect(x, y, pixelSize, pixelSize);
        }
    }
}
