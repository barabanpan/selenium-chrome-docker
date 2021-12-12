from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service


chrome_options = ChromeOptions()
chrome_options.add_argument('--window-size=1280,720')
chrome_options.add_argument('--no-sandbox')

remote_driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)
