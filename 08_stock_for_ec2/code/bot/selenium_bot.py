import os
from time import sleep
from datetime import datetime, timedelta

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

from bot.constants import TIMEOUT, CSV_PATH, TXT_PATH
from bot.driver.driver import get_chrome_driver as get_driver


def clean_and_to_float(string):
    return float(string.strip().replace(',', ''))


def get_percent_diff(old_value, new_value):
    """100(1 - old/new) gives percent diff"""
    return round(100 * (1 - old_value/new_value), 2)


def csv_updated_more_than_week_ago():
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


def get_last_update_if_not_older_than_24_hours():
    message_for_update = f"Txt file '{TXT_PATH}' will be updated"
    if not os.path.exists(TXT_PATH):
        logger.debug(message_for_update)
        return False  # obviously updates are needed

    modified_time = os.path.getmtime(TXT_PATH)
    if modified_time + timedelta(days=1).total_seconds() < datetime.now().timestamp():
        logger.debug(message_for_update)
        return False
    logger.debug(f"TXT file '{CSV_PATH}' is fresh enough!")
    with open(TXT_PATH, "r") as file:
        update = ""
        for line in file:
            update += line
    return update


class StocksBot:
    def __init__(self, driver_type):
        self.driver = get_driver(driver_type)
        self.timeout = TIMEOUT
        self.to_buy_messages = list()
        self.to_sell_messages = list()
        self.changes = ""

    def find(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def find_click(self, xpath):
        return WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def find_all(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))

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

    def check_price_changes(self):
        df = pd.read_csv(CSV_PATH)
        self.to_sell_messages = list()  # empty the lists
        self.to_buy_messages = list()
        for index, row in df.iterrows():  # generator, not list
            if index > 10:
                break
            ticker = row["ticker"].replace(".", "-")
            old_price = row["price"]
            self.driver.get(f"https://finance.yahoo.com/quote/{ticker}?p={ticker}")
            xpath = '//fin-streamer[@class="Fw(b) Fz(36px) Mb(-4px) D(ib)"]'
            new_price = clean_and_to_float(self.find(xpath).text)
            diff = get_percent_diff(old_price, new_price)
            if diff >= 1:
                self.to_sell_messages.append(f'{diff}! {ticker} - was: {old_price}, now: {new_price}')
            if diff <= -1:
                self.to_buy_messages.append(f'{diff}! {ticker} - was: {old_price}, now: {new_price}')
        logger.debug("All 505 tickers were processed")

    def write_changes_to_txt_file(self):
        self.changes = ("TIME TO BUY:\n" + "\n".join(self.to_buy_messages)) if self.to_buy_messages else ""
        self.changes += ("\n\nTIME TO SELL:\n" + "\n".join(self.to_sell_messages)) if self.to_sell_messages else ""
        if not self.changes:
            self.changes = "No significant price changes so far!"
        with open(TXT_PATH, "w+") as file:
            file.writelines(self.changes)
        logger.debug(f"Wrote change updates to txt file {TXT_PATH}")
