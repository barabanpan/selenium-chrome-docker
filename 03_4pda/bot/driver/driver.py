import os
from loguru import logger
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, FirefoxProfile
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FOptions

from bot.constants import REMOTE_DRIVER, LOCAL_DRIVER, DOWNLOAD_FOLDER


def get_chrome_driver(driver_type=LOCAL_DRIVER):
    chrome_options = Options() if driver_type == REMOTE_DRIVER else ChromeOptions()
    chrome_options.add_argument('--window-size=1400,800')
    # chrome_options.add_extension(os.getcwd() + '/bot/driver/AdBlock-4.41.0.crx')
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': os.getcwd() + os.sep + DOWNLOAD_FOLDER,
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


def get_mozilla_driver(driver_type=LOCAL_DRIVER):
    firefox_options = FOptions()
    firefox_options.add_argument("--window-size=1400,800")

    # 2 for custom specified folder
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("browser.download.dir", os.getcwd() + os.sep + DOWNLOAD_FOLDER)
    # find right mime type
    firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/html")
    # files are downloaded without extension, why?

    try:
        if driver_type == REMOTE_DRIVER:
            return webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=firefox_options)
        elif driver_type == LOCAL_DRIVER:
            driver_path = os.getcwd() + '/bot/driver/geckodriver_v0.30.0'
            return webdriver.Firefox(executable_path=driver_path, options=firefox_options)
        else:
            logger.error('Unsupported type driver!')
    except Exception as e:
        logger.error(repr(e))



