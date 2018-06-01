import time

import pytest
from utils import is_driver, run_driver, kill_driver

from yandex_autotests.ocr import find_image, FindArea


def setup_module(self):
    """
    Подготовка тестового окружения. Запуск броузера если он не запущен.
    """
    if not is_driver():
        run_driver()

def teardown_module(self):
    """"
    Остановка тестового окружения. Остановка вебдрайвера.
    """
    kill_driver()


class TestOpenWebsite:
    def setup_class(self):
        self.desktop = FindArea()

    @pytest.mark.usefixtures("logo")
    def test_login(self, logo):
        """
        Первый тест. Проверяет, что по адресу yandex.ru открывается фактически данный сайт.
        :param driver: webdriver
        """
        time.sleep(10)
        assert True == find_image(logo, self.desktop.get_area([1, 0, 0], [0, 1, 1]))
        #(115,430,250,520)
        #assert pytest.check_title == driver.title
        #assert pytest.check_url == driver.current_url
