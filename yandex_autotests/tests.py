import time

import pytest

from desktop import get_areas, Area
from iodev import move_cursor, click, enter_text, press_tab, press_space
from ocr import FindImage
from utils import is_driver, run_driver, kill_driver


def setup_module(self):
    """
    Подготовка тестового окружения. Запуск броузера если он не запущен.
    """
    if not is_driver():
        run_driver()
    time.sleep(10)

def teardown_module(self):
    """"
    Остановка тестового окружения. Остановка вебдрайвера.
    """
    kill_driver()


class TestOpenWebsite:
    def setup_class(self):
        self.ocr = FindImage()

    '''
    def test_login(self):
        """
        Первый тест. Проверяет, что по адресу yandex.ru открывается фактически данный сайт.
        :param driver: webdriver
        """
        login_area = get_areas(pytest.main_logo_area)
        result = self.find_image(pytest.logo, login_area, convert="1")

        assert result[0], True
    '''

    def test_email(self):
        """
        Второй тест. Проверяет, что по адресу yandex.ru открывается фактически данный сайт.
        :param driver: webdriver
        """
        mail_area = get_areas(pytest.mail_area)
        result = self.find_image(pytest.mail, mail_area, convert="L")
        if result[0]:
            self.authentication((result[1], result[2]))

        assert result[0], True

    def authentication(self, location):
        move_cursor(location)
        click()
        time.sleep(5)

        auth_logo_area = get_areas(pytest.auth_logo_area)
        #result = self.find_image(pytest.logo_auth, auth_logo_area, convert="1")
        #if result[0]:
        #move_cursor((result[1], result[2] + 150))
        enter_text(pytest.username)
        press_tab()
        enter_text(pytest.password)
        press_tab()
        press_tab()
        press_space()
        #else:
        #    assert result[0], True
        time.sleep(5)

    def find_image(self, image_path, areas, convert='1'):
        result = (False, 0, 0)
        for a in areas:
            result = self.ocr.find_image_on_screen(image_path, area=a, convert=convert)
            if result[0]:
                return result
        return result





