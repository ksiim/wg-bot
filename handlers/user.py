from aiogram import F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, CallbackQuery, FSInputFile
)

from bot import dp, bot

from models.dbs.orm import Orm
from models.dbs.models import *
from utils.wireguard import WireGuard

from .callbacks import *
from .markups import *
from .states import *

@dp.message(Command('start'))
async def start_message_handler(message: Message, state: FSMContext):
    await state.clear()
    
    await Orm.create_user(message)
    await send_start_message(message)
    
async def send_start_message(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=await generate_start_text(message),
    )
    
@dp.message(Command('qwe'))
async def qwe_message_handler(message: Message):
    wg = WireGuard()
    user = await Orm.get_user_by_telegram_id(message.from_user.id)
    wg.generate_server_config()
    
@dp.message(Command('asd'))
async def asd_message_handler(message: Message):
    wg = WireGuard()
    user = await Orm.get_user_by_telegram_id(message.from_user.id)
    path = wg.create_user_config(user)
    file = FSInputFile(path=path)
    await message.answer_document(file)
    