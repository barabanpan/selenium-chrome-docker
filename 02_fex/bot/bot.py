from time import sleep
import os

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from bot.constants import TIMEOUT, FILE_FOLDER
from bot.driver.driver import get_driver


class FexBot:
    def __init__(self, driver_type):
        self.driver = get_driver(driver_type)
        self.timeout = TIMEOUT

    def find(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def find_all(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))

    def pass_files(self, file_names):
        self.find('//button/span[text()="Передати файли"]').click()
        cwd = os.getcwd()
        for name in file_names:
            abs_path = os.path.join(cwd, FILE_FOLDER, name)
            self.find('//button/span[text()="Додати"]').click()
            el = self.find('//li[contains(@class, "drop-down")][1]')
            el.find_element_by_xpath('//input[@type="file"]').send_keys(abs_path)
            sleep(10)
            self.find('//span[@class="modal__close-btn"]').click()
            logger.debug(f"Uploaded file {abs_path}")

            # can't find it, why???
            # self.find('//input[@type="file"]').send_keys(abs_path)
            # self.find('//input[@type="file"]').click()

            #//button[contains(@class, "button_theme_secondary")]