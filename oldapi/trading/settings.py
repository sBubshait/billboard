from __future__ import annotations

from dotenv import load_dotenv

import os

load_dotenv()


HTTP_PORT = os.environ["HTTP_PORT"]
HTTP_HOST = os.environ["HTTP_HOST"]

WS_PORT = os.environ["WS_PORT"]

MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_PORT = os.environ["MYSQL_PORT"]
MYSQL_USER = os.environ["MYSQL_USER"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_DB = os.environ["MYSQL_DB"]
