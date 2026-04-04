# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of KumsalTR

import time
import logging
from logging.handlers import RotatingFileHandler

# LOGGER AYARLARI
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=10485760, backupCount=5),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.CRITICAL)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)

# HATA BURADAYDI
logger = logging.getLogger(__name__)

version = "3.0.1"

from config import Config

config = Config()
config.check()

# Plugins içindeki dosyaların LOGGER_ID kullanabilmesi için
LOGGER_ID = config.LOGGER_ID
OWNER_ID = config.OWNER_ID

tasks = []
boot = time.time()

from KumsalTR.core.bot import Bot
app = Bot()

from KumsalTR.core.dir import ensure_dirs
ensure_dirs()

from KumsalTR.core.userbot import Userbot
userbot = Userbot()

from KumsalTR.core.mongo import MongoDB
db = MongoDB()

from KumsalTR.core.lang import Language
lang = Language()

from KumsalTR.core.telegram import Telegram
from KumsalTR.core.youtube import YouTube

tg = Telegram()
yt = YouTube()

from KumsalTR.helpers import Queue
queue = Queue()

from KumsalTR.core.calls import TgCall
anon = TgCall()


async def stop() -> None:
    logger.info("Bot durduruluyor...")

    for task in tasks:
        task.cancel()
        try:
            await task
        except:
            pass

    await app.exit()
    await userbot.exit()
    await db.close()

    logger.info("Bot başarıyla durduruldu.\n")