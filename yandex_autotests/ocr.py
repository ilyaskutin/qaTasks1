import random

from PIL import Image
from PIL import ImageChops
from PIL import ImageFilter
import pyscreenshot as ImageGrab
import os
import math
from multiprocessing import Pool as ThreadPool
from desktop import Area


class FindImage():
    def __init__(self):
        self.screen = None
        self.image = None

    def is_equal(self, im1, im2, diff=3):
        h = ImageChops.difference(im1, im2).histogram()
        sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares / float(im1.size[0] * im2.size[1]))
        if rms < diff:
            return True
        else:
            return False

    def find_image_on_lines(self, lines):
        for line in lines:
            _x = 0
            while _x + self.image.width < self.screen.width:
                _x += 1
                if self.is_equal(self.screen.crop(
                        box=(_x, line, _x + self.image.width, line + self.image.height)),
                        self.image):
                    self.screen.crop(box=(_x, line, _x + self.image.width, line + self.image.height)).save(
                        '{}/yandex_autotests/.resources/test/true.png'.format(os.getcwd()))
                    self.image.save('{}/yandex_autotests/.resources/test/equal.png'.format(os.getcwd()))
                    return True, _x, line

    def find_image_on_screen(self, path_to_etalon, screen=None, area=None, convert="1"):
        if not area:
            area = Area()
        else:
            area = Area(area[0], area[1], area[2], area[3])
        if not screen:
            screen = ImageGrab.grab(bbox=(area.x1, area.y1, area.x2, area.y2))

        if convert:
            self.screen = screen.convert(convert)
            self.image = Image.open(path_to_etalon).convert(convert)
        else:
            self.screen = screen
            self.image = Image.open(path_to_etalon)

        #self.screen = self.screen.filter(ImageFilter.DETAIL)
        #self.image = self.image.filter(ImageFilter.DETAIL)

        self.screen = self.screen.filter(ImageFilter.SHARPEN)
        self.image = self.image.filter(ImageFilter.SHARPEN)


        self.screen.save('{}/yandex_autotests/.resources/test/screen.png'.format(os.getcwd()))

        display_rows = range(self.screen.height-self.image.height)

        lines = [display_rows[i:i + int(len(display_rows) / 100)]
                 for i in
                 range(0, len(display_rows), int(len(display_rows) / 100))]

        while len(lines) > 4:
            responces = []
            random.shuffle(lines)
            for _ in range(4):
                responces.append(lines.pop())
            results = self.finding(responces)
            for res in results:
                if res:
                    return res[0], res[1]+area.x1, res[2]+area.y1
        if len(lines) > 0:
            results = self.finding(lines)
            for res in results:
                if res:
                    return res[0], res[1]+area.x1, res[2]+area.y1

        return False, 0, 0

    def finding(self, lines):
        pool = ThreadPool(4)
        results = pool.map(self.find_image_on_lines, lines)
        pool.close()
        pool.join()
        return results


if __name__ == '__main__':
    screen = ImageGrab.grab(bbox=(0, 0, 1920, 1122))
    screen.save('{}/.resources/test/screen.png'.format(os.getcwd()))
