from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from bot import bot

from .callbacks import *


prices = {
    1: 170,
    3: 500,
    12: 2000
}

help_photo = 'AgACAgIAAxkBAAMDZy5T-bGJZVGVUA82sgFlu9onWJ0AApTkMRthjnFJBFmGReZetXoBAAMCAANtAAM2BA'

choose_type_of_subscription_text = "Выберите тип подписки:"
choose_period_of_renew_text = "Выберите срок продления:"
help_text = """Для работы VPN необходимо скачать WireGuard приложение из Google Play / App Store, также приложение есть на ПК.

Открыть приложение WireGuard и нажать кнопку «+», далее «импорт из файла или архива» выбрать ранее полученный файл от бота после покупки подписки. Для выключения или включения VPN нажимайте на ползунок.

При возникновении проблем свяжитесь с поддержкой @Lim148."""

async def generate_start_text(message):
    return f"Чем могу помочь?"

async def incline_by_period(period):
    if period == 1:
        return "месяц"
    elif period in (2, 3, 4):
        return "месяца"
    else:
        return "месяцев"
    
async def generate_payment_keyboard(payment_link: str, payment_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оплатить",
                    url=payment_link,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Проверить оплату/Получить VPN",
                    callback_data=f"check_payment:{payment_id}"
                )
            ]
        ]
    )

choose_type_of_subscription_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'Купить на 1 месяц (Германия) - {prices[1]}р',
                callback_data='buy_vpn_:1'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'Купить на 3 месяца (Германия) - {prices[3]}р',
                callback_data='buy_vpn_:3'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'Купить на год (Германия) - {prices[12]}р',
                callback_data='buy_vpn_:12'
            )
        ],
        [
            InlineKeyboardButton(
                text='Главное меню',
                callback_data='main_menu'
            )
        ]
    ]
)

choose_perdiod_of_renew_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'Продлить на 1 месяц (Германия) - {prices[1]}р',
                callback_data='renew_vpn_:1'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'Продлить на 3 месяца (Германия) - {prices[3]}р',
                callback_data='renew_vpn_:3'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'Продлить на год (Германия) - {prices[12]}р',
                callback_data='renew_vpn_:12'
            )
        ],
        [
            InlineKeyboardButton(
                text='Главное меню',
                callback_data='main_menu'
            )
        ]
    ]
)

start_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Купить подписку VPN ",
                callback_data='buy_vpn'
            )
        ],
        [
            InlineKeyboardButton(
                text="Продлить подписку",
                callback_data='renew_vpn'
            )
        ],
        [
            InlineKeyboardButton(
                text='Помощь/как пользоваться',
                callback_data='help'
            )
        ],
        [
            InlineKeyboardButton(
                text='Моя подписка',
                callback_data='my_subscription'
            )
        ]
    ]
)

main_menu_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Главное меню',
                callback_data='main_menu'
            )
        ]
    ]
)