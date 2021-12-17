from time import sleep
import os

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from bot.constants import TIMEOUT, UPLOAD_FOLDER, DOWNLOAD_FOLDER
from bot.driver.driver import get_driver


def find_file_in_items(items, file_name):
    # find right files
    for item in items:
        try:
            print("hereA")
            name = item.find_element_by_xpath('.//span[contains(@class, "text_overflow_ellipsis")]').text
            print("hereB")
        except NoSuchElementException:
            # it's a folder, not a file
            print("hereC")
            continue
        print("hereD")
        if name == file_name:
            print("hereE")
            return item


class FexBot:
    def __init__(self, driver_type):
        self.driver = get_driver(driver_type)
        self.timeout = TIMEOUT

    def find(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def find_all(self, xpath):
        sleep(0.5)
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))

    def pass_files(self, file_names):
        self.find('//button/span[text()="Передати файли"]').click()
        cwd = os.getcwd()
        for name in file_names:
            abs_path = os.path.join(cwd, UPLOAD_FOLDER, name)
            self.find('//button/span[text()="Додати"]').click()
            el = self.find('//li[contains(@class, "drop-down")][1]')
            el.find_element_by_xpath('//input[@type="file"]').send_keys(abs_path)
            # TODO: wait for first 10 sec, for other 1 sec
            sleep(10)
            self.find('//span[@class="modal__close-btn"]').click()
            logger.debug(f"Uploaded file {abs_path}")

            # can't find it, why???
            # self.find('//input[@type="file"]').send_keys(abs_path)
            # self.find('//input[@type="file"]').click()

    def create_folder(self, folder_name):
        self.find('//button[contains(@class, "button_theme_secondary")]').click()
        self.find('//input[@class="input"]').send_keys(folder_name)
        self.find('//button[@type="submit"]').click()
        logger.debug(f"Created folder '{folder_name}'")

    def close_black_thing_if_its_there(self):
        try:
            self.find('//div[text()="ЗАКРЫТЬ"]').click()
            logger.debug("Closed the black thing")
        except:
            logger.debug("Didn't find the black thing")

    def close_ads_if_they_are_there(self):
        try:
            ads = self.find_all('//iframe[@width="240px" and @height="400px"]')
            for ad in ads:
                ad.find_element_by_xpath('.//div[@id="cbb"]').click()
            logger.debug("Closed ads")
        except:
            logger.debug("Didn't find ads")

    def move_files(self, file_names, folder_name):
        print("here1")

        items = self.find_all('//div[contains(@class, "table__item")]')
        for file_name in [n.split('.')[0] for n in file_names]:
            print("here2")
            item = find_file_in_items(items, file_name)
            print("here3")
            #retry_click(xpath)
            i = item.find_element_by_xpath('.//span[@class="checkbox__icon checkbox__icon_state_multi"]')
            print("here4")
            i.click()
            logger.debug(f"Pick file with name '{file_name}'")
        self.find('//span[text()="Перемістити"]').click()
        print("here5")

        # find right folder
        folder_items = self.find_all('//li[contains(@class, "tree-manage-list__item")]')
        print("here6")
        for folder in folder_items:
            print("here7")
            name = folder.find_element_by_xpath('.//span[contains(@class, "text")]').text
            if name == folder_name:
                print("here8")
                folder.click()
                self.close_ads_if_they_are_there()
                self.find('//button[contains(@class, "primary")]/span[text()="Перемістити"]').click()
                logger.debug(f"Moved picked files to folder '{folder_name}'")
                break

    def open_folder(self, folder_name):
        xp = f'//div[contains(@class, "table__item")]//div[@class="text_overflow_ellipsis" and text()="{folder_name}"]'
        self.find(xp).click()

    def add_to_name(self, old_name, add_to_name):
        # find right file
        items = self.find_all('//div[contains(@class, "table__item")]')
        old_name_no_ext = old_name.split('.')[0]
        new_name = old_name_no_ext + add_to_name + "." + old_name.split('.')[1]
        item = find_file_in_items(items, old_name_no_ext)
        logger.debug(f"Found file with name '{old_name}' to rename")

        item.find_element_by_xpath('.//div[contains(@class,"tooltip-anchor node-controls")]').click()
        self.find('//span[text()="Перейменувати"]').click()
        self.find('//input[@data-qa="renameNodeForm_name"]').clear()  # WHY NO WORKING???
        self.find('//input[@data-qa="renameNodeForm_name"]').send_keys(add_to_name)
        self.find('//button//span[text()="Зберегти"]').click()
        logger.debug(f"Renamed file '{old_name}' to '{new_name}'")

    def remove_file(self, file_name):
        # find right file
        print("here8")
        items = self.find_all('//div[contains(@class, "table__item")]')
        print("here9")
        item = find_file_in_items(items, file_name.split('.')[0])
        print("here10")
        logger.debug(f"Found file with name '{file_name}' to delete")
        print("here11")

        item.find_element_by_xpath('.//span[contains(@class, "checkbox__icon")]').click()
        print("here5")
        self.find('//span[contains(@class, "checkbox__icon")]').click()
        print("here6")
        self.find('//button[contains(@class, "primary")]//span[text()="Видалити"]').click()
        print("here7")
        logger.debug(f"File {file_name} deleted")
