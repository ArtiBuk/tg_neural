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
from urllib.parse import unquote_plus, urlparse
import random
from fake_useragent import UserAgent


def search_google(query, limit):
    # Разделяем слова запроса и объединяем их с помощью %20
    query_words = query.split()
    # Формируем URL для запроса в Google
    url = f"https://www.google.com/search?q={'%20'.join(query_words)}"

    # Отправляем GET-запрос и получаем HTML-страницу с результатами поиска
    try:
        response = requests.get(url,headers={'User-Agent': UserAgent().googlechrome})
        response.raise_for_status()
        print(UserAgent().googlechrome)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return []

    # Используем BeautifulSoup для парсинга HTML-страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем все ссылки на странице
    links = soup.find_all('a')

    # Извлекаем ссылки и преобразуем относительные ссылки в абсолютные
    result_links = []
    count = 0
    for i, link in enumerate(links, start=1):
        href = link.get('href')
        if href and href.startswith('/url?q='):
            url = unquote_plus(href[7:])
            parsed_url = urlparse(url)
            cleaned_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            try:
                # Проверяем доступность страницы перед добавлением ссылки в результаты
                response = requests.get(cleaned_url,headers={'User-Agent': UserAgent().googlechrome})
                response.raise_for_status()
                result_links.append(cleaned_url)
                count += 1
                if count >= limit:
                    break
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при обработке ссылки: {e}")

    # Добавляем задержку в 1 секунду перед каждым запросом
    time.sleep(1)

    return result_links[:limit]


def save_page_content(url, filename):
    # Отправляем GET-запрос и получаем HTML-страницу
    try:
        response = requests.get(url,headers={'User-Agent': UserAgent().googlechrome})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return

    # Используем BeautifulSoup для парсинга HTML-страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем текст с веб-страницы и удаляем лишние разрывы
    text = soup.get_text().replace('\n\n', ' ')

    # Сохраняем текст в текстовый файл
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


# Пример использования функции
user_query = 'двенадцати струнная гитара что это такое?'
search_results = search_google(user_query, limit=2)
print(search_results)
for i, link in enumerate(search_results, start=1):
    filename = f"page_{i}.txt"
    save_page_content(link, filename)
    print(f"Страница {i} сохранена в файл {filename}")