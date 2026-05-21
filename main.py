import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

TOKEN = os.getenv('BOT_AUTH_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="👍 Like", callback_data="btn_like"),
        InlineKeyboardButton(text="👎 Dislike", callback_data="btn_dislike")
    ],
    [
        InlineKeyboardButton(text="Visit Website", url="https://example.com")
    ]
])

reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Авторизироваться", request_location=True)],
        [KeyboardButton(text="Выйти")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Здравствуйте, {message.from_user.full_name}! Выберите опцию:",
        reply_markup=reply_kb
    )

@router.message(F.text == "Выйти")
async def hide_keyboard(message: Message) -> None:
    from aiogram.types import ReplyKeyboardRemove
    await ReplyKeyboardRemove()



@router.message()
async def send_inline_buttons(message: Message) -> None:
    """Fallback handler that sends inline buttons for any text message."""
    await message.answer("Here are some inline buttons:", reply_markup=inline_kb)


@router.callback_query(F.data.startswith("btn_"))
async def handle_inline_buttons(callback: CallbackQuery) -> None:
    if callback.data == "btn_like":
        await callback.answer("You liked it! 👍")
        await callback.message.edit_text("You clicked: Like 👍")
    elif callback.data == "btn_dislike":
        await callback.answer("You disliked it! 👎")
        await callback.message.edit_text("You clicked: Dislike 👎")


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
