import asyncio
import aiohttp
import yarl

import logging

URL_BASE = 'http://zabbix.gmkzoloto.ru/zabbix'

class ZabbixPoller:
    def __init__(self, url: str) -> None:
        self.url_base = yarl.URL(url)
    
    def __repr__(self) -> str:
        return f'ZabbixPoller<url={self.url_base!s}>'

async def main():
    zb = ZabbixPoller(URL_BASE)    
    print(zb)
    return True


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
    try:
        logging.info(asyncio.run(main()))
    except KeyboardInterrupt:
        logging.info('The bot was stopped!')
