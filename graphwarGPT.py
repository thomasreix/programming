#!/usr/bin/env python3

import json
import re
import select
import subprocess

from evdev import InputDevice, ecodes, list_devices


# ============================================================
# GRAPHWAR COORDINATES
# ============================================================

GRAPH_LEFT = 14
GRAPH_RIGHT = 785

GRAPH_TOP = 14
GRAPH_BOTTOM = 465

ORIGIN_X = 400
ORIGIN_Y = 240

X_MIN = -25
X_MAX = 25

Y_MIN = -15
Y_MAX = 15


# ============================================================
# GET MOUSE POSITION
# ============================================================


def get_cursor_position():

    try:
        result = subprocess.run(
            ["hyprctl", "cursorpos", "-j"],
            capture_output=True,
            text=True,
            check=True,
        )

        data = json.loads(result.stdout)

        return (
            int(data["x"]),
            int(data["y"]),
        )

    except Exception:
        pass

    try:
        result = subprocess.run(
            ["hyprctl", "cursorpos"],
            capture_output=True,
            text=True,
            check=True,
        )

        match = re.search(
            r"(-?\d+)\s*,\s*(-?\d+)",
            result.stdout,
        )

        if match:
            return (
                int(match.group(1)),
                int(match.group(2)),
            )

    except Exception:
        pass

    raise RuntimeError("Could not get mouse position.")


# ============================================================
# SCREEN -> GRAPH
# ============================================================


def screen_to_graph(screen_x, screen_y):

    pixels_per_x = (GRAPH_RIGHT - GRAPH_LEFT) / (X_MAX - X_MIN)

    pixels_per_y = (GRAPH_BOTTOM - GRAPH_TOP) / (Y_MAX - Y_MIN)

    x = (screen_x - ORIGIN_X) / pixels_per_x

    y = (ORIGIN_Y - screen_y) / pixels_per_y

    return x, y


# ============================================================
# FORMAT NUMBER
# ============================================================


def fmt(value):

    if abs(value) < 1e-10:
        value = 0.0

    return f"{value:.8f}".rstrip("0").rstrip(".")


# ============================================================
# COPY TO CLIPBOARD
# ============================================================


def copy_text(text):

    try:
        subprocess.run(
            ["wl-copy"],
            input=text,
            text=True,
            check=True,
        )

        return True

    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
    ):
        return False


# ============================================================
# CALCULATE SLOPES
# ============================================================


def calculate_slopes(points):

    slopes = []

    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        dx = x1 - x2
        dy = y1 - y2

        if abs(dx) < 1e-10:
            raise ValueError(f"Points {i} and {i + 1} have the same X coordinate.")

        slopes.append(dy / dx)

    return slopes


# ============================================================
# BUILD FUNCTION
# ============================================================


def build_function(points):

    if len(points) < 2:
        raise ValueError("You need at least two points.")

    slopes = calculate_slopes(points)

    # A
    ax, ay = points[0]

    expression = f"({fmt(ay)})+({fmt(slopes[0])})*(x-({fmt(ax)}))"

    # B, C, D...
    for i in range(1, len(points) - 1):
        point_x, _ = points[i]

        coefficient = (slopes[i] - slopes[i - 1]) / 2

        expression += (
            f"+({fmt(coefficient)})*(abs(x-({fmt(point_x)}))+x-({fmt(point_x)}))"
        )

    return expression, slopes


# ============================================================
# GENERATE FUNCTION
# ============================================================


def generate_function(points):

    if len(points) < 2:
        return

    try:
        expression, slopes = build_function(points)

    except ValueError as error:
        print()
        print(f"ERROR: {error}")
        print()

        return

    # --------------------------------------------------------
    # POINTS
    # --------------------------------------------------------

    print()
    print("here are the points")

    for i, point in enumerate(points):
        name = chr(ord("A") + i)

        print(f"{name} = ({fmt(point[0])}, {fmt(point[1])})")

    # --------------------------------------------------------
    # SLOPES
    # --------------------------------------------------------

    print()
    print("=== slopes ===")

    for i, slope in enumerate(
        slopes,
        start=1,
    ):
        print(f"S{i} = {fmt(slope)}")

    # --------------------------------------------------------
    # FUNCTION
    # --------------------------------------------------------

    print()
    print("=== function ==")
    print()
    print(expression)
    print()

    # Copy silently.
    copy_text(expression)


# ============================================================
# FIND INPUT DEVICES
# ============================================================


def find_devices():

    mice = []
    keyboards = []

    for path in list_devices():
        try:
            device = InputDevice(path)

            capabilities = device.capabilities()

        except (
            PermissionError,
            OSError,
        ):
            continue

        keys = set(
            capabilities.get(
                ecodes.EV_KEY,
                [],
            )
        )

        # Mouse
        if ecodes.BTN_LEFT in keys:
            mice.append(device)

        # Keyboard
        keyboard_keys = {
            ecodes.KEY_LEFTSHIFT,
            ecodes.KEY_RIGHTSHIFT,
            ecodes.KEY_LEFTCTRL,
            ecodes.KEY_RIGHTCTRL,
            ecodes.KEY_LEFTALT,
            ecodes.KEY_RIGHTALT,
            ecodes.KEY_ESC,
        }

        if keys & keyboard_keys:
            keyboards.append(device)

    return mice, keyboards


# ============================================================
# MAIN
# ============================================================


def main():

    print("=== graphwar ALI ===")

    mice, keyboards = find_devices()

    if not mice:
        raise SystemExit("No mouse input device found.")

    if not keyboards:
        raise SystemExit("No keyboard input device found.")

    # --------------------------------------------------------
    # Modifier state
    # --------------------------------------------------------

    shift_down = False
    ctrl_down = False
    alt_down = False

    # --------------------------------------------------------
    # Points
    #
    # A, B, C, D...
    # --------------------------------------------------------

    points = []

    # --------------------------------------------------------
    # Devices
    # --------------------------------------------------------

    devices = []

    for mouse in mice:
        devices.append(
            (
                mouse,
                "mouse",
            )
        )

    for keyboard in keyboards:
        devices.append(
            (
                keyboard,
                "keyboard",
            )
        )

    # ========================================================
    # EVENT LOOP
    # ========================================================

    while True:
        readable, _, _ = select.select(
            [device.fd for device, _ in devices],
            [],
            [],
        )

        for fd in readable:
            device = None
            device_type = None

            for current_device, current_type in devices:
                if current_device.fd == fd:
                    device = current_device
                    device_type = current_type

                    break

            if device is None:
                continue

            try:
                events = device.read()

            except OSError:
                continue

            for event in events:
                if event.type != ecodes.EV_KEY:
                    continue

                code = event.code
                value = event.value

                # =================================================
                # KEYBOARD
                # =================================================

                if device_type == "keyboard":
                    # SHIFT
                    if code in (
                        ecodes.KEY_LEFTSHIFT,
                        ecodes.KEY_RIGHTSHIFT,
                    ):
                        shift_down = value != 0
                        continue

                    # CTRL
                    if code in (
                        ecodes.KEY_LEFTCTRL,
                        ecodes.KEY_RIGHTCTRL,
                    ):
                        ctrl_down = value != 0
                        continue

                    # ALT
                    if code in (
                        ecodes.KEY_LEFTALT,
                        ecodes.KEY_RIGHTALT,
                    ):
                        alt_down = value != 0
                        continue

                    # ESCAPE
                    if code == ecodes.KEY_ESC and value == 1:
                        for current_device, _ in devices:
                            try:
                                current_device.close()
                            except Exception:
                                pass

                        return

                # =================================================
                # MOUSE
                # =================================================

                elif device_type == "mouse":
                    if not (code == ecodes.BTN_LEFT and value == 1):
                        continue

                    # ------------------------------------------------
                    # Get mouse position.
                    # ------------------------------------------------

                    try:
                        mouse_x, mouse_y = get_cursor_position()

                    except RuntimeError:
                        continue

                    # ------------------------------------------------
                    # Convert to Graphwar coordinates.
                    #
                    # There is intentionally NO check for whether
                    # Graphwar is open.
                    # ------------------------------------------------

                    x, y = screen_to_graph(
                        mouse_x,
                        mouse_y,
                    )

                    # =================================================
                    # SHIFT + ALT + CLICK
                    # REMOVE ALL POINTS
                    # =================================================

                    if shift_down and alt_down:
                        points.clear()

                        print("all points removed")

                        continue

                    # =================================================
                    # CTRL + CLICK
                    # GENERATE
                    # =================================================

                    if ctrl_down:
                        generate_function(points)

                        continue

                    # =================================================
                    # ALT + CLICK
                    # REMOVE LAST
                    # =================================================

                    if alt_down:
                        if points:
                            removed = points.pop()

                            name = chr(ord("A") + len(points))

                            print(
                                f"removed {name} = "
                                f"({fmt(removed[0])}, "
                                f"{fmt(removed[1])})"
                            )

                        continue

                    # =================================================
                    # SHIFT + CLICK
                    # ADD
                    # =================================================

                    if shift_down:
                        points.append(
                            (
                                x,
                                y,
                            )
                        )

                        name = chr(ord("A") + len(points) - 1)

                        text = f"{name} = ({fmt(x)}, {fmt(y)})"

                        print(text)

                        # Copy A = (...), B = (...), etc.
                        copy_text(text)

                        continue


if __name__ == "__main__":
    main()
