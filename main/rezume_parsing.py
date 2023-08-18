import requests
from bs4 import BeautifulSoup
import fake_useragent
import time

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

    rezume = [main[i] for i in range(len(main)) if i in [0, 1, 4, 5, 7]]

    return rezume

rezume_url = input("Введите URL резюме (например, 'https://hh.ru/resume/8734e61f0000f3fcf00039ed1f44455a346c36'): ")
REZUME = get_rezume(rezume_url)


