# Import Library 
import openai  
import time
import requests
from bs4 import BeautifulSoup
import fake_useragent
import requests


def get_completion(prompt, model="gpt-3.5-turbo-16k"):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0,
    )
    return response.choices[0].text


def get_rezume(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=f'{text}',
        headers={'user-agent': ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')

    try:
        main = [info.text.replace('\xa0', ' ').replace('\n', '.').replace('\r', '').replace('\t', '').replace('•', '').replace('\u2009', '') for info in soup.find(attrs={'class': 'bloko-gap bloko-gap_top'})]
    except:
        main = ''

    return main

if __name__ == '__main__':
    # rezume = get_rezume('9c60df860004d3a9150039ed1f456168487a33')
    rezume_url = input("Введите URL резюме (например, 'https://hh.ru/resume/8734e61f0000f3fcf00039ed1f44455a346c36'): ")
    rezume = get_rezume(rezume_url)
    middle_index = len(rezume) // 2
    first_part = " ".join(rezume[:middle_index-3])
    second_part = " ".join(rezume[middle_index-3:])

    del rezume

def get_vacancy(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=f'{text}',
        headers={'user-agent': ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')

    try:
        main = [info.text.replace('\xa0', ' ').replace('\n', '.').replace('\r', '').replace('\t', '').replace('•', '').replace('\u2009', '') for info in soup.find(attrs={'class': 'vacancy-description'})]
    except:
        main = ''

    return str(main)

if __name__ == '__main__':
    vacancy_url = input("Введите URL вакансии (например, 'https://hh.ru/vacancy/84829254'): ")
    vacancy = get_vacancy(vacancy_url)

# Ваш API-ключ GPT-3
api_key = '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'
openai.api_key  = api_key















# prompt_1 = f"""
# Напиши сопроводительное письмо на основе описания резюме и вкансии.
# Я предоставлю текст по частям. Пожалуйста, выдайте ответ после того, как я скажу 'КОНЕЦ'
# Описание резюме, 1 часть: '''{first_part}'''
# """
# # response_1 = get_completion(prompt_1)
# prompt_2 = f"""
# Описание резюме, 2 часть: '''{second_part}'''
# """
# response_2 = get_completion(prompt_2)
# prompt_3 = f"""
# Описание вакансии: '{vacancy}'. КОНЕЦ
# """
# # response_3 = get_completion(prompt_3)
# # print(response_1+response_2+response_3)

# response_1 = get_completion(prompt_1)
# print("Response 1:", response_1)

# time.sleep(10)

# response_2 = get_completion(prompt_2)
# print("Response 2:", response_2)

# time.sleep(10)

# response_3 = get_completion(prompt_3)
# print("Response 3:", response_3)

