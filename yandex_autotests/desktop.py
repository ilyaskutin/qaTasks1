from xdo import Xdo
import unittest


class Area:
    __slots__ = ['x1', 'y1', 'x2', 'y2']

    def __init__(self, x1=None, y1=None, x2=None, y2=None):
        self.x1 = 0
        self.y1 = 0
        xdo = Xdo()
        size = xdo.get_window_size(xdo.get_active_window())
        self.x2 = size.width
        self.y2 = size.height

        if x1:
            self.x1 = x1
        if y1:
            self.y1 = y1
        if x2:
            self.x2 = x2
        if y2:
            self.y2 = y2


def get_areas(area_map):
    if len(area_map) == 0:
        return 0, 0, 0, 0

    xdo = Xdo()
    size = xdo.get_window_size(xdo.get_active_window())
    wnd_w = int(size.width / len(area_map[0]))
    wnd_h = int(size.height / len(area_map))
    result = []

    for row_n in range(len(area_map)):
        for cell_n in range(len(area_map[row_n])):
            if area_map[row_n][cell_n] == 1:
                result.append(
                    (wnd_w * cell_n, wnd_h * row_n, wnd_w * cell_n + wnd_w, wnd_h * row_n + wnd_h)
                )
    return result


if __name__ == '__main__':
    # part of the screen
    # unittest.main()

    print(get_areas((
        [0, 1, 1],
        [0, 1, 1],
        [0, 0, 0],
    )))
