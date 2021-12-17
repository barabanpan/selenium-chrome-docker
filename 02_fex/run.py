import sys

from loguru import logger

from bot.bot import FexBot
from bot.constants import REMOTE_DRIVER, LOCAL_DRIVER, FEX_FOLDER_NAME

files_list = ['file1.txt', 'file2.txt'] #, 'file3.txt']

if __name__ == "__main__":
    driver_type = sys.argv[1] if len(sys.argv) > 1 else LOCAL_DRIVER
    logger.debug(f"Driver: {driver_type}")
    try:
        f_bot = FexBot(driver_type=driver_type)
        f_bot.driver.get("https://fex.net/uk/")
        f_bot.pass_files(files_list)
        f_bot.create_folder(FEX_FOLDER_NAME)
        f_bot.close_black_thing_if_its_there()
        f_bot.move_files(files_list, FEX_FOLDER_NAME)
        f_bot.open_folder(FEX_FOLDER_NAME)
        f_bot.add_to_name(files_list[0], add_to_name="_new")
        f_bot.remove_file(files_list[1])

    except Exception as e:
        logger.error(repr(e))
        if driver_type == REMOTE_DRIVER:
            f_bot.driver.quit()
    if driver_type == REMOTE_DRIVER:
        f_bot.driver.quit()
