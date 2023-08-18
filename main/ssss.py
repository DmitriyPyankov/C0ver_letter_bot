import logging
from telegram.ext import Filters
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
import openai
from config import TOKEN_TG_BOT
import config  # Предполагая, что у вас есть переменная OPENAI_API_KEY в config.py
import rezume_parsing
import vacancy_parsing

# Ваш API-ключ GPT-3
api_key = config.OPENAI_API_KEY
openai.api_key = api_key

rezume = rezume_parsing.REZUME
vacancy = vacancy_parsing.VACANCY

# Обработчик команды /start
def start(update: "telegram.Update", context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я бот для создания сопроводительных писем. Просто отправь мне ссылки на резюме и вакансию в формате:\n\n/cover_letter [ссылка на резюме] [сслылка на вакансию]")

# Обработчик команды /cover_letter
def cover_letter(update: "telegram.Update", context: CallbackContext) -> None:
    args = context.args
    if len(args) >= 2:
        rezume_description = args[0]
        vacancy_description = args[1]
        
        prompt = f"""
        Напиши сопроводительное письмо на основе описания резюме и вакансии, текст которых выделен в тройные кавычки.
        ссылка на резюме: '''{rezume_description}'''
        сслылка на вакансию: '''{vacancy_description}'''
        """
        
        response = get_completion(prompt)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Использование: /cover_letter [ссылка на резюме] [сслылка на вакансию]")

def main():
    # Инициализация бота с токеном
    updater = Updater("TOKEN_TG_BOT")
    dp = updater.dispatcher
    
    # Добавляем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cover_letter", cover_letter))
    
    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()










# def get_completion(prompt, model="gpt-3.5-turbo-16k"):
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0,
#     )
#     return response.choices[0].message["content"]


# # Ваш API-ключ GPT-3
# api_key = config.OPENAI_API_KEY
# openai.api_key = api_key

# prompt = f"""
# Напиши сопроводительное письмо на основе описания резюме и вкансии, текст которых выделен в тройные кавычки.
# ссылка на резюме: '''{rezume}'''
# сслылка на вакансию: '''{vacancy}'''
# """
# response = get_completion(prompt)
# print(response)



# https://hh.ru/resume/c25565e100075e48200039ed1f4c6269506536?hhtmFrom=resume_search_result
# https://hh.ru/vacancy/83116089?from=vacancy_search_list&query=python
