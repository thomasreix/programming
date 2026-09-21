const button = document.getElementById("button");
const display = document.getElementById("display");
const lapses = document.getElementById("lapses");
const minutesInput = document.getElementById("minutes");
const secondsInput = document.getElementById("seconds");

let timer = null;
let lapsesCount = 0;
let isRunning = false;
let audioCtx = null;


function playBeep() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }

  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();

  osc.type = "sine";
  osc.frequency.setValueAtTime(880, audioCtx.currentTime);

  gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
  
  osc.connect(gain);
  gain.connect(audioCtx.destination);

  osc.start();
  osc.stop(audioCtx.currentTime + 0.25);
}


function updateDisplay(totalSeconds) {
  let minutes = minutesInput.value || 0;
  let seconds = secondsInput.value || 0;
  display.innerText = minutes + "m " + seconds + "s";
}

if (!isRunning) {
  minutesInput.oninput = updateDisplay();
  secondsInput.oninput = updateDisplay;
}

button.onclick = function () {
  if (!isRunning) {
    let timeSeconds =
      (parseInt(minutesInput.value) || 0) * 60 +
      (parseInt(secondsInput.value) || 0);

    isRunning = true;
    let totalSeconds = timeSeconds;

    button.innerText = "reset";
    button.classList.add("reset-mode");
    updateDisplay();

    timer = setInterval(function () {
      if (totalSeconds > 1) {
        totalSeconds--;

        let m = Math.floor(totalSeconds / 60);
        let s = totalSeconds % 60;
        display.innerText = m + "m " + s + "s";
      } else {
        playBeep();
        totalSeconds = timeSeconds;
        lapsesCount++;
        lapses.innerText = lapsesCount;
        updateDisplay();
      }
    }, 1000);
  } else {
    clearInterval(timer);
    isRunning = false;
    button.innerText = "start";
    button.classList.remove("reset-mode");
    lapsesCount = 0;
    lapses.innerText = lapsesCount;
    updateDisplay();
  }
};
