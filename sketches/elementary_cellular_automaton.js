let tileSize = 5;

let cols;
let rows;
let grid;

let offset = 100;
let mode = "fixed";

function setup() {
    createCanvas(960, 540);

    cols = width - offset / tileSize;
    rows = height / tileSize;
    grid = newGrid();
}

function draw() {
    background(255);
    displayGrid(grid);
    grid = updateGrid(grid);
    menu();
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
            if (mode == "open") {
                gridArr[i][j] = floor(random(2));
            }

            if (mode == "fixed") {
                if (i == 0 || j == 0) {
                    gridArr[i][j] = 1;
                } else {
                    gridArr[i][j] = 0;
                }
            }
        }
    }
    return gridArr;
}

function updateGrid(grid) {
    let nextGrid = make2DArray(cols, rows);

    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            let stateA = grid[(i + 1) % cols][j];
            let stateB = grid[i][(j + 1) % rows];

            let newI = (i + 1) % cols;
            let newJ = (j + 1) % rows;

            if (mode == "fixed" && (newI == 0 || newJ == 0)) {
                continue;
            }

            if (stateA == stateB) {
                nextGrid[newI][newJ] = 0;
            } else {
                nextGrid[newI][newJ] = 1;
            }
        }
    }

    // restore fixed walls
    if (mode == "fixed") {
        for (let i = 0; i < cols; i++) {
            nextGrid[i][0] = 1;
        }
        for (let j = 0; j < rows; j++) {
            nextGrid[0][j] = 1;
        }
    }

    return nextGrid;
}

function displayGrid(grid) {
    fill(0);
    noStroke();
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            if (grid[i][j] == 1) {
                rect(i * tileSize + offset, j * tileSize, tileSize, tileSize);
            }
        }
    }
}

function menu() {
    fill(255);
    stroke(0);
    strokeWieght(5);
    for (let y = 30; y < height; y += 30) {
        rect(30, y, 40, 40);
    }
}
