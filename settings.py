import os

from dotenv import load_dotenv

load_dotenv()
db_config = {
    'dbname': os.getenv('DBNAME'),
    'user': os.getenv('USER_DB'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'port': 5432
}

URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')
