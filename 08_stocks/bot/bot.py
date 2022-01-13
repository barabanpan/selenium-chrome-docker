import os
from time import sleep
from datetime import datetime, timedelta

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import pandas as pd

from bot.constants import TIMEOUT, CSV_PATH
from bot.driver.driver import get_edge_driver as get_driver


def clean_and_to_float(string):
    return float(string.strip().replace(',', ''))


def get_percent_diff(old_value, new_value):
    """100(1 - old/new) gives percent diff"""
    return round(100 * (1 - old_value/new_value), 2)


class StocksBot:
    def __init__(self, driver_type):
        self.driver = get_driver(driver_type)
        self.timeout = TIMEOUT
        self.changed_prices = []

    def find(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def find_click(self, xpath):
        return WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def find_all(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))

    def csv_updated_more_than_week_ago(self):
        message_for_update = f"Csv file '{CSV_PATH}' will be updated"
        if not os.path.exists(CSV_PATH):
            logger.debug(message_for_update)
            return True   # obviously updates are needed

        modified_time = os.path.getmtime(CSV_PATH)
        if modified_time + timedelta(days=7).total_seconds() < datetime.now().timestamp():
            logger.debug(message_for_update)
            return True
        logger.debug(f"Csv file '{CSV_PATH}' won't be updated")
        return False

    def write_505_stock_prices_to_csv(self):
        rows = self.find_all('//tbody/tr')[:505]
        data = []
        for row in rows:
            tds = row.find_elements_by_xpath('.//td')
            ticker = tds[2].find_element_by_xpath('.//a').text
            price = clean_and_to_float(tds[4].text)
            data.append([ticker, price])
        data_df = pd.DataFrame(data=data, columns=["ticker", "price"])
        data_df.to_csv(CSV_PATH, index=False)
        logger.debug("505 rows were written to csv")

    def check_price_changes_and_write_to_list(self):
        df = pd.read_csv(CSV_PATH)
        for index, row in df.iterrows():  # generator, not list
            if index > 10:
                break
            ticker = row["ticker"].replace(".", "-")
            old_price = row["price"]
            # self.find('//input[@id="yfin-usr-qry"]').send_keys(ticker)
            # self.find('//button[@id="header-desktop-search-button"]').click()
            self.driver.get(f"https://finance.yahoo.com/quote/{ticker}?p={ticker}")
            xpath = '//fin-streamer[@class="Fw(b) Fz(36px) Mb(-4px) D(ib)"]'
            new_price = clean_and_to_float(self.find(xpath).text)
            # new_price = clean_and_to_float(self.find('//span[@class="_11248a25 c916dce9"]').text)
            diff = get_percent_diff(old_price, new_price)
            if diff >= 1:
                print(f'TIME TO SELL({diff})! {ticker} - was: "{old_price}", now: "{new_price}"')
            if diff <= -1:
                print(f'TIME TO BUY({diff})! {ticker} - was: "{old_price}", now: "{new_price}"')
        logger.debug("All 505 tickers were processed")
