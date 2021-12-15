import sys

from loguru import logger

from bot.bot import FexBot
from bot.constants import REMOTE_DRIVER, LOCAL_DRIVER


if __name__ == "__main__":
    r_bot = ""
    try:
        r_bot = FexBot(driver_type=sys.argv[1] if len(sys.argv) > 1 else LOCAL_DRIVER)
        r_bot.driver.get("https://fex.net/uk/")
        r_bot.pass_files(['file1.txt', 'file2.txt', 'file3.txt'])

    except Exception as e:
        logger.error(repr(e))
        if sys.argv[1] == REMOTE_DRIVER:
            r_bot.driver.quit()
    if sys.argv[1] == REMOTE_DRIVER:
        r_bot.driver.quit()
