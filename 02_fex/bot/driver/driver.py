import os
from loguru import logger
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options

from bot.constants import REMOTE_DRIVER, LOCAL_DRIVER


def get_driver(driver_type=LOCAL_DRIVER):
    chrome_options = Options() if driver_type == REMOTE_DRIVER else ChromeOptions()
    chrome_options.add_argument('--window-size=1400,800')
    try:
        if driver_type == REMOTE_DRIVER:
            return webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)
        elif driver_type == LOCAL_DRIVER:
            driver_path = os.getcwd() + '/bot/driver/chromedriver_96'
            return webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
        else:
            logger.error('Unsupported type driver!')
    except Exception as e:
        logger.error(repr(e))
