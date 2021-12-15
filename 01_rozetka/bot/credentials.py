import os

from dotenv import load_dotenv


load_dotenv(os.path.join(os.getcwd(), '.env'))
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")
