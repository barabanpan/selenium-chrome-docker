import sys
import time

from loguru import logger

from bot.bot import PdaBot
from bot.constants import REMOTE_DRIVER, LOCAL_DRIVER, MEMBER_ID, PASS_HASH


if __name__ == "__main__":
    time_start = int(time.time())
    driver_type = sys.argv[1] if len(sys.argv) > 1 else LOCAL_DRIVER
    logger.debug(f"Driver: {driver_type}")
    try:
        bot = PdaBot(driver_type=driver_type)
        bot.driver.get("https://4pda.to")
        bot.login_with_cookies(MEMBER_ID, PASS_HASH)
        bot.open_android_forum()
        bot.download_topics()
        seconds = int(time.time()) - time.start
        logger.info(f"Time taken: {seconds // 3600}h {seconds // 60 % 60}m {seconds % 60}s.")
    except Exception as e:
        logger.error(repr(e))
        if driver_type == REMOTE_DRIVER:
            bot.driver.quit()
    if driver_type == REMOTE_DRIVER:
        bot.driver.quit()
