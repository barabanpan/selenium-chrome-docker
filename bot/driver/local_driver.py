import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

driver_path = os.getcwd() + '/bot/driver/chromedriver_96'

options = Options()
options.add_argument('--window-size=1400,800')
# 1 to allow, 2 to block
options.add_experimental_option('prefs', {
    'safebrowsing.enabled': True,
    'profile.default_content_setting_values.notifications': 2
})

local_driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

