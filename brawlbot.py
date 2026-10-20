import math
import subprocess

SLOPE = -0.5
DURATION = 5000  # Milliseconds
DISTANCE = 100  # Joystick movement distance

CENTER_X = 300
CENTER_Y = 200

dx = DISTANCE / math.sqrt(1 + SLOPE**2)
dy = -SLOPE * dx  # Screen Y increases downward

subprocess.run(
    [
        "adb",
        "shell",
        "input",
        "swipe",
        str(CENTER_X),
        str(CENTER_Y),
        str(round(CENTER_X + dx)),
        str(round(CENTER_Y + dy)),
        str(DURATION),
    ],
    check=True,
)
