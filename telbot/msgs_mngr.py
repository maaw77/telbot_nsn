import logging
from random import randrange

import asyncio
from asyncio import Queue





class MessagesManager:
    """A class for creating an instance of the message manager."""
    def __init__(self, queue_msgs: Queue):
        self.queue_msgs = queue_msgs # Message queue for telegram bot.

    async def run(self) -> None:
        msgs = ('Hello, boss!', 'Hello, client!', 'Hello, coworker!', )
        users_id = ['80901973', ]
        while True:
            mess = msgs[randrange(len(msgs))]
            logging.info(mess)
            for uid in users_id:
                self.queue_msgs.put_nowait({'chat_id': uid, 'text': mess})
                await asyncio.sleep(20)
