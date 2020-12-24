"""telegram user bot."""

import asyncio
import logging
import json
import socks
import sys
from configparser import ConfigParser
from os import listdir, path

from telethon import TelegramClient


class CheckInBot:
    """telegram user bot class."""

    def __init__(self):
        """init the userbot."""

        self.logger = logging.getLogger("userbot")
        config = ConfigParser()
        config.read(path.join(path.dirname(__file__), "config.ini"))

        for configsection in config:
            if ("api_id" in config[configsection] and
                "api_hash" in config[configsection]):
                self.api_id = config[configsection]["api_id"]
                self.api_hash = config[configsection]["api_hash"]
                self.name = configsection
            elif "bots" in config[configsection]:
                self.bots = json.loads(config.get("checkin", "bots"))
            elif configsection == "DEFAULT":
                continue
            else:
                self.logger.warning(f"Invalid configration in {configsection}")

        try:
            self.client = TelegramClient(self.name, self.api_id, self.api_hash, proxy=(socks.SOCKS5, "127.0.0.1", 10890, True))
        except (NameError, AttributeError):
            raise ValueError("Invalid configration: need api_id and api_hash")

    async def async_init(self):
        self.logger.info(f"Starting userbot {self.name}")
        self.userbot = await self.client.start()

    async def send_checkin_to_bots(self):
        # wait for all client.send_message to complete
        await asyncio.wait([
            self.userbot.send_message(bot, '/checkin')
            for bot in self.bots
        ])

    async def disconnect(self):
        await self.userbot.disconnect()


async def main():
    bot = CheckInBot()
    await bot.async_init()
    await bot.send_checkin_to_bots()
    await bot.disconnect()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())
