# import sys
# import os

from loguru import logger
# from dotenv import load_dotenv

from bot.selenium_bot import StocksBot, csv_updated_more_than_week_ago, get_last_update_if_not_older_than_24_hours
from bot.constants import REMOTE_DRIVER, LOCAL_DRIVER


def run_selenium_bot(driver_type=LOCAL_DRIVER):
    logger.debug(f"Driver: {driver_type}")
    try:
        res = get_last_update_if_not_older_than_24_hours()
        if res:
            return res

        bot = StocksBot(driver_type=driver_type)
        bot.driver.get("https://www.slickcharts.com/sp500")
        if csv_updated_more_than_week_ago():
            bot.write_505_stock_prices_to_csv()
        bot.driver.get("https://finance.yahoo.com/")
        bot.check_price_changes()
        bot.write_changes_to_txt_file()

        if driver_type == REMOTE_DRIVER:
            bot.driver.quit()
        return bot.changes
    except Exception as e:
        logger.error(repr(e))
        if driver_type == REMOTE_DRIVER:
            bot.driver.quit()