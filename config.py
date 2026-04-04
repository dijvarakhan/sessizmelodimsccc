# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.API_ID = int(getenv("API_ID", "38168684"))
        self.API_HASH = getenv("API_HASH", "e29dd7af9cac399bfbc003a4c60a23b6")

        self.BOT_TOKEN = getenv("BOT_TOKEN", "8441056561:AAFhSeSQ49OoXZiuipYD-J94xjgjISd4KS0")
        self.MONGO_URL = getenv("MONGO_URL", "mongodb+srv://mongoguess:guessmongo@cluster0.zcwklzz.mongodb.net/?retryWrites=true&w=majority")

        self.LOGGER_ID = int(getenv("LOGGER_ID", "-1003639948579"))
        self.OWNER_ID = int(getenv("OWNER_ID", "8237345360"))

        self.DURATION_LIMIT = int(getenv("DURATION_LIMIT", 180)) * 60
        self.QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", 50))
        self.PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", 20))

        self.SESSION1 = getenv("SESSION", "BAJGaGwAB5mNIrS4H9VhhhjrGbeTsimp032-F152bC0pvKT0ACH0PYCbHSd9KYff_uCcZ6ocK914bSKAXNGrvRFATEADUgfMEdZ0ulRs-ahrdY2U05nBP8eSLSqRUk2qU1od8W5wP3a8uT-Ut5XIgM9MP3ZIUMYxfyw7qzCu0rl1LJPGHOdghEcKYSZFG7GDFGTZciB90-oXX_tAN5-Nghq61Gh-udGrkJeF3v_XMSaI-AmkOrEpuxf2uYEco8LLFuvAQmuARJgFN8Ev1zqqy7wwL7YFEWXaJGoLEDuDJwEmsA4COeQFsODpy8pDvcIzTMrPnJgH1NwT7xLucWXzPr9q2eL4BAAAAAH8BwLoAA")
        self.SESSION2 = getenv("SESSION2", None)
        self.SESSION3 = getenv("SESSION3", None)

        self.SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/grupgirdap")
        self.SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/grupgirdap")

        def parse_bool(key: str, default: bool) -> bool:
            val = getenv(key)
            if val is None:
                return default
            return str(val).lower() in ["true", "1", "yes"]

        self.AUTO_END: bool = parse_bool("AUTO_END", False)
        self.AUTO_LEAVE: bool = parse_bool("AUTO_LEAVE", False)
        self.VIDEO_PLAY: bool = parse_bool("VIDEO_PLAY", True)
        self.COOKIES_URL = [
            url for url in getenv("COOKIES_URL", "https://batbin.me/spongioblastic").split(" ")
            if url and "batbin.me" in url
        ]
        self.DEFAULT_THUMB = getenv("DEFAULT_THUMB", "https://te.legra.ph/file/3e40a408286d4eda24191.jpg")
        self.PING_IMG = getenv("PING_IMG", self.DEFAULT_THUMB) or self.DEFAULT_THUMB
        self.START_IMG = getenv("START_IMG", self.DEFAULT_THUMB) or self.DEFAULT_THUMB

    def check(self):
        missing = [
            var
            for var in ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "LOGGER_ID", "OWNER_ID", "SESSION1"]
            if not getattr(self, var)
        ]
        if missing:
            raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")
