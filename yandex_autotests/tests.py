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

        self.ocr = OCR(pytest.path_to_res,
                       search_accuracy=pytest.search_accuracy,
                       debug=pytest.debug_mode)
        self.mouse = Mouse()
        self.keyboard = Keyboard()

    def teardown_class(self):
        """"
        Остановка тестового окружения. Закрытие браузера.
        """
        self.keyboard.press_button('alt+f4')

    def find_image(self, image_path, areas, convert='1'):
        result = False
        for a in areas:
            result = self.ocr.find_image_on_screen(image_path, area=a, convert=convert)
            if result:
                return result
            if pytest.debug_mode:
                print("В блоке с координатами {}, {}."
                      "Изображение не найдено, самый близкий фрагмент "
                      "с различиями {} rms".format(a[0], a[1], result.rms))
        if not result and pytest.repeat_search:
            result = self.ocr.find_image_on_screen(image_path, convert=convert)
        return result


class TestOpenWebsite(Base):
    def test_login(self):
        """
        Первый тест. Проверяет, что по адресу yandex.ru открывается фактически данный сайт.
        """
        login_area = get_areas(pytest.main_logo_area)
        result = self.find_image(pytest.logo, login_area, convert="L")
        assert result, True


class TestAuthentication(Base):
    def test_email(self):
        """
        Второй тест. Позитивная авторизация, тестовым пользователем, на сайте yandex.ru
        """
        #  Ищу кнопку "Войти в почту"
        result = self.find_image(pytest.mail,  # Изображение кнопки
                                 get_areas(pytest.mail_area),  # Участки экрана в которых буду искать
                                 convert="L")
        # Если кнопка "Войти в почту" не нашлась это ошибка
        if not result:
            assert result, True

        self.mouse.move((result.x, result.y))
        self.mouse.click()
        time.sleep(pytest.between_page_timeout)

        result = self.find_image(pytest.logo_auth,
                                 get_areas(pytest.auth_area),
                                 convert="L")
        if not result:
            assert result, True

        self.keyboard.enter_text(pytest.username)
        self.keyboard.press_button('tab')
        self.keyboard.enter_text(pytest.password)
        self.keyboard.press_button('tab')
        self.keyboard.press_button('tab')
        self.keyboard.press_button('space')
        time.sleep(pytest.between_page_timeout)

        result = self.find_image(pytest.user_login,
                                 get_areas(pytest.user_login_area),
                                 convert="L")

        assert result, True
