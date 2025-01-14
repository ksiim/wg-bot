from aiogram import F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, CallbackQuery, FSInputFile
)
from sqlalchemy import delete

from bot import dp, bot

from models.dbs.orm import Orm
from models.dbs.models import *
from utils.wireguard import WireGuard

from .callbacks import *
from .markups import *
from .states import *


@dp.message(F.photo)
async def photo_handler(message: Message):
    await message.answer(
        text=f"<code>{message.photo[-1].file_id}</code>"
    )


@dp.message(Command('start'))
async def start_message_handler(message: Message, state: FSMContext):
    await state.clear()

    await Orm.create_user(message)
    await send_start_message(message)


@dp.callback_query(F.data == "main_menu")
async def main_menu_callback_handler(callback: CallbackQuery):
    await callback.message.answer(
        text="Главное меню",
        reply_markup=start_markup
    )


async def send_start_message(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=await generate_start_text(message),
        reply_markup=start_markup
    )


@dp.callback_query(F.data == "buy_vpn")
async def buy_vpn_callback(callback: CallbackQuery):
    await callback.message.answer(
        text=choose_type_of_subscription_text,
        reply_markup=choose_type_of_subscription_markup
    )


@dp.callback_query(F.data == "renew_vpn")
async def renew_vpn_callback(callback: CallbackQuery):
    await callback.message.answer(
        text=choose_period_of_renew_text,
        reply_markup=choose_perdiod_of_renew_markup
    )


@dp.callback_query(F.data == "help")
async def help_callback_handler(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo=help_photo,
        caption=help_text,
        reply_markup=main_menu_markup
    )


@dp.callback_query(F.data == "my_subscription")
async def my_subscription_callback_handler(callback: CallbackQuery):
    end_of_subscription_date = await Orm.get_end_of_subscription(callback.from_user.id)
    user = await Orm.get_user_by_telegram_id(callback.from_user.id)
    wg = WireGuard()
    user_config_path = wg.get_user_config_path(user)
    if end_of_subscription_date:
        text = f"Ваша подписка активна до {end_of_subscription_date.strftime('%d.%m.%Y')}"
        await callback.message.answer_document(
            document=FSInputFile(user_config_path),
            caption=text,
            reply_markup=main_menu_markup
        )
    else:
        text = 'Похоже у вас еще нет подписки'
        await callback.message.answer(
            text=text,
            reply_markup=main_menu_markup
        )


@dp.message(Command('qwe'))
async def qwe_message(message: Message):
    await Orm.kill_date(message.from_user.id)

# @dp.message(Command('asd'))
# async def asd_message_handler(message: Message):
#     wg = WireGuard()
#     user = await Orm.get_user_by_telegram_id(message.from_user.id)
#     path, public_key = wg.create_user_config(user)
#     await Orm.update_public_key(user.id, public_key)
#     file = FSInputFile(path=path)
#     await message.answer_document(file)
#     wg.delete_user_config(user)

# @dp.message(Command('zxc'))
# async def zxc_message_handler(message: Message):
#     wg = WireGuard()
#     user = await Orm.get_user_by_telegram_id(message.from_user.id)
#     user_public_key = user.public_key
#     wg.remove_peer_from_server_config(user_public_key)
