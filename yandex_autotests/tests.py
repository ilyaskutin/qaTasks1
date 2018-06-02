import time

import pytest

from desktop import get_areas
from iodev import Mouse, Keyboard
from ocr import OCR
from utils import Browser


class Base:
    def setup_class(self):
        """
        Подготовка тестового окружения. Запуск броузера если он не запущен.
        """
        browser = Browser()
        browser.browser_run(pytest.url, timeout=pytest.start_timeout)
        time.sleep(pytest.start_timeout)

        self.ocr = OCR()
        self.mouse = Mouse()
        self.keyboard = Keyboard()

    def teardown_class(self):
        """"
        Остановка тестового окружения. Закрытие браузера.
        """
        self.keyboard.press_button('alt+f4')

    def find_image(self, image_path, areas, convert='1'):
        for a in areas:
            result = self.ocr.find_image_on_screen(image_path, area=a, convert=convert)
            if result:
                return result
        return False


class TestOpenWebsite(Base):

    def test_login(self):
        """
        Первый тест. Проверяет, что по адресу yandex.ru открывается фактически данный сайт.
        """
        login_area = get_areas(pytest.main_logo_area)
        result = self.find_image(pytest.logo, login_area, convert="1")

        assert result, True


class TestAuthentication(Base):
    def test_email(self):
        """
        Второй тест. Позитивная авторизация, тестовым пользователем, на сайте yandex.ru
        """
        #  Ищу кнопку "Войти в почту"
        result = self.find_image(pytest.mail,                  # Изображение кнопки
                                 get_areas(pytest.mail_area),  # Участки экрана в которых буду искать
                                 convert="L")
        # Если кнопка "Войти в почту" нашлась, пытаюсь авторизоваться
        if result:
            self.authentication((result.x, result.y))  # Запуск аутентификации

        assert result, True

    def authentication(self, location):
        self.mouse.move(location)
        self.mouse.click()
        time.sleep(pytest.between_page_timeout)

        auth_logo_area = get_areas(pytest.auth_logo_area)
        #result = self.find_image(pytest.logo_auth, auth_logo_area, convert="1")
        #if result[0]:
        #move_cursor((result[1], result[2] + 150))
        self.keyboard.enter_text(pytest.username)
        self.keyboard.press_button('tab')
        self.keyboard.enter_text(pytest.password)
        self.keyboard.press_button('tab')
        self.keyboard.press_button('tab')
        self.keyboard.press_button('space')
        #else:
        #    assert result[0], True
        time.sleep(pytest.between_page_timeout)





