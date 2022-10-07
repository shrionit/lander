from .utils import Dict
import glfw as g
mouse = Dict({"x": 0, "y": 0, "dx": 0, "dy": 0, "scrollY": 0})
keyboard = [False] * 349
mousebuttons = [False] * 12
keyboard_events = [lambda: None] * 349
mousebutton_events = [lambda: None] * 12

KEYS = Dict()
KEYS.UP = g.KEY_UP
KEYS.DOWN = g.KEY_DOWN
KEYS.LEFT = g.KEY_LEFT
KEYS.RIGHT = g.KEY_RIGHT
KEYS.W = g.KEY_W
KEYS.A = g.KEY_A
KEYS.S = g.KEY_S
KEYS.D = g.KEY_D
KEYS.LEFT_CTRL = g.KEY_LEFT_CONTROL
KEYS.RIGHT_CTRL = g.KEY_RIGHT_CONTROL
KEYS.LEFT_SHIFT = g.KEY_LEFT_SHIFT
KEYS.RIGHT_SHIFT = g.KEY_RIGHT_SHIFT
KEYS.LEFT_ALT = g.KEY_LEFT_ALT
KEYS.RIGHT_ALT = g.KEY_RIGHT_ALT
KEYS.SPACE = g.KEY_SPACE


def clear_mouse():
    mouse.dx = 0
    mouse.dy = 0
    mouse.scrollY = 0

is_key_pressed = lambda key: keyboard[key]
is_key_released = lambda key: not keyboard[key]
is_mouse_pressed = lambda key: mousebuttons[key]

def mouse_handler(_, x, y):
    mouse.dx = x - mouse.x
    mouse.dy = y - mouse.y
    mouse.x = x
    mouse.y = y


def keyboard_handler(_, key, scancode, action, mods):
    keyboard[key] = action >= g.PRESS
    if keyboard[key]:
        keyboard_events[key]()

def mouse_button_handler(_, key, action, mods):
    mousebuttons[key] = action >= g.PRESS
    if mousebuttons[key]:
        mousebutton_events[key]()

def set_on_key(key, cb):
    if type(cb).__name__ == "function":
        if is_key_pressed(key)==g.PRESS:
            keyboard_events[key] = cb

def set_on_mouse_key(key, cb):
    if type(cb).__name__ == "function":
        if is_mouse_pressed(key)==g.PRESS:
            mousebutton_events[key] = cb

def on_scroll(window, hScroll, vScroll):
    mouse.scrollY += vScroll
