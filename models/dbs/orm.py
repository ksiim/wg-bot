import asyncio

from models.databases import Session
from models.dbs.models import *

from sqlalchemy import insert, inspect, or_, select, text, update


class Orm:
    
    @staticmethod
    async def kill_date(telegram_id):
        async with Session() as session:
            query = (
                update(User)
                .where(User.telegram_id == telegram_id)
                .values(end_of_subscription=datetime.datetime.now() - datetime.timedelta(days=365))
            )
            await session.execute(query)
            await session.commit()
    
    @staticmethod
    async def unsubscribe_user(telegram_id):
        async with Session() as session:
            query = (
                update(User)
                .where(User.telegram_id == telegram_id)
                .values(subscription=False)
                .values(end_of_subscription=None)
            )
            await session.execute(query)
            await session.commit()
    
    @staticmethod
    async def get_users_with_ended_subscription():
        async with Session() as session:
            query = (
                select(User)
                .where(User.subscription == True)
                .where(User.end_of_subscription < datetime.datetime.now())
            )
            users = (await session.execute(query)).scalars().all()
            return users
    
    @staticmethod
    async def get_end_of_subscription(telegram_id):
        async with Session() as session:
            query = (
                select(User.end_of_subscription)
                .where(User.telegram_id == telegram_id)
            )
            end_of_subscription = (await session.execute(query)).scalar_one_or_none()
            return end_of_subscription
    
    @staticmethod
    async def add_subscription_months(telegram_id, months):
        subscription_end_date = await Orm.get_end_of_subscription(telegram_id)
        result = 'renew'
        if subscription_end_date is None or subscription_end_date < datetime.datetime.now():
            subscription_end_date = datetime.datetime.now()
            result = 'new'
        async with Session() as session:
            query = (
                update(User)
                .where(User.telegram_id == telegram_id)
                .values(end_of_subscription=subscription_end_date + datetime.timedelta(days=30 * int(months)))
                .values(subscription=True)
            )
            await session.execute(query)
            await session.commit()
        return result
    
    @staticmethod
    async def update_public_key(user_id, public_key):
        async with Session() as session:
            query = (
                update(User)
                .where(User.id == user_id)
                .values(public_key=public_key)
            )
            await session.execute(query)
            await session.commit()
    
    @staticmethod
    async def create_user(message):
        if await Orm.get_user_by_telegram_id(message.from_user.id) is None:
            async with Session() as session:
                user = User(
                    full_name=message.from_user.full_name,
                    telegram_id=message.from_user.id,
                    username=message.from_user.username
                )
                session.add(user)
                await session.commit()
    
    @staticmethod
    async def get_user_by_telegram_id(telegram_id):
        async with Session() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            user = (await session.execute(query)).scalar_one_or_none()
            return user
    
    @staticmethod
    async def get_all_users():
        async with Session() as session:
            query = select(User)
            users = (await session.execute(query)).scalars().all()
            return users
        