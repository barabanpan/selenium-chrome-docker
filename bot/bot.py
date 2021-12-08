from time import sleep

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from bot.driver.driver import local_driver #, docker_driver
from bot.constants import DOCKER_DRIVER, LOCAL_DRIVER, TIMEOUT


class RozetkaBot:
    def __init__(self, driver_type=LOCAL_DRIVER):
        if driver_type == DOCKER_DRIVER:
            # self.driver = docker_driver
            pass
        else:
            self.driver = local_driver
        self.timeout = TIMEOUT

    def find(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def find_all(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))

    def auth(self, login, password):
        self.find('//button[@class="header__button ng-star-inserted"]').click()
        self.find('//input[@id="auth_email"]').send_keys(login)
        self.find('//input[@id="auth_pass"]').send_keys(password)
        self.find('//button[contains(@class, "auth-modal__submit")]').click()
        try:
            self.find('//div[contains(@class,"recaptcha-checkbox")]')
        except TimeoutException:
            # can't check if indeed logged in
            logger.info(f"Logged in as {login}")
        else:
            self.find('//div[contains(@class,"recaptcha-checkbox")]').click()
            self.find('//button[contains(@class, "auth-modal__submit")]').click()
            # can't check if indeed logged in
            logger.info(f"Logged in as {login} after captcha")

    def open_phones(self):
        # how to do that properly???
        self.driver.get('https://rozetka.com.ua/ua/mobile-phones/c80003/preset=smartfon/')

    def check_boxes(self):
        # brand
        self.find('//label[@for="OnePlus"]').click()
        self.find('//label[@for="Samsung"]').click()
        self.find('//label[@for="Xiaomi"]').click()
        # ram
        self.find('//label[@for="8 ГБ"]').click()
        self.find('//label[@for="12 ГБ"]').click()
        # memory
        self.find('//label[@for="128 ГБ"]').click()
        self.find('//label[@for="256 ГБ"]').click()
        # screen
        self.find('//label[contains(@for, "6.49")]').click()
        self.find('//label[contains(@for, "6.5")]').click()
        # processor
        self.find('//label[contains(@for, "Qualcomm")]').click()
        # price
        # clean?
        self.find('//input[@formcontrolname="min"]').clear()
        self.find('//input[@formcontrolname="min"]').send_keys(10000)
        self.find('//input[@formcontrolname="max"]').clear()
        self.find('//input[@formcontrolname="max"]').send_keys(20000)
        self.find('//button[text()=" Ok "]').click()

    def sort(self):
        self.find('//select').click()
        self.find('//select/option[text()=" Новинки "]').click()
        sleep(3)

    def add_to_compare(self):
        # it doesn't work! :(
        self.find('//ul[contains(@class, "catalog")]/li[1]')




















