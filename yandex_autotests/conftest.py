import pytest
import os

RESOURCE_DIR = os.path.join(os.getcwd(), "yandex_autotests/.resources")


def pytest_namespace():
    return {
        #Константы
        'start_timeout': 10,                      # таймаут для браузера, сколько ждать на старте
        'between_page_timeout': 5,                # таймаут при переходе между страницами
        'url': 'http://www.yandex.ru',            # url сайта которые проверям
        'username': 'arrival18',                  # логин тестового пользователя
        'password': 'QWEqwe123',                  # пароль тестового пользователя

        'search_accuracy': 10,                     # точность, с которой будет производится поиск
        'check_url': 'https://www.yandex.ru/',    # url сайта, который ожидаем после загрузки
        'check_title': 'Яндекс',                  # заголовок сайта, который ожидаем после
        'debug_mode': False,                       # debug
        'repeat_search': True,                    # Если не найдет в арене, повторит по всему экрану
        'path_to_res': RESOURCE_DIR,

        # Ресурсы
        'logo': os.path.join(RESOURCE_DIR, 'logo.png'),
        'mail': os.path.join(RESOURCE_DIR, 'mail.png'),
        'logo_auth': os.path.join(RESOURCE_DIR, 'logo_auth.png'),
        'login_button': os.path.join(RESOURCE_DIR, 'login.png'),
        'user_login': os.path.join(RESOURCE_DIR, 'user_login.png'),

        # Арены
        "main_logo_area": (
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 0]
        ),

        "mail_area": (
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 0]
        ),

        "auth_area": (
            [0, 1, 0],
            [0, 1, 0],
            [0, 0, 0]
        ),

        "user_login_area": (
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 0]
        )
    }