from time import sleep

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium import webdriver

from bot.constants import TIMEOUT
from bot.driver.driver import get_driver


class RozetkaBot:
    def __init__(self, driver_type):
        self.driver = get_driver(driver_type)
        self.timeout = TIMEOUT

    def find(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def find_click(self, xpath):
        return WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

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
            logger.debug(f"Logged in as {login}")
        else:
            self.find('//div[contains(@class,"recaptcha-checkbox")]').click()
            self.find('//button[contains(@class, "auth-modal__submit")]').click()
            # can't check if indeed logged in
            logger.debug(f"Logged in as {login} after captcha")

    def open_phones(self):
        # self.find('//button[@id="fat-menu"]').click()
        # self.find('//a[contains(@href, "c4627949")]').click()
        # doesn't work :(
        # self.find('//a[contains(@href, "c80003")]').click()
        self.driver.get('https://rozetka.com.ua/ua/mobile-phones/c80003/preset=smartfon/')
        logger.debug("Opened smartphones")

    def check_boxes(self):
        # brand
        self.find('//label[@for="OnePlus"]').click()
        self.find('//label[@for="Samsung"]').click()
        self.find('//label[@for="Xiaomi"]').click()
        logger.debug("Sorted by brands")
        # ram
        self.find('//label[@for="8 ГБ"]').click()
        self.find('//label[@for="12 ГБ"]').click()
        logger.debug("Sorted by RAM")
        # memory
        self.find('//label[@for="128 ГБ"]').click()
        self.find('//label[@for="256 ГБ"]').click()
        logger.debug("Sorted by memory")
        # screen
        self.find('//label[contains(@for, "6.49")]').click()
        self.find('//label[contains(@for, "6.5")]').click()
        logger.debug("Sorted by screen size")
        # processor
        self.find('//label[contains(@for, "Qualcomm")]').click()
        logger.debug("Sorted by processor")
        # price
        self.find('//input[@formcontrolname="min"]').clear()
        self.find('//input[@formcontrolname="min"]').send_keys(10000)
        self.find('//input[@formcontrolname="max"]').clear()
        self.find('//input[@formcontrolname="max"]').send_keys(20000)
        self.find('//button[text()=" Ok "]').click()
        logger.debug("Sorted by price")

    def sort(self):
        Select(self.find('//select')).select_by_visible_text('Новинки')
        logger.debug("Sorted by 'Новинки'")

    def add_to_compare_and_click(self, first_n):
        elements = self.find_all(f'//button[contains(@class,"compare-button")]')
        for el in elements[:first_n]:
            # for ElementClickInterceptedException
            webdriver.ActionChains(self.driver).move_to_element(el).click(el).perform()
        logger.debug("Added to compare")

        self.find('//button[contains(@aria-label, "Списки")]').click()
        self.find('//a[contains(@class, "comparison")]').click()
        self.find('//button[contains(text(),"відмінності")]').click()
        logger.debug("Chose only differences")
