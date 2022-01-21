import sys

from loguru import logger

from bot.bot import filter_smartphones_and_return_titles
from bot.constants import FIRST_N_PHONES


if __name__ == "__main__":
    try:
        filter_smartphones_and_return_titles(first_n=FIRST_N_PHONES)
    except Exception as e:
        logger.error(repr(e))