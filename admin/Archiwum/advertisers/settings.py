from __future__ import annotations

from dotenv import load_dotenv

import os

load_dotenv()

HTTP_PORT = int(os.getenv("HTTP_PORT", "5000"))
HTTP_HOST = os.getenv("HTTP_HOST", "0.0.0.0")

API_URL = os.getenv("API_URL", "https://api.c4s.lol/api")
