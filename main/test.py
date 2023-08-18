import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import openai
import re
from config import TOKEN_TG_BOT, OPENAI_API_KEY
from rezume_parsing import get_rezume
from vacancy_parsing import get_vacancy


logging.basicConfig(
    format="%(levelname)s: %(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)

bot = Bot(TOKEN_TG_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

openai.api_key = OPENAI_API_KEY


def get_completion(prompt, model="gpt-3.5-turbo-16k"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Приветики. Я готов написать для тебя уникальное сопроводительное письмо для любой вакансии. \nВведите ссылку на ваше резюме. \nНапример: https://hh.ru/resume/8734e61f0000f3fcf00039ed1f44455a346c36")
    await SomeState.first()  # Переход к первому шагу (если используете FSM)


@dp.message_handler(lambda message: not re.match(r"https://hh\.ru/resume/\S+", message.text))
async def invalid_resume_link(message: types.Message, state: FSMContext):
    await message.answer("Ошибка: Некорректный формат ссылки на резюме. Пожалуйста, введите ссылку правильно.")
    await SomeState.first()  # Возвращаемся к началу шага ввода ссылки на резюме


@dp.message_handler(regexp=r"https://hh\.ru/resume/\S+")
async def rezume(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["rezume_url"] = message.text

    rezume_url = message.text
    rezume = get_rezume(rezume_url)
    if not rezume:
        await message.answer("Ошибка: Резюме не может быть обработано. Пожалуйста, попробуйте снова.")
        return

    async with state.proxy() as data:
        data["rezume_data"] = rezume

    await message.answer("Введите ссылку на интересующую вас вакансию. Например, https://hh.ru/vacancy/84829254")
    await SomeState.next()  # Переход к следующему шагу (если используете FSM)

@dp.message_handler(regexp="https://hh\.ru/vacancy/.*")
async def vacancy(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        rezume_url = data["rezume_url"]
    vacancy_url = message.text
    await message.answer("Пишу для вас сопроводительное письмо...")

    rezume = get_rezume(rezume_url)
    vacancy = get_vacancy(vacancy_url)

    prompt = f"""
    Напиши сопроводительное письмо на основе описания резюме и вакансии, текст которых выделен в тройные кавычки.
    ссылка на резюме: '''{rezume}'''
    сслылка на вакансию: '''{vacancy}'''
    """
    response = get_completion(prompt)
    await message.answer(response)
    await state.finish()


@dp.message_handler()
async def undefined_message(message: types.Message):
    await message.answer(
        "Введена ерунда) \nНачните, пожалуйста, сначала. \nЧтобы начать пользоваться ботом, используйте команду /start",
        parse_mode="Markdown",
    )


if __name__ == "__main__":
    executor.start_polling(dp)