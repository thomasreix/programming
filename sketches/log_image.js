let img;
let mappedPixels = [];
let pixelSize = 1;
let cols, rows;

let tile = true;
let rotationAngle = Math.atan(9 / 16);
let pg;

function preload() {
    img = loadImage("../assets/pi_zoom.png");
}

function setup() {
    createCanvas(960, 540);
    img.resize(width, height);

    cols = floor(width / pixelSize);
    rows = floor(height / pixelSize);

    for (let i = 0; i < cols; i++) {
        mappedPixels[i] = [];
        for (let j = 0; j < rows; j++) {
            let x = (i / cols) * Math.log(dist(0, 0, width / 2, height / 2));
            let y = (j / rows) * TWO_PI;
            let r = Math.exp(x);

            let imageX = width / 2 + r * Math.cos(y);
            let imageY = height / 2 + r * Math.sin(y);

            mappedPixels[i][j] = img.get(imageX, imageY);
        }
    }

    pg = createGraphics(width, height);
    pg.background(0);
    pg.noStroke();

    if (!tile) {
        drawMappedImage(pg, 0, 0, 1);
    } else {
        let incrementX = width / 2 - width / Math.PI;
        for (
            let imgX = width / 2 + incrementX;
            imgX > -width / 2;
            imgX -= incrementX
        ) {
            for (let imgY = 0; imgY < height; imgY += height / 2) {
                drawMappedImage(pg, imgX, imgY, 2);
            }
        }
    }

    noLoop();
}

function draw() {
    background(0);

    push();
    translate(width / 2, height / 2);
    rotate(rotationAngle);
    imageMode(CENTER);
    image(pg, 0, 0);
    pop();
}

function drawMappedImage(target, imgX, imgY, k) {
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            let x = (i * pixelSize) / k;
            let y = (j * pixelSize) / k;
            target.fill(mappedPixels[i][j]);
            target.rect(x + imgX, y + imgY, pixelSize / k, pixelSize / k);
        }
    }
}
2;
