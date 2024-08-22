# import asyncio
# import aiohttp
# import yarl
#
# import logging
#
# URL_BASE = 'http://zabbix.gmkzoloto.ru/zabbix'
#
#
# class ZabbixPoller:
#     def __init__(self, url: str) -> None:
#         self.url_base = yarl.URL(url)
#
#     def __repr__(self) -> str:
#         return f'ZabbixPoller<url={self.url_base!s}>'
#
#
# async def main():
#     zb = ZabbixPoller(URL_BASE)
#     print(zb)
#     return True


import logging
import asyncio
from asyncio import Queue

from pprint import pprint

import aiohttp
from aiohttp import ClientSession

from yarl import URL

from telbot import tbot
from telbot.settings import config
from telbot import msgs_mngr





async def main():
    queue_messages = Queue()  # Message queue for telegram bot.
    bot = tbot.TelBot(config.bot_token.get_secret_value(), queue_messages)
    msgs_manager = msgs_mngr.MessagesManager(queue_messages)

    coroutines = (bot.run(), msgs_manager.run(), )
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
