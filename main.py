import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot import dp, bot

import logging

import handlers

from utils.tasks import delete_unsubscribed_people

from models.databases import create_database


logging.basicConfig(level=logging.INFO)

async def main():
    initialize_scheduler()
    await create_database()
    await dp.start_polling(bot)
    
def initialize_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(delete_unsubscribed_people, 'cron', hour=0)
    # scheduler.add_job(delete_unsubscribed_people, 'interval', seconds=10)
    scheduler.start()

if __name__ == "__main__":
    asyncio.run(main())