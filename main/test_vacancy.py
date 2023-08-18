import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json

def get_rezume(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=f'{text}',
        headers={'user-agent':ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')

    try:
        # main = soup.find(attrs={'class': 'bloko-gap bloko-gap_top'}).text
        main = [info.text.replace('\xa0', ' ').replace('\n', '.').replace('\r', '').replace('\t', '').replace('•', '').replace('\u2009', '') for info in soup.find(attrs={'class': 'bloko-gap bloko-gap_top'})]
    except:
        main = ''

    resume = {
        'main':main
    }
    return resume

if __name__ == '__main__':
    rezume = get_rezume('https://hh.ru/resume/9c60df860004d3a9150039ed1f456168487a33')
                        # 'https://hh.ru/resume/'
    print(rezume)


