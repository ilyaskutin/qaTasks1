### Задание

* Cоздайте тест (или несколько тестов), который должен проверять, что по адресу yandex.ru открывается фактически данный сайт, то есть проверить по каким-либо ключевым словам на странице или иначе.
 
 * Опционально (но, то, что даст вам преимущество). Добавьте тест позитивной авторизации, тестовым пользователем, на сайте yandex.ru.
 
##### Мы ожидаем, что:
 * Будет использован Python3. Фреймворк для тестирования PyTest.
 * НЕ будет использован Selenium.
 * Тест (или тесты), данные и используемые библиотеки будут разнесены.
 * Будут использованы фикстуры, в том числе setup teardown.
 * Решение оформлено в виде архива, с инструкцией по установке компонент и их использованию.
 
### Решение

Код моего решения находится в папке yandex_autotests

#### Как запускать
* Склонировать себе репозиторий
* Установить необходимые пакеты с помощью команды ```sudo apt-get install $(cat ./debian_requirements.txt)```
* Создать виртуальное окружение с помощью команды  ```virtualenv venv -p python3```
* Установить python пакеты с помощью команды ```./venv/bin/pip install -r  python_requirements.txt```
* Для запуска тестов использовать команду ```./venv/bin/python3 -m pytest -q ./yandex_autotests/tests.py```

