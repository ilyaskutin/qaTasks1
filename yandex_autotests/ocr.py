from PIL import Image
from PIL import ImageChops
import pyscreenshot as ImageGrab
from xdo import Xdo
import os
import math, operator
from functools import reduce


class Area:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class FindArea:
    def __init__(self, spacing=3):
        xdo = Xdo()
        self.spacing = spacing
        self.size = xdo.get_window_size(xdo.get_active_window())
        self.x1 = [int(self.size.width / spacing) * i for i in range(spacing)]
        self.x2 = [int(self.size.width / spacing) * i for i in range(1, spacing + 1)]
        self.y1 = [int(self.size.height / spacing) * i for i in range(spacing)]
        self.y2 = [int(self.size.height / spacing) * i for i in range(1, spacing + 1)]

    def get_area(self, horizontal=[], vertical=[]):
        x1, y1 = 0, 0
        x2, y2 = self.size.width, self.size.height
        if len(horizontal) == self.spacing:
            x1 = self.x1[horizontal.index(1)]
            x2 = self.x2[len(horizontal) - 1 - horizontal[::-1].index(1)]
        if len(vertical) == self.spacing:
            y1 = self.y1[vertical.index(1)]
            y2 = self.y2[len(vertical) - 1 - vertical[::-1].index(1)]

        return Area(x1, y1, x2, y2)


def diff_image(im1, im2):
    h = ImageChops.difference(im1, im2).histogram()
    sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(im1.size[0] * im2.size[1]))
    return rms


def find_image(image, area):
    _x = 0
    _y = 0
    screen = ImageGrab.grab(bbox=(area.x1, area.y1, area.x2, area.y2))
    screen.save('{}/yandex_autotests/.resources/test/screen.png'.format(os.getcwd()))
    region = screen.crop(box=(_x, _y, image.width + _x, image.height + _y))
    while region.histogram() != image.histogram():
        while image.width + _x < screen.width:
            region = screen.crop(box=(_x, _y, image.width + _x, image.height + _y))
            if diff_image(region, image) < 5:
                region.save('{}/yandex_autotests/.resources/test/{}_{}.png'.format(os.getcwd(), _x, _y))
                return True
            _x += 1
        _x = 0
        _y += 1
        if image.height + _y > screen.height:
            return False
    return True


if __name__ == '__main__':
    # part of the screen
    image = Image.open('{}/.resources/test/15_9.png'.format(os.getcwd()))
    image1 = Image.open('{}/.resources/logo.png'.format(os.getcwd()))
    print(diff_image(image1, image))
