let black = "#0f0f0f";
let white = "#ffffff";

let grid;
let cols = 32;
let rows = 18;
let paused = false;
let lines = false;

let backgroundColor;
let mainColor;
let light = false;

function setup() {
    frameRate(60);
    createCanvas(960, 540);
    grid = newGrid();

    backgroundColor = black;
    mainColor = white;

    if (light) {
        backgroundColor = white;
        mainColor = black;
    }
}

function draw() {
    background(backgroundColor);
    displayGrid(grid, mainColor, lines);
    mouseInteraction();

    if (!paused) {
        grid = updateGrid(grid);
    }
}

function keyPressed() {
    if (key === "r") {
        grid = newGrid();
    }
    if (key === " ") {
        paused = !paused;
    }
    if (key === "s") {
        let tempMainColor = backgroundColor;
        backgroundColor = mainColor;
        mainColor = tempMainColor;
    }
    if (key === "l") {
        lines = !lines;
    }
    if (key === "c") {
        grid = emptyGrid();
    }
    return false;
}

function make2DArray(cols, rows) {
    let arr = new Array(cols);
    for (let i = 0; i < arr.length; i++) {
        arr[i] = new Array(rows);
    }
    return arr;
}

function newGrid() {
    let gridArr = make2DArray(cols, rows);
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            gridArr[i][j] = floor(random(2));
        }
    }
    return gridArr;
}

function displayGrid(grid, mainColor, lines) {
    fill(mainColor);
    noStroke();
    let w = width / cols;
    let h = height / rows;
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            if (grid[i][j] == 1) {
                rect(i * w, j * h, w, h);
            }
        }
    }
    if (lines) {
        drawLines(mainColor);
    }
}

function countNeighbors(grid, x, y) {
    let sum = 0;
    for (let i = -1; i < 2; i++) {
        for (let j = -1; j < 2; j++) {
            let col = (x + i + cols) % cols;
            let row = (y + j + rows) % rows;
            sum += grid[col][row];
        }
    }
    sum -= grid[x][y];
    return sum;
}

function updateGrid(grid) {
    let next = make2DArray(cols, rows);
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            let state = grid[i][j];
            let neighbors = countNeighbors(grid, i, j);

            next[i][j] = state;
            if (state == 0 && neighbors == 3) {
                next[i][j] = 1;
            } else if (state == 1 && (neighbors < 2 || neighbors > 3)) {
                next[i][j] = 0;
            }
        }
    }
    return next;
}

function emptyGrid() {
    let emptyArr = make2DArray(cols, rows);
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            emptyArr[i][j] = 0;
        }
    }
    return emptyArr;
}

function drawLines(mainColor) {
    stroke(mainColor);
    strokeWeight(1);
    let w = width / cols;
    let h = height / rows;
    for (let x = 0; x <= cols; x++) {
        line(x * w, 0, x * w, height);
    }
    for (let y = 0; y <= rows; y++) {
        line(0, y * h, width, y * h);
    }
}

function mouseInteraction() {
    if (mouseIsPressed) {
        let w = width / cols;
        let h = height / rows;

        let i = floor(mouseX / w);
        let j = floor(mouseY / h);

        if (i >= 0 && i < cols && j >= 0 && j < rows) {
            if (mouseButton === LEFT) {
                grid[i][j] = 1;
            } else if (mouseButton === RIGHT) {
                grid[i][j] = 0;
            }
        }
    }
}
