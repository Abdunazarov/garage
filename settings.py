# stdlib
import os

# thirdparty
from dotenv import load_dotenv

load_dotenv(override=True)


DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_URL_PSYCOPG2 = os.environ["DATABASE_URL_PSYCOPG2"] 