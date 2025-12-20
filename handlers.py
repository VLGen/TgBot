from aiogram import types, F
from aiogram.filters.command import Command
from keyboards import generate_options_keyboard, start_keyboard
from quiz_data import quiz_data
from database import get_quiz_index, update_quiz_index, get_user_score, update_user_score

async def get_question(message: types.Message, user_id: int):
    current_index = await get_quiz_index(user_id)
    opts = quiz_data[current_index]['options']
    keyboard = generate_options_keyboard(opts)
    await message.answer(quiz_data[current_index]['question'], reply_markup=keyboard)

async def new_quiz(message):
    user_id = message.from_user.id
    new_score = 0
    await update_user_score(user_id, new_score)
    await update_quiz_index(user_id, 0)
    await get_question(message, user_id)

def register_handlers(dp):

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer("Добро пожаловать в квиз!", reply_markup=start_keyboard())

    @dp.message(F.text == "Начать игру!")
    @dp.message(Command("quiz"))
    async def cmd_quiz(message: types.Message):
        await message.answer("Давайте начнем!")
        await new_quiz(message)

    # Метод проверки правильного ответа
    @dp.callback_query()
    async def process_answer(callback: types.CallbackQuery):

        await callback.bot.edit_message_reply_markup( # type: ignore
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id, # type: ignore
            reply_markup=None
        )

        user_choice = callback.data
        await callback.message.answer(user_choice) # type: ignore

        current_question_index = await get_quiz_index(callback.from_user.id)
        current_score = await get_user_score(callback.from_user.id)
        correct_option = quiz_data[current_question_index]["options"][quiz_data[current_question_index]["correct_option"]]

        if user_choice == correct_option:
            await callback.message.answer("Верно!") # type: ignore
            current_score += 1
        else:
            await callback.message.answer( # type: ignore
            f"Неправильно. Правильный ответ: {correct_option}"
        )
            
        current_question_index += 1
        await update_quiz_index(callback.from_user.id, current_question_index)
        await update_user_score(callback.from_user.id, current_score)

        if current_question_index < len(quiz_data):
            await get_question(callback.message, callback.from_user.id) # type: ignore
        else:
            await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nКоличество правильных ответов: {current_score}.") # type: ignore
