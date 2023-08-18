import openai  
import main.rezume_parsing as rezume_parsing
import rezume_parsing
import vacancy_parsing 
import config

rezume = rezume_parsing.REZUME
vacancy = vacancy_parsing.VACANCY


def get_completion(prompt, model="gpt-3.5-turbo-16k"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


# Ваш API-ключ GPT-3
api_key = config.OPENAI_API_KEY
openai.api_key = api_key

prompt = f"""
Напиши сопроводительное письмо на основе описания резюме и вкансии, текст которых выделен в тройные кавычки.
Описание резюме: '''{rezume}'''
Описание вакансии: '''{vacancy}'''
"""
response = get_completion(prompt)
print(response)