import random
import os
import math

from PIL import Image
from PIL import ImageChops
from PIL import ImageFilter
import pyscreenshot as ImageGrab

from multiprocessing import Pool as ThreadPool
from multiprocessing import cpu_count

from desktop import Area

DEBUG = True


class OCR:
    def __init__(self, path_to_resource=os.getcwd(), search_accuracy=8):
        self.screen = None
        self.image = None
        self.rms = []

        self.resources = path_to_resource
        self.search_accuracy = search_accuracy

    def find_image_on_screen(self, path_to_etalon, screen=None, area=None, convert="1"):
        if not area:
            area = Area()
        else:
            area = Area(area[0], area[1], area[2], area[3])
        if not screen:
            screen = ImageGrab.grab(bbox=(area.x1, area.y1, area.x2, area.y2))

        self.__preparation_img(path_to_etalon, screen, convert=convert)

        if DEBUG:
            self.screen.save('{}/debug/screen.png'.format(self.resources))

        for lines_pack in self.__lines_pack_for_found(self.__lines_for_found()):
            results = self.finding(lines_pack)
            for result in results:
                if result[0]:
                    return Result((result[0], \
                                   result[1] + area.x1 + int(self.image.width / 2), \
                                   result[2] + area.y1 + int(self.image.height / 2)))
                else:
                    self.rms.append(result[1])

        return Result((False, min(self.rms)))

    def finding(self, lines):
        pool = ThreadPool(cpu_count())
        results = pool.map(self.find, lines)
        pool.close()
        pool.join()
        return results

    def is_equal(self, im1, im2, diff=8):
        h = ImageChops.difference(im1, im2).histogram()
        sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares / float(im1.size[0] * im2.size[1]))
        self.rms.append(rms)
        if rms < diff:
            return True
        else:
            return False

    def __preparation_img(self, path_to_etalon, screen, convert=None):
        if convert:
            self.screen = screen.convert(convert)
            self.image = Image.open(path_to_etalon).convert(convert)
            self.screen = self.screen.filter(ImageFilter.SHARPEN)
            self.image = self.image.filter(ImageFilter.SHARPEN)
            self.screen = self.screen.filter(ImageFilter.DETAIL)
            self.image = self.image.filter(ImageFilter.DETAIL)
        else:
            self.screen = screen
            self.image = Image.open(path_to_etalon)

    def __lines_for_found(self):
        display_rows = range(self.screen.height - self.image.height)

        return [display_rows[i:i + int(len(display_rows) / 100)]
                for i in
                range(0, len(display_rows), int(len(display_rows) / 100))]

    def __lines_pack_for_found(self, lines):
        while lines:
            pack = []
            random.shuffle(lines)
            if len(lines) > cpu_count():
                for _ in range(cpu_count()):
                    pack.append(lines.pop())
            else:
                for _ in range(len(lines)):
                    pack.append(lines.pop())
            yield pack

    def find(self, lines):
        for line in lines:
            _x = 0
            while _x + self.image.width < self.screen.width:
                _x += 1
                if self.is_equal(self.screen.crop(
                        box=(_x, line, _x + self.image.width, line + self.image.height)),
                        self.image):
                    if DEBUG:
                        self.screen.crop(box=(_x,
                                              line,
                                              _x + self.image.width,
                                              line + self.image.height)).save(
                            '{}/debug/true.png'.format(self.resources))
                        self.image.save('{}/debug/equal.png'.format(self.resources))
                    return True, _x, line
        return False, min(self.rms)


class Result:
    __slots__ = ['x', 'y', 'rms', 'result']

    def __init__(self, result):
        if len(result) > 0:
            self.result = result[0]
        else:
            self.result = False
        if self.result:
            if len(result) > 2:
                self.x = result[1]
                self.y = result[2]
            else:
                self.result = False
        else:
            if len(result) > 1:
                self.rms = result[1]

    def __bool__(self):
        return self.result
