from pynput import mouse, keyboard

shift = False
ctrl = False
alt = False


def on_key_press(key):
    global shift, ctrl, alt

    if key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
        shift = True
    elif key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl = True
    elif key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
        alt = True


def on_key_release(key):
    global shift, ctrl, alt

    if key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
        shift = False
    elif key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl = False
    elif key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
        alt = False


def on_click(x, y, button, pressed):
    if not pressed or button != mouse.Button.left:
        return

    if shift and alt:
        print("all points removed")

    elif shift:
        print(f"A = ({x}, {y})")

    elif ctrl:
        print("generate function")

    elif alt:
        print("point removed")


mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)

mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()
mouse_listener.stop()
