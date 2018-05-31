import subprocess
import os


def parse_ps():
    """
    Пасит вывод команды ps cax | grep chromedriver
    :return: str, str
    """
    proc1 = subprocess.Popen(['ps', 'cax'],
                             stdout=subprocess.PIPE)

    proc2 = subprocess.Popen(['grep', 'chromedriver'],
                             stdin=proc1.stdout,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    proc1.stdout.close()
    out, err = proc2.communicate()
    return out.decode("utf-8"), err.decode("utf-8")


def is_driver():
    """
    Проверяет запущен веб драйвер или нет
    :return: bool
    """
    out, err = parse_ps()
    if out:
        return True
    else:
        return False


def run_driver():
    """
    Просто запускает драйвер
    """
    subprocess.Popen(['{}/chromedriver'.format(os.getcwd())],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     shell=True)


def driver_id():
    """
    Парсит PID процессов chromedriver
    :return: list
    """
    out, err = parse_ps()
    id = []
    for line in out.split("\n"):
        if line != "":
            for l in line.split(" "):
                try:
                    id.append(int(l))
                except ValueError:
                    continue
                break
    return id


def kill_driver():
    """
    Останавливает все запущенные процессы chromedriver
    """
    for id in driver_id():
        os.system("kill -9 {}".format(id))

kill_driver()