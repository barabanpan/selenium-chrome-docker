import sys

from loguru import logger

from bot.bot import PdaBot
from bot.constants import REMOTE_DRIVER, LOCAL_DRIVER, FEX_FOLDER_NAME


if __name__ == "__main__":
    r_bot = ""
    driver_type = sys.argv[1] if len(sys.argv) > 1 else LOCAL_DRIVER
    logger.debug(f"Driver: {driver_type}")
    try:
        f_bot = PdaBot(driver_type=driver_type)
        f_bot.driver.get("https://fex.net/uk/")

    except Exception as e:
        logger.error(repr(e))
        if driver_type == REMOTE_DRIVER:
            r_bot.driver.quit()
    if driver_type == REMOTE_DRIVER:
        r_bot.driver.quit()
