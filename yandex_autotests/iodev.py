from xdo import Xdo
import time
import random
from pynput.keyboard import Key, Controller


class Mouse:
    def __init__(self):
        self.xdo = Xdo()
        self.screen = self.xdo.get_current_desktop()

    def move(self, location):
        # Move mouse
        while self.xdo.get_mouse_location().x != location[0] or self.xdo.get_mouse_location().y != location[1]:
            if random.randint(0, 10) > 3:
                if self.xdo.get_mouse_location().x == location[0]:
                    continue
                move_x = 1 if (self.xdo.get_mouse_location().x < location[0]) else -1
                self.xdo.move_mouse_relative(move_x, 0)
                time.sleep(int(random.randint(1, 3) / 1500.0))
            else:
                if self.xdo.get_mouse_location().y == location[1]:
                    continue
                move_y = 1 if (self.xdo.get_mouse_location().y < location[1]) else -1
                self.xdo.move_mouse_relative(0, move_y)
                time.sleep(int(random.randint(1, 3) / 1500.0))

    def click(self):
        self.xdo.mouse_down(self.screen, 1)
        time.sleep(int(random.randint(50, 200) / 500.0))
        self.xdo.mouse_up(self.screen, 1)


class Keyboard:
    def __init__(self):
        self.keyboard = Controller()

    def enter_text(self, text):
        for key in text:
            self.keyboard.press(key)
            self.keyboard.release(key)

    def press_button(self, key):
        keys = key.split("+")
        for k in keys:
            if k in dir(Key):
                self.keyboard.press(Key[k])
        for k in keys:
            if k in dir(Key):
                self.keyboard.release(Key[k])