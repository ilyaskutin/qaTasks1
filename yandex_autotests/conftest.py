import pytest


@pytest.fixture
def driver(webdriver):
    """
    Фикстура подготавливает драйвер к работе
    :return: webdriver
    """
    webdriver.get(pytest.url)
    webdriver.implicitly_wait(pytest.timeout)
    return webdriver


def pytest_namespace():
    """
    Константы
    """
    return {
        'timeout' : 20,                           # таймаут для вебдрайвера, сколько секунд ждать загрузки эл-та
        'url': 'http://www.yandex.ru',            # url сайта которые проверям
        'username': 'arrival18',                  # логин тестового пользователя
        'password': 'QWEqwe123',                  # пароль тестового пользователя

        'check_url': 'https://www.yandex.ru/',    # url сайта, который ожидаем после загрузки
        'check_title': 'Яндекс',                  # заголовок сайта, который ожидаем после загрузки
    }

