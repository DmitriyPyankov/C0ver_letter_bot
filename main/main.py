import logging
import re
import os
from typing import Any, Dict

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import openai

from rezume_parsing import get_rezume
from vacancy_parsing import get_vacancy

TOKEN_TG_BOT = os.environ.get("TOKEN_TG_BOT")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = Bot(token=TOKEN_TG_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

openai.api_key = OPENAI_API_KEY


class Data(StatesGroup):
    resume = State()
    vacancy = State()
    fio = State()


def get_completion(prompt: str, model: str = "gpt-3.5-turbo-16k") -> str:
    """
    Function for using the openai API model "gpt-3.5-turbo-16k"
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


@dp.message_handler(commands="start")
async def start(message: types.Message, state: FSMContext):
    """
    The starting function for the introduction of the fio
    """
    await state.set_state(Data.fio)
    await message.answer("Привет! Я готов написать для Вас уникальное сопроводительное письмо для любой вакансии. \n\nМеня в любой момент можно прервать командой /cancel\n\nВведите, как к Вам можно обращаться. \nНапример: Иван Иванов")


@dp.message_handler(commands=['cancel'], state='*')
@dp.message_handler(lambda message: message.text.lower() == 'cancel', state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.finish()
    await message.answer('Создание сопроводительного письма прервано. Чтобы начать заново, воспользуйтесь командой /start.')


@dp.message_handler(lambda message: re.match(r'[^а-яА-ЯёЁ\']', message.text), state=Data.fio)
async def process_failed_resume(message: types.Message):
    """
    If FIO is invalid
    """
    return await message.reply("Неверный формат ФИО. Введите корректные данные.")


@dp.message_handler(state=Data.fio)
async def process_resume(message: types.Message, state: FSMContext):
    """
    Parsing resume
    """
    fio = message.text.strip()    

    async with state.proxy() as data:
        data["fio"] = fio
    
    await state.set_state(Data.resume)
    await message.answer('Введите ссылку на ваше резюме. Например: https://hh.ru/resume/12345"')

@dp.message_handler(lambda message: not re.match(r'https://.*hh\.ru/resume/.*', message.text), state=Data.resume)
async def process_failed_resume(message: types.Message):
    """
    If resume url is invalid
    """
    return await message.reply("Неверный формат ссылки на резюме. Введите корректную ссылку.")


@dp.message_handler(state=Data.resume)
async def process_resume(message: types.Message, state: FSMContext):
    """
    Parsing resume
    """
    resume_url = message.text.strip()    
    try:
        resume = get_rezume(resume_url)
    except Exception:
        return await message.reply(f"Не удалось распарсить резюме. Введите другую ссылку.")

    async with state.proxy() as data:
        data["resume_data"] = resume
        data["resume_url"] = resume_url
    
    await state.set_state(Data.vacancy)
    await message.answer('Введите ссылку на вакансию. Например, https://hh.ru/vacancy/12345')


@dp.message_handler(lambda message: not re.match(r'https://.*hh\.ru/vacancy/.*', message.text), state=Data.vacancy)
async def process_failed_vacancy(message: types.Message):
    """
    If vacancy url is invalid
    """
    return await message.reply("Неверный формат ссылки на вакансию. Введите корректную ссылку.")


@dp.message_handler(state=Data.vacancy)
async def process_vacancy(message: types.Message, state: FSMContext):
    """
    Parsing vacanty
    """
    vacancy_url = message.text.strip()
    try:
        vacancy = get_vacancy(vacancy_url)
    except Exception:
        return await message.reply(f"Не удалось распарсить вакансию. Введите другую ссылку.")

    async with state.proxy() as data:
        data["vacacny_data"] = vacancy
        data["vacancy_url"] = vacancy_url
    
    await message.answer("Пишу сопроводительное письмо...")
    try:
        await get_covering_letter(message=message, data=await state.get_data())
    except Exception:
        await message.answer("Что-то пошло не так...")

    await state.finish()
    await message.answer("Чтобы начать заново, воспользуйтесь командой /start.")


async def get_covering_letter(message: types.Message, data: Dict[str, Any]):
    """
    Func for function openai's request
    """
    fio = data.get('fio')
    resume_data = data.get('resume_data')
    vacancy_data = data.get('vacancy_data')
    prompt = f"""
        Напиши сопроводительное письмо на основе описания резюме и вакансии, текст которых выделен в тройные кавычки.
        Меня зовут: '''{fio}'''
        Текст резюме: '''{resume_data}'''
        Текст вакансии: '''{vacancy_data}'''
        """
    response = get_completion(prompt)
    await message.answer(response)


@dp.message_handler()
async def undefined_message(message: types.Message):
    """
    Func for trash random text
    """
    await message.answer(
        "Введена ерунда) \nНачните, пожалуйста, сначала. \nЧтобы начать пользоваться ботом, используйте команду /start",
        parse_mode="Markdown",
    )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s: %(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level=logging.INFO,
    )
    executor.start_polling(dp)