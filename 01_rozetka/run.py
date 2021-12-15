import sys

from loguru import logger

from bot.bot import RozetkaBot
from bot.constants import REMOTE_DRIVER, LOCAL_DRIVER, FIRST_N_PHONES
from bot.credentials import login, password


if __name__ == "__main__":
    r_bot = ""
    driver_type = sys.argv[1] if len(sys.argv) > 1 else LOCAL_DRIVER
    try:
        r_bot = RozetkaBot(driver_type=driver_type)
        r_bot.driver.get("https://rozetka.com.ua/ua/")
        # r_bot.auth(login, password)  # captcha :(
        r_bot.open_phones()
        r_bot.check_boxes()
        # r_bot.sort()
        r_bot.add_to_compare_and_click(first_n=FIRST_N_PHONES)
    except Exception as e:
        logger.error(repr(e))
        if driver_type == REMOTE_DRIVER:
            r_bot.driver.quit()
    if driver_type == REMOTE_DRIVER:
        r_bot.driver.quit()
