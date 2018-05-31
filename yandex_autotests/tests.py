import pytest
from utils import is_driver, run_driver, kill_driver


def setup_module(self):
    """
    Подготовка тестового окружения. Запуск вебдрайвера если он не запущен.
    """
    if not is_driver():
        run_driver()

def teardown_module(self):
    """"
    Остановка тестового окружения. Остановка вебдрайвера.
    """
    kill_driver()


class TestOpenWebsite:
    @pytest.mark.usefixtures("driver")
    def test_login(self, driver):
        """
        Первый тест. Проверяет, что по адресу yandex.ru открывается фактически данный сайт.
        :param driver: webdriver
        """
        assert pytest.check_title == driver.title
        assert pytest.check_url == driver.current_url
        assert pytest.check_url == driver.find_element_by_class_name("home-logo__link").get_attribute("href")


class TestPositiveAuthorization:
    @pytest.mark.usefixtures("driver")
    def test_authorization(self, driver):
        """
        Второй тест. Позитивная авторизация, тестовым пользователем, на сайте yandex.ru
        :param driver: webdriver
        """

        # Ищу элемент для авторизации и регистрации в почте
        auth_desk = driver.find_element_by_class_name("desk-notif-card__card")
        # Прохожу по всем тегам "а", ищу кнопку "Войти", кликаю на нее
        for _a in auth_desk.find_elements_by_tag_name("a"):
            if "https://passport.yandex.ru/auth" in _a.get_attribute("href"):
                if _a.get_attribute("role") == "button":
                    _a.click()
                    break

        # Ожидаю форму для авторизации
        passport_desk = driver.find_element_by_class_name("passport-Domik-Content")
        # Прохожу по полям "input", ищу поле для ввода логина и пароля
        for field in passport_desk.find_elements_by_tag_name("input"):
            if field.get_attribute("name") == "login":
                # Ввожу логин
                field.send_keys(pytest.username)
            elif field.get_attribute("name") == "passwd":
                # Ввожу пароль
                field.send_keys(pytest.password)

        # Ищу кнопку "Войти" в почту и кликаю на нее
        passport_enter = passport_desk.find_element_by_class_name("passport-Button")
        passport_enter.click()

        # Получаю логин пользователя которым я вошел и проверяю что это мой
        desk_user = driver.find_element_by_class_name("mail-User-Name").text
        assert desk_user == pytest.username

