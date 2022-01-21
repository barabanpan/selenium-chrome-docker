import os
import platform

from loguru import logger
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from msedge.selenium_tools import EdgeOptions, Edge

from bot.constants import REMOTE_DRIVER, LOCAL_DRIVER

sys = platform.system()

chrome_driver_path = {
    "Linux": os.getcwd() + os.sep + os.sep.join(['bot', 'driver', 'chromedriver_96_linux']),
    "Windows": os.getcwd() + os.sep + os.sep.join(['bot', 'driver', 'chromedriver_97_windows.exe'])
}

edge_driver_path = {
    "Linux": "not_there_yet!",
    "Windows": os.getcwd() + os.sep + os.sep.join(['bot', 'driver', 'edgedriver_97_windows.exe'])
}

def get_chrome_driver(driver_type=LOCAL_DRIVER):
    chrome_options = Options() if driver_type == REMOTE_DRIVER else ChromeOptions()
    chrome_options.add_argument('--window-size=1400,800')
    chrome_options.add_extension(os.getcwd() + os.sep + os.sep.join(["bot", "driver", "AdBlock-4.41.0_chrome.crx"]))
    # chrome_options.add_argument("user-data-dir=/home/nataliia/.config/google-chrome/Profile 1")

    try:
        if driver_type == REMOTE_DRIVER:
            return webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)
        elif driver_type == LOCAL_DRIVER:
            driver_path = chrome_driver_path[sys]
            print(driver_path)
            return webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
        else:
            logger.error('Unsupported type driver!')
    except Exception as e:
        logger.error(repr(e))


def get_edge_driver(driver_type=LOCAL_DRIVER):
    options = EdgeOptions()
    options.use_chromium = True

    try:
        if driver_type == REMOTE_DRIVER:
            return webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=options)
        elif driver_type == LOCAL_DRIVER:
            driver_path = edge_driver_path[sys]
            return Edge(executable_path=driver_path, options=options)
        else:
            logger.error('Unsupported type driver!')
    except Exception as e:
        logger.error(repr(e))
