import time
import requests
from bs4 import BeautifulSoup

def search_yandex(query):
    # Разделяем слова запроса и объединяем их с помощью %20
    query_words = query.split()
    url_query = '%20'.join(query_words)

    # Формируем URL для запроса в Яндекс
    url = f'https://yandex.ru/search/?text={url_query}&lr=213'

    # Отправляем GET-запрос и получаем HTML-страницу с результатами поиска
    response = requests.get(url)
    response.raise_for_status()

    # Используем BeautifulSoup для парсинга HTML-страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем все ссылки на странице
    links = soup.find_all('a')

    # Извлекаем первые 5 ссылок и сохраняем их в список
    result_links = []
    for link in links[:10]:
        result_links.append(link['href'])

    # Добавляем задержку в 1 секунду перед каждым запросом
    time.sleep(1)

    return result_links

# Пример использования функции
# user_query = 'как стать бэкенд-разработчиком'
# search_results = search_yandex(user_query)
# for link in search_results:
#     print(link)