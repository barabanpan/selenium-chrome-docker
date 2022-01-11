import os
from time import sleep

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium import webdriver

from bot.constants import TIMEOUT, CSV_PATH
from bot.driver.driver import get_edge_driver as get_driver


class StocksBot:
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

    def csv_updated_more_than_week_ago(self):
        if not os.path.exists(CSV_PATH):
            return True   # obviously updates are needed
        # modified_time = os.path.getmtime(CSV_PATH)
        # if mo
        # last updated less that a week ado - false
        # else true

        return False

    def write_505_stock_prices_to_csv(self):
        rows = self.find_all('//tbody/tr')[:506]
        for row in rows[:3]:
            tds = row.find_elements_by_xpath('.//td')
            ticker = tds[2].find_element_by_xpath('.//a').text
            print(ticker, end=", ")
            price = float(tds[4].text.strip().replace(',', ''))
            print(price)
            # add to pandas DataFrame
        # write to csv
