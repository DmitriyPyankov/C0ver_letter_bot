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

# Вместо этой функции, вы можете использовать свою логику для отправки сообщений
async def send_message(message: types.Message, text: str, reply_markup: types.InlineKeyboardMarkup = None):
    await message.reply(text, reply_markup=reply_markup)

@dp.message_handler(commands="start")
async def start(message: types.Message, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('FIO', callback_data='get_fio'))
    markup.add(types.InlineKeyboardButton('rezume', callback_data='get_rezume_url'))
    markup.add(types.InlineKeyboardButton('vacancy', callback_data='get_vacancy_url'))
    markup.add(types.InlineKeyboardButton('cover', callback_data='get_cover'))
    
    await send_message(message, 'Hello', reply_markup=markup)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'get_rezume_url')
async def get_rezume_callback(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    
    await send_message(query.message, '''Введите URL резюме \n(например, https://hh.ru/resume/123) :''')
    await state.set_state('waiting_for_rezume_url')

@dp.message_handler(lambda message: message.text.startswith('http'), state='waiting_for_rezume_url')
async def handle_rezume_url(message: types.Message, state: FSMContext):
    await state.finish() 
    rezume_url = message.text
    try:
        rezume_data = get_rezume(rezume_url)
        await state.update_data(rezume_data=rezume_data)
        await send_message(message, "Success saved") 
        return rezume_data
        # await send_message(message, rezume_data) 
    except Exception as e:
        await message.answer(f"Ошибка при получении данных о резюме. Пожалуйста, попробуйте снова и начните с команды /start.")
        return  

@dp.callback_query_handler(lambda c: c.data == 'get_vacancy_url')
async def get_vacancy_callback(query: types.CallbackQuery, state: FSMContext):
    await query.answer()  # Ответить на callback_query
    
    await send_message(query.message, '''Введите URL вакансии \n(например, https://hh.ru/vacancy/123) :''')
    await state.set_state('waiting_for_vacancy_url')

@dp.message_handler(lambda message: message.text.startswith('http'), state='waiting_for_vacancy_url')
async def handle_vacancy_url(message: types.Message, state: FSMContext):
    await state.finish()
    vacancy_url = message.text
    try:
        vacancy_data = get_vacancy(vacancy_url)
        await state.update_data(vacancy_data=vacancy_data)
        await send_message(message, "Success saved")
        # await send_message(message, vacancy_data)
        return vacancy_data
    except Exception as e:
        await message.answer(f"Ошибка при получении данных о вакансии. Пожалуйста, попробуйте снова и начните с команды /start.")
        return


@dp.callback_query_handler(lambda c: c.data == 'get_fio')
async def get_fio_callback(query: types.CallbackQuery, state: FSMContext):
    await query.answer()  
    
    await send_message(query.message, 'Введите свою имя и фамилию (например, Иван Иванов):')
    await state.set_state('waiting_for_fio')

@dp.message_handler(lambda message: True, state='waiting_for_fio')
async def handle_fio(message: types.Message, state: FSMContext):
    await state.finish()  
    fio = message.text
    await state.update_data(fio=fio)
    await send_message(message, f'Спасибо, вы ввели, а мы сохранили: {fio}')
    return fio

@dp.callback_query_handler(lambda c: c.data == 'get_cover')
async def get_cover_callback(query: types.CallbackQuery, state: FSMContext):
    await query.answer() 
    
    # Проверяю, что переменные не пустые
    async with state.proxy() as data:
        fio = data.get('fio')
        rezume_data = data.get('rezume_data')
        vacancy_data = data.get('vacancy_data')
        
        if fio and rezume_data and vacancy_data:
            prompt = f"""
                Напиши сопроводительное письмо на основе описания резюме и вакансии, текст которых выделен в тройные кавычки.
                моё имя: '''{fio}'''
                ссылка на резюме: '''{rezume_data}'''
                сслылка на вакансию: '''{vacancy_data}'''
                """
            response = get_completion(prompt)
            await send_message(query.message, response)
        else:
            await send_message(query.message, 'Не хватает данных для создания сопроводительного письма.')
        
    await state.finish()

@dp.message_handler()
async def undefined_message(message: types.Message):
    await message.answer(
        "Введена ерунда) \nНачните, пожалуйста, сначала. \nЧтобы начать пользоваться ботом, используйте команду /start",
        parse_mode="Markdown",
    )

if __name__ == "__main__":
    executor.start_polling(dp)
