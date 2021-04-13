import logging
import os
import sys

from telethon import TelegramClient

VERSION = "0.1"

# Module name
module = "init"

# enable logging
LOGGER = logging.getLogger(__name__)

ENV = bool(os.environ.get('ENV', False))
if ENV:
    DEBUG = os.environ.get('DEBUG', None)
else:
    from userbot.config import Development as Config
    DEBUG = Config.DEBUG

LOGFORMAT = "[%(asctime)s | %(levelname)s] %(message)s"
if DEBUG:
    logging.basicConfig(
        format=LOGFORMAT,
        level=logging.DEBUG)
else:
    logging.basicConfig(
        format=LOGFORMAT,
        level=logging.INFO)

LOGGER.info(f"OpenUserbot v{VERSION}\n"
            f"This program is free software: you can redistribute it and/or modify\n"
            f"it under the terms of the GNU General Public License as published by\n"
            f"the Free Software Foundation, either version 3 of the License, or\n"
            f"(at your option) any later version.")
# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.") # ERR_INVALID_PYTHON_VERSION
    sys.exit(1)

API_KEY = Config.API_KEY
API_HASH = Config.API_HASH
LOAD = Config.LOAD
NO_LOAD = Config.NO_LOAD

import socks as python_socks
bot = TelegramClient("userbot2", API_KEY, API_HASH, proxy=(python_socks.HTTP, '192.168.2.110', 3128))

