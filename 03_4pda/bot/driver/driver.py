import os
from loguru import logger
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options

from bot.constants import REMOTE_DRIVER, LOCAL_DRIVER, DOWNLOAD_FOLDER


def get_driver(driver_type=LOCAL_DRIVER):
    chrome_options = Options() if driver_type == REMOTE_DRIVER else ChromeOptions()
    chrome_options.add_argument('--window-size=1400,800')
    # chrome_options.add_extension(os.getcwd() + '/bot/driver/AdBlock-4.41.0.crx')
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': os.getcwd() + DOWNLOAD_FOLDER,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
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
