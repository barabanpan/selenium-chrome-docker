import sys

from loguru import logger

from bot.bot import StocksBot
from bot.constants import REMOTE_DRIVER, LOCAL_DRIVER


if __name__ == "__main__":
    driver_type = sys.argv[1] if len(sys.argv) > 1 else LOCAL_DRIVER
    logger.debug(f"Driver: {driver_type}")
    try:
        bot = StocksBot(driver_type=driver_type)
        bot.driver.get("https://www.slickcharts.com/sp500")
        if bot.csv_updated_more_than_week_ago():
            bot.write_505_stock_prices_to_csv()
        bot.driver.get("https://finance.yahoo.com/")
        bot.check_price_changes_and_write_to_list()

    except Exception as e:
        logger.error(repr(e))
        if driver_type == REMOTE_DRIVER:
            r_bot.driver.quit()
    if driver_type == REMOTE_DRIVER:
        r_bot.driver.quit()
