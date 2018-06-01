from xdo import Xdo
import time
import random
from pynput.keyboard import Key, Controller


xdo = Xdo()
screen = xdo.get_current_desktop()


def move_cursor(location):
    # Move mouse
    while xdo.get_mouse_location().x != location[0] or xdo.get_mouse_location().y != location[1]:
        if random.randint(0, 10) > 3:
            if xdo.get_mouse_location().x == location[0]:
                continue
            move_x = 1 if (xdo.get_mouse_location().x < location[0]) else -1
            xdo.move_mouse_relative(move_x, 0)
            time.sleep(random.randint(1, 3) / 1000.0)
        else:
            if xdo.get_mouse_location().y == location[1]:
                continue
            move_y = 1 if (xdo.get_mouse_location().y < location[1]) else -1
            xdo.move_mouse_relative(0, move_y)
            time.sleep(random.randint(1, 3) / 1000.0)


def click():
    xdo.mouse_down(screen, 1)
    time.sleep(random.randint(50, 200) / 100.0)
    xdo.mouse_up(screen, 1)


def enter_text(text):
    keyboard = Controller()
    for key in text:
        keyboard.press(key)
        keyboard.release(key)

def press_tab():
    keyboard = Controller()
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)

def press_space():
    keyboard = Controller()
    keyboard.press(Key.space)
    keyboard.release(Key.space)

