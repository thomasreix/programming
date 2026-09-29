from pynput import mouse, keyboard
from pyperclip import copy as clipboard

WINDOW_TOP = 14
WINDOW_BOTTOM = 465
WINDOW_RIGHT = 785
WINDOW_LEFT = 14

ORIGIN_X = 400
ORIGIN_Y = 240

GRAPH_TOP = 15
GRAPH_BOTTOM = -15
GRAPH_RIGHT = 25
GRAPH_LEFT = -25

ADD_POINT = 0
GENERATE_FUNCTION = 1
REMOVE_POINT = 2
REMOVE_ALL_POINTS = 3


def get_inputs():
    keys = []
    inputs = [None]

    def on_press(key, injected=False):
        if key not in keys:
            keys.append(key)

    def on_release(key, injected=False):
        if key in keys:
            keys.remove(key)

    def on_click(x, y, button, pressed):
        if not pressed or button != mouse.Button.left:
            return

        shift = keyboard.Key.shift_l in keys
        ctrl = keyboard.Key.ctrl_l in keys
        alt = keyboard.Key.alt_l in keys

        if shift and alt:
            action = REMOVE_ALL_POINTS
        elif shift:
            action = ADD_POINT
        elif ctrl:
            action = GENERATE_FUNCTION
        elif alt:
            action = REMOVE_POINT
        else:
            return

        inputs[0] = (action, (x, y))

    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    mouse_listener = mouse.Listener(on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()

    return inputs


def compute_slopes(points):
    slopes = []
    points_lenth = len(points)
    for i in range(points_lenth - 1):
        dx = points[i][0] - points[i + 1][0]
        dy = points[i][1] - points[i + 1][1]
        if dx > 0:
            slope = dy / dx
        else:
            dx += 1/1000000
            slope = dy / dx
        slopes.append(slope)

    return slopes


def compute_function(points, slopes):
    function = f"({points[0][1]})+({slopes[0]})*(x-({points[0][0]}))"
    slopes_lenth = len(slopes)
    for i in range(slopes_lenth - 1):
        constant = (slopes[i+1]-slopes[i]) / 2
        function += f"+({constant})*(abs(x-({points[i+1][0]}))+x-({points[i+1][0]}))"
    return function


def point_graph(point, border):
    x, y = point

    x -= ORIGIN_X
    y -= ORIGIN_Y

    if border:
        x -= 4
        y -= 4

    x *= (GRAPH_RIGHT - GRAPH_LEFT) / (WINDOW_RIGHT - WINDOW_LEFT)
    y *= (GRAPH_TOP - GRAPH_BOTTOM) / (WINDOW_TOP - WINDOW_BOTTOM)

    return x, y


def main():
    border = False
    points = []

    inputs = get_inputs()

    print("=== graphwar ALI ===")
    points_title = True

    while True:
        if inputs[0] is None:
            continue

        action, mouse_position = inputs[0]
        inputs[0] = None

        if action == ADD_POINT:
            if points_title:
                print("\n=== points ===")
                points_title = False
            graph_point = point_graph(mouse_position, border)
            points.append(graph_point)
            points_lenth = len(points)
            print(f"[{points_lenth - 1}] = {graph_point}")

        elif action == GENERATE_FUNCTION:
            points_lenth = len(points)
            if points_lenth > 1:
                print("\n=== slopes ===")
                slopes = compute_slopes(points)
                for i in range(points_lenth - 1):
                    print(f"({i}, {i + 1}) = {slopes[i]}")

                print("\n=== function ===")
                function = compute_function(points, slopes)
                print(function)
                clipboard(function)

                points = []
                points_title = True

        elif action == REMOVE_POINT:
            if points:
                points.pop()
                print("\033[F\033[K", end="", flush=True)  # removes previous line

        elif action == REMOVE_ALL_POINTS:
            points_lenth = len(points)
            if points:
                for i in range(points_lenth):
                    print("\033[F\033[K", end="", flush=True)  # removes previous line
            points = []

if __name__ == "__main__":
    main()
