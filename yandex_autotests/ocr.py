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


class OCR:
    """
    Выполняет поиск фрагмента на изображении.
    """
    def __init__(self, path_to_resource, search_accuracy=8, debug=True):
        """
        :param path_to_resource: путь к каталогу с ресурсами
        :param search_accuracy: точность, с которой выполняется сравнение фрагментов
        :param debug: включает отключает режим дебага
        """
        self.screen = None
        self.image = None
        self.rms = []

        self.resources = path_to_resource
        self.search_accuracy = search_accuracy
        self.debug = debug

        if self.debug:
            if not os.path.exists(os.path.join(self.resources, 'debug')):
                os.mkdir(os.path.join(self.resources, 'debug'))

    def find_image_on_screen(self, path_to_etalon, screen=None, area=None, convert="1"):
        """
        :param path_to_etalon: путь к фрагменту, который требуется найти (эталон)
        :param screen: изображение на котором стоит искать (если None то сделает скриншот)
        :param area: координаты области экрана, в которой требуется искать
        :param convert: моды для конвертации 1-чб, L-градации серого и т.д.
        :return: Result
        """
        if not area:
            area = Area()
        else:
            area = Area(area[0], area[1], area[2], area[3])
        if not screen:
            screen = ImageGrab.grab(bbox=(area.x1, area.y1, area.x2, area.y2))

        self.__preparation_img(path_to_etalon, screen, convert=convert)

        if self.debug:
            name = 'screen.png'
            scr_nmb = 1
            while os.path.exists(os.path.join(self.resources, 'debug/{}'.format(name))):
                name = 'screen_{}.png'.format(scr_nmb)
                scr_nmb += 1
            self.screen.save(os.path.join(self.resources, 'debug/{}'.format(name)))

        # Набираю пакеты линий, для поиска в несколько потоков. Линии
        # набираются согласно количеству потоков=процессорных ядер.
        # lines_pack имеет формат [L1, L2 .. LN] - где N количество ядер
        # L в свою очередь это [line1, line2 ... lineС] где С это 1% от
        # всего количества линий
        for lines_pack in self.__lines_pack_for_found(self.__lines_for_found()):
            results = self.finding(lines_pack)
            for result in results:
                if result[0]:
                    return Result(
                        (result[0],
                         result[1] + area.x1 + int(self.image.width / 2),
                         result[2] + area.y1 + int(self.image.height / 2))
                    )
                else:
                    self.rms.append(result[1])

        return Result((False, min(self.rms)))

    def finding(self, lines):
        """
        Запускает поиск фрагмента в нескольких потоках
        :param lines: [L1, L2 .. LN]
        :return: [Result1, Result2 .. ResultN]
        """
        pool = ThreadPool(cpu_count())
        results = pool.map(self.find, lines)
        pool.close()
        pool.join()
        return results

    def is_equal(self, im1, im2):
        """
        Сравнивает 2 изображения
        :param im1: изображение 1
        :param im2: изображение 2
        :return: bool
        """
        h = ImageChops.difference(im1, im2).histogram()
        sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares / float(im1.size[0] * im2.size[1]))
        self.rms.append(rms)
        if rms < self.search_accuracy:
            return True
        else:
            return False

    def find(self, lines):
        """
        Непосредственно ищет фрагмент в линиях
        :param lines: [line1, line2 .. lineC]
        :return: bool, x, y
        """
        for line in lines:
            _x = 0
            while _x + self.image.width < self.screen.width:
                _x += 1
                if self.is_equal(self.screen.crop(
                        box=(_x, line, _x + self.image.width, line + self.image.height)),
                        self.image):
                    if self.debug:
                        self.screen.crop(box=(_x,
                                              line,
                                              _x + self.image.width,
                                              line + self.image.height)).save(
                            os.path.join(self.resources, 'debug/found.png'))
                        self.image.save(os.path.join(self.resources, 'debug/equal.png'))
                    return True, _x, line
        return False, min(self.rms)

    def __preparation_img(self, path_to_etalon, screen, convert=None):
        """
        Предобработки для изображений
        :param path_to_etalon: путь к фрагменту, который требуется найти
        :param screen: изображение на котором стоит искать
        :param convert: моды для конвертации
        :return:
        """
        if convert:
            self.screen = screen.convert(convert)
            self.image = Image.open(path_to_etalon).convert(convert)
            self.screen = self.screen.filter(ImageFilter.SHARPEN)
            self.image = self.image.filter(ImageFilter.SHARPEN)
            self.screen = self.screen.filter(ImageFilter.DETAIL)
            self.image = self.image.filter(ImageFilter.DETAIL)
        else:
            self.screen = screen.convert('RGBA')
            self.image = Image.open(path_to_etalon).convert('RGBA')

    def __lines_for_found(self):
        """
        Возвращает список линий разбитых по пакам в 1% от всех линий
        :return: list
        """
        display_rows = range(self.screen.height - self.image.height)

        return [display_rows[i:i + int(len(display_rows) / 100)]
                for i in
                range(0, len(display_rows), int(len(display_rows) / 100))]

    def __lines_pack_for_found(self, lines):
        """
        Генерирует паки в зависимости от количества ядер
        :param lines: линии разбитые по пакам
        :return:
        """
        while lines:
            pack = []
            # Перемешивает линии, для того что бы поиск
            # проходил не сверху вниз. Каждый новый пул потоков
            # начинает искать рандомно в разных линиях экрана
            # Так фрагмент который будет вверху экрана и внизу
            # найдутся примерно за одно время (с учетом рандома)
            random.shuffle(lines)
            if len(lines) > cpu_count():
                for _ in range(cpu_count()):
                    pack.append(lines.pop())
            else:
                for _ in range(len(lines)):
                    pack.append(lines.pop())
            yield pack


class Result:
    """Класс для инкапсуляции результатов"""
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
