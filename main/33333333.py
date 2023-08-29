import requests
from bs4 import BeautifulSoup
import fake_useragent

def get_vacancy(text):
    ua = fake_useragent.UserAgent()
    
    try:
        data = requests.get(url=f"{text}", headers={"user-agent": ua.random})
    except requests.exceptions.RequestException:
        print("Ошибка при выполнении запроса. Пожалуйста, проверьте внимательно вашу ссылку и сравните с образцом")
        return
    
    if data.status_code != 200:
        print("Ошибка: Страница не доступна")
        return
    
    soup = BeautifulSoup(data.content, "lxml")
    
    try:
        main = [
            info.text.replace("\xa0", " ")
            .replace("\n", ".")
            .replace("\r", "")
            .replace("\t", "")
            .replace("•", "")
            .replace("\u2009", "")
            for info in soup.find(attrs={"class": "vacancy-description"})
        ]
    except:
        raise ParsingError("Не получилось спарсить")

    if not main:
        print("Пожалуйста, проверьте внимательно вашу ссылку и сравните с образцом")
        return
    
    return str(main)

if __name__ == "__main__":
    vacancy_url = input(
        "Введите URL вакансии (например, 'https://hh.ru/vacancy/84829254'): "
    )
    VACANCY = get_vacancy(vacancy_url)
    
    if VACANCY:
        print(VACANCY)
