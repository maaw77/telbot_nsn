import logging

import asyncio
from asyncio import Queue

import aiohttp
from aiohttp import ClientSession

from yarl import URL


class BotConnectionError(Exception):
    def __str__(self):
        return 'EXCEPTION:Bot connection error!'


class TelBot:
    """A class for creating a bot instance."""
    URL_BASE = URL('https://api.telegram.org')

    def __init__(self, token: str, queue_msgs: Queue):
        self.bot_token = str(token) # A token to authorize your bot
        self.url_bot = self.URL_BASE/('bot'+self.bot_token)  # The base URL of the bot API
        self.url_check_bot = self.url_bot/'getMe' # The method for testing your bot's authentication token.
        self.url_send_message = self.url_bot/'sendMessage' #  The method of sending text messages.
        self.url_get_updates = self.url_bot/'getUpdates' # The method of receiving incoming updates.
        self.queue_msgs = queue_msgs # Message queue for telegram bot.

    # def __repr__(self):
    #     return f''

    async def check_bot_token(self, client: ClientSession) -> None:
        """Checks the connection to the bot."""
        async with client.get(self.url_check_bot) as resp:
            data = await resp.json()
            # logging.info(data)
            if data['ok'] is False:
                raise BotConnectionError

    async def send_message(self, client: ClientSession, message: dict[str, str]) -> None:
        """Send messages."""
        async with client.post(self.url_send_message, json=message) as resp:
            logging.info(await resp.json())

    async def poller(self, client: ClientSession) -> None:
        """Receive incoming updates."""
        parameters = {'offset': -1, 'timeout': 3}
        async with client.post(self.url_get_updates, json=parameters) as resp:
            logging.info(resp.json())

    async def run(self) -> None:
        """Launch the bot"""
        async with aiohttp.ClientSession() as client:
            await self.check_bot_token(client)
            # await self.send_message(client, {'chat_id': '80901973', 'text': 'Hello!'})
            # await self.poller(client)
            while True:
                if not self.queue_msgs.empty():
                    mess = self.queue_msgs.get_nowait()
                    await self.send_message(client, mess)
                    self.queue_msgs.task_done()
                await asyncio.sleep(0)
