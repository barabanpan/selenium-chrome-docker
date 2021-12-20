from time import sleep
import os

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from bot.constants import TIMEOUT
from bot.driver.driver import get_driver


class PdaBot:
    def __init__(self, driver_type):
        self.driver = get_driver(driver_type)
        self.timeout = TIMEOUT

    def find(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def find_all(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))

    def login_with_cookies(self, member_id, pass_hash):
        self.driver.add_cookie({"name": "member_id", "value": member_id})
        self.driver.add_cookie({"name": "pass_hash", "value": pass_hash})
        self.driver.refresh()
        sleep(0.5)
        logger.debug("Passed cookies")

    def open_android_forum(self):
        self.find('//a[@href="//4pda.to/forum/"]').click()
        self.find('//a[text()="Android - Программы"]').click()
        logger.debug("Opened 'Android - Программы'")

        self.find('//a[text()="Программы для ПК"]').click()
        logger.debug("Opened 'Программы для ПК'")

    def download_topics(self):
        pages = int(self.find('//span[@class="pagelink" and contains(text(), "страниц")]').text.split()[0])
        logger.debug(f"There are {pages} pages with topics")

        for i in range(1, pages + 1):
            self.find('//span[@class="pagelink" and contains(text(), "страниц")]').click()
            self.find('//input[@type="text" and contains(@id, "st")]').send_keys(i)
            self.find('//input[@value="ОК"]').click()

            print(f"page {i}")
            # get all elements in one page
            """elements = self.find_all('//span[contains(@id, "tid-span")]')
            for el in elements:
                el.click()
                #logger.debug("Opened topic with id=309357")

                self.find('//div[@class="popmenubutton"]').click()
                self.find('//a[text()="Добавить в избранное"]').click()
                #logger.debug('Added to "избранное"')

                self.find('//div[@class="popmenubutton"]').click()
                self.find('//a[text()="Скачать тему"]').click()
                self.find('//a[text()="HTML версия"]').click()

                self.find('//a[text()="Вернуться в тему"]').click()

                # go to last page and click 'хорошо' ??
                # self.find('//a[@title="На последнюю страницу"]').click()

                # return to all topics
                self.find('//a[text()="Программы для ПК"]').click()"""
            logger.debug(f"{i} page of topics was downloaded")
