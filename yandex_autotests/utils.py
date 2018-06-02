import subprocess
import os
import time


class Browser:
    def __init__(self):
        self.existing_id = self.__browser_id()
        self.my_wnd_id = []

    def is_browser(self):
        """
        Проверяет запущен браузер или нет
        :return: bool
        """
        out, err = self.__parse_ps()
        if out:
            return True
        else:
            return False

    def browser_run(self, url, timeout=10):
        """
        Запускает браузер и сохраняет его PID в self.my_wnd_id
        :return: bool
        """
        subprocess.Popen(["chromium-browser --incognito --start-maximized --new-window {}".format(url)],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)
        __find_iter = 0
        while not list(set(self.existing_id + self.__browser_id())):
            if __find_iter > timeout:
                return False
            time.sleep(1)
            __find_iter += 1
        self.my_wnd_id = list(set(self.existing_id + self.__browser_id()))
        return True

    def browser_close(self):
        """
        Останавливает все процессы chromium-browse, которые
        были запущены с помощью этого класса
        """
        for b_id in self.my_wnd_id:
            os.system("kill -9 {}".format(b_id))

    def __parse_ps(self):
        """
        Пасит вывод команды ps cax | grep chromium-browse
        :return: str, str
        """
        proc1 = subprocess.Popen(['ps', 'cax'],
                                 stdout=subprocess.PIPE)

        proc2 = subprocess.Popen(['grep', 'chromium-browse'],
                                 stdin=proc1.stdout,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        proc1.stdout.close()
        out, err = proc2.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def __browser_id(self):
        """
        Парсит PID процессов chromedriver
        :return: list
        """
        out, err = self.__parse_ps()
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
