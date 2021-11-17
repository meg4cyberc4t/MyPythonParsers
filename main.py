import requests
from bs4 import BeautifulSoup
import os
import datetime
import re

def getDataFromSport(site):
    response = requests.get(site)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            quotes = soup.find_all('div', class_='text-article__inside')
            data = quotes[0].text.replace('\xa0', ' ')
            data = data.replace('\n', ' ')
            data = re.sub(r"\s{2,}", "", data)
            data = re.sub(r'(?<=[.])(?=[^\s])', r' ', data)
            return data
        except:
            pass
    return ''


# https://iz.ru/{i}' для политики 1249839
# https://3dnews.ru/{i}/ для техники 1053916
maxValue = 1249839
def main():
    filename = "politics.txt"
    with open(filename, "w") as file:
        counter200 = 0
        counter404 = 0
        timeStart = datetime.datetime.now()
        for i in range(maxValue-4, maxValue-400, -1):
            data = getDataFromSport(f'https://iz.ru/{i}')
            if data != '':
                file.write(" "+data)
                counter200 += 1
            else:
                counter404 += 1
            os.system('clear')
            print(f'---- {timeStart} ----')
            print(f'---- {datetime.datetime.now()} ----')
            print('Удачные сайты:', counter200)
            print('Неудачные сайты:', counter404)
            print('Всего', counter200+ counter404, 'из', maxValue)
            print('Вес:')
            print(os.stat(filename).st_size / 1000000, 'мегабайт')

if __name__ == "__main__":
    main()
