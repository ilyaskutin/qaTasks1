import pytest
from PIL import Image
import os

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
        'timeout' : 20,                           # таймаут для вебдрайвера, сколько секунд ждать загрузки эл-та
        'url': 'http://www.yandex.ru',            # url сайта которые проверям
        'username': 'arrival18',                  # логин тестового пользователя
        'password': 'QWEqwe123',                  # пароль тестового пользователя

        'check_url': 'https://www.yandex.ru/',    # url сайта, который ожидаем после загрузки
        'check_title': 'Яндекс',                  # заголовок сайта, который ожидаем после

        # Ресурсы
        'logo': '{}/yandex_autotests/.resources/logo.png'.format(os.getcwd()),
        'mail': '{}/yandex_autotests/.resources/mail.png'.format(os.getcwd()),
        'logo_auth': '{}/yandex_autotests/.resources/logo_auth.png'.format(os.getcwd()),
        'login_button': '{}/yandex_autotests/.resources/login.png'.format(os.getcwd()),

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