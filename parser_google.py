import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote_plus, urlparse
from fake_useragent import UserAgent
import re


def search_google(query, limit):
    # Разделяем слова запроса и объединяем их с помощью %20
    query_words = query.split()
    # Формируем URL для запроса в Google
    url = f"https://www.google.com/search?q={'%20'.join(query_words)}"

    # Отправляем GET-запрос и получаем HTML-страницу с результатами поиска
    try:
        response = requests.get(url, headers={'User-Agent': UserAgent().googlechrome})
        response.raise_for_status()
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
                response = requests.get(cleaned_url, headers={'User-Agent': UserAgent().googlechrome})
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


def remove_links(text):
    # Удаление ссылок из текста
    text_without_links = re.sub(r"http\S+|www\S+|\S+\.\S+", "<URL>", text)
    return text_without_links


def remove_special_characters(text):
    # Удаление специальных символов
    special_characters = ["&", "=", "»"]
    for char in special_characters:
        text = text.replace(char, " ")
    return text


def remove_formatting(text):
    # Удаление форматирования
    text = text.replace("\n", " ")
    return text


def remove_extra_spaces(text):
    # Удаление лишних пробелов
    text = " ".join(text.split())
    return text


def process_text(text):
    # Приведение всех слов к нижнему регистру
    text = text.lower()
    text = remove_links(text)
    text = remove_special_characters(text)
    text = remove_formatting(text)
    text = remove_extra_spaces(text)
    return text


def save_page_content(url, filename):
    # Отправляем GET-запрос и получаем HTML-страницу
    try:
        response = requests.get(url, headers={'User-Agent': UserAgent().googlechrome})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return

    # Используем BeautifulSoup для парсинга HTML-страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем текст с веб-страницы и обрабатываем его
    text = soup.get_text()
    processed_text = process_text(text)

    # Создаем папку "text", если она не существует
    text_folder = os.path.join(os.path.dirname(__file__), 'text')
    if not os.path.exists(text_folder):
        os.makedirs(text_folder)

    # Сохраняем обработанный текст в текстовый файл в папке "text"
    with open(os.path.join(text_folder, filename), 'w', encoding='utf-8') as file:
        file.write(processed_text)


# Пример использования функции
user_query = 'значения слова привет'
search_results = search_google(user_query, limit=3)
print(search_results)
for i, link in enumerate(search_results, start=1):
    filename = f"page_{i}.txt"
    save_page_content(link, filename)
    print(f"Страница {i} сохранена в файл {filename}")