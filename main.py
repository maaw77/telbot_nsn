import logging
import asyncio
from asyncio import Queue
from http import HTTPStatus
from pprint import pprint

import aiohttp
from aiohttp import ClientSession

from yarl import URL

from telbot import tbot
from telbot.settings import config
from telbot import msgs_mngr


URL_ZABBIX_BASE = 'http://zabbix.gmkzoloto.ru/zabbix'


class ZabbixPoller:
    def __init__(self, url: str) -> None:
        self.url_base = URL(url)
        self.url_api =  self.url_base/'api_jsonrpc.php'
        self.auth: str = '' # uthentication token
        self.id: int = 0 # an identifier of the corresponding request
    
    async def authontication(self, client: ClientSession) -> None:
        data = {"jsonrpc":"2.0",
                "method":"user.login",
                "params": {"username": config.zabbix_username.get_secret_value(),
                           "password": config.zabbix_password.get_secret_value()},
                "id":1}
        async with client.post(self.url_api, json=data) as resp:
            assert resp.status == HTTPStatus.OK
            data_for_auth = await resp.json()
            self.auth = data_for_auth['result']
            self.id = data_for_auth['id'] 
            logging.info(data_for_auth)                


    async def run(self) -> None:
        """Launch the poller"""
        async with aiohttp.ClientSession() as client:
            await self.authontication(client)
            while True:
                await asyncio.sleep(0)


async def main():
    queue_messages = Queue()  # Message queue for telegram bot.
    bot = tbot.TelBot(config.bot_token.get_secret_value(), queue_messages)
    msgs_manager = msgs_mngr.MessagesManager(queue_messages)
    zbx_plr = ZabbixPoller(URL_ZABBIX_BASE)
    coroutines = (bot.run(), msgs_manager.run(), zbx_plr.run())
    tasks = [asyncio.create_task(cor) for cor in coroutines]
    try:
        await asyncio.gather(queue_messages.join(), *tasks)
    except tbot.BotConnectionError as ex:
        logging.info(ex)
    finally:
        for tsk in tasks:
            if not tsk.done():
                tsk.cancel()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
    try:
        asyncio.run(main())
        logging.info(asyncio.run(main()))
    except KeyboardInterrupt:
        logging.info('The bot was stopped!')
