import asyncio

from bot import dp, bot

import logging

import handlers

from utils.wireguard import WireGuard

from models.databases import create_database


logging.basicConfig(level=logging.INFO)

async def main():
    await create_database()
    wg = WireGuard()
    wg.install_wireguard()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())