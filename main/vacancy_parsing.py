import requests
from bs4 import BeautifulSoup
import fake_useragent


def get_vacancy(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(url=f"{text}", headers={"user-agent": ua.random})
    if data.status_code != 200:
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
        main = ""

    return str(main)


if __name__ == "__main__":
    vacancy_url = input(
        "Введите URL вакансии (например, 'https://hh.ru/vacancy/84829254'): "
    )
    VACANCY = get_vacancy(vacancy_url)
