import requests
from bs4 import BeautifulSoup
import fake_useragent
from typing import List


def get_rezume(text: str) -> List[str]:
    """
    Parsing resume
    """
    ua = fake_useragent.UserAgent()
    data = requests.get(url=f"{text}", headers={"user-agent": ua.random})

    data.raise_for_status()

    soup = BeautifulSoup(data.content, "lxml")

    try:
        main = [
            info.text.replace("\xa0", " ")
            .replace("\n", ".")
            .replace("\r", "")
            .replace("\t", "")
            .replace("•", "")
            .replace("\u2009", "")
            for info in soup.find(attrs={"class": "bloko-gap bloko-gap_top"})
        ]
    except:
        main = ""

    rezume = [main[i] for i in range(len(main)) if i in [0, 1, 4, 5, 7]]

    return rezume


if __name__ == "__main__":
    rezume_url = input(
        "Введите URL резюме (например, 'https://hh.ru/resume/12345'): "
    )
    REZUME = get_rezume(rezume_url)
    print(REZUME)