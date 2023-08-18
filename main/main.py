import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import openai
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


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Приветики. Я готов написать для тебя уникальное сопроводительное письмо для любой вакансии. \nВведите ссылку на ваше резюме. Например: https://hh.ru/resume/8734e61f0000f3fcf00039ed1f44455a346c36")


@dp.message_handler(regexp="https://hh\.ru/resume/.*")
async def rezume(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["rezume_url"] = message.text
    await message.answer("Введите ссылку на интересующую вас вакансию. Например, https://hh.ru/vacancy/84829254")


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
        "Чтобы начать пользоваться ботом, используйте команду /start",
        parse_mode="Markdown",
    )


if __name__ == "__main__":
    executor.start_polling(dp)


# https://hh.ru/resume/8734e61f0000f3fcf00039ed1f44455a346c36
# https://hh.ru/vacancy/84829254


# https://hh.ru/resume/c25565e100075e48200039ed1f4c6269506536?hhtmFrom=resume_search_result
# https://hh.ru/vacancy/83116089?from=vacancy_search_list&query=python
