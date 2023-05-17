# import time
# import requests
# from bs4 import BeautifulSoup
# import webbrowser

# def search_yandex(query):
#     # Разделяем слова запроса и объединяем их с помощью %20
#     query_words = query.split()
#     url_query = '%20'.join(query_words)

#     # Формируем URL для запроса в Яндекс
#     url = f'https://www.google.ru/search?q={url_query}'

#     # Открываем страницу поиска в браузере
#     webbrowser.open(url)

#     # Добавляем задержку в 1 секунду перед каждым запросом
#     time.sleep(1)

#     # Возвращаем URL страницы поиска
#     return url

# # Пример использования функции
# user_query = 'как стать бэкенд-разработчиком'
# search_url = search_yandex(user_query)
# print("Открыта страница поиска:", search_url)

import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

def search_google(query, limit):
    # Разделяем слова запроса и объединяем их с помощью %20
    query_words = query.split()

    # Формируем URL для запроса в Google
    url = f"https://www.google.com/search?q={' '.join(query_words)}"

    # Отправляем GET-запрос и получаем HTML-страницу с результатами поиска
    response = requests.get(url)
    response.raise_for_status()

    # Используем BeautifulSoup для парсинга HTML-страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем все ссылки на странице
    links = soup.find_all('a')

    # Извлекаем ссылки и преобразуем относительные ссылки в абсолютные
    result_links = []
    count = 0
    for i, link in enumerate(links, start=1):
        href = link.get('href')
        if href.startswith('/url?q='):
            url = unquote(href[7:])
            result_links.append(f"{i}. {url}")
            count += 1
            if count >= limit:
                break

    # Добавляем задержку в 1 секунду перед каждым запросом
    time.sleep(1)

    return result_links[:limit]

# Пример использования функции
# user_query = 'как стать бэкенд-разработчиком'
# search_results = search_google(user_query, limit=3)
# for link in search_results:
#     print(link)
