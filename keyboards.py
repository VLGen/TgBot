from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# Функция генерации инлайн кнопок 
def generate_options_keyboard(answer_options):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=option
        ))
    builder.adjust(1)
    return builder.as_markup()

# Функция создания начальной кнопки
def start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру!"))
    return builder.as_markup(resize_keyboard=True)
