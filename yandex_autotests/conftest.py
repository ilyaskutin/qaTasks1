import pytest
from PIL import Image
import os

RESOURCE_DIR = "{}/yandex_autotests/.resources".format(os.getcwd())

@pytest.fixture
def logo():
    """
    Фикстура подготавливает драйвер к работе
    :return: webdriver
    """
    return Image.open('{}/yandex_autotests/.resources/logo.png'.format(os.getcwd()))


def pytest_namespace():
    return {
        #Константы
        'start_timeout': 10,                      # таймаут для браузера, сколько ждать на старте
        'between_page_timeout': 5,                # таймаут при переходе между страницами
        'url': 'http://www.yandex.ru',            # url сайта которые проверям
        'username': 'arrival18',                  # логин тестового пользователя
        'password': 'QWEqwe123',                  # пароль тестового пользователя

        'check_url': 'https://www.yandex.ru/',    # url сайта, который ожидаем после загрузки
        'check_title': 'Яндекс',                  # заголовок сайта, который ожидаем после

        # Ресурсы
        'logo': os.path.join(RESOURCE_DIR, 'logo.png'),
        'mail': os.path.join(RESOURCE_DIR, 'mail.png'),
        'logo_auth': os.path.join(RESOURCE_DIR, 'logo_auth.png'),
        'login_button': os.path.join(RESOURCE_DIR, 'login.png'),

        # Арены
        "main_logo_area": (
            [1, 0, 0],
            [1, 1, 0],
            [1, 0, 0]
        ),

        "mail_area": (
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 0]
        ),

        "auth_logo_area": (
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        )
    }