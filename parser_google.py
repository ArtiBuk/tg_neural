import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote_plus, urlparse
from fake_useragent import UserAgent
import re
import json
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from nltk.corpus import stopwords

LANGUAGE = "russian"
stemmer = Stemmer(LANGUAGE)
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
    # Удаление всех латинских символов
    text = re.sub(r'[a-zA-Z]', '', text)
    # Приведение всех слов к нижнему регистру
    text = text.lower()
    text = remove_links(text)
    text = remove_special_characters(text)
    text = remove_formatting(text)
    text = remove_extra_spaces(text)
    return text


def summarize_text(text, sentences_count):
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = set(stopwords.words('russian'))

    summary = []
    for sentence in summarizer(parser.document, sentences_count):
        summary.append(str(sentence))

    return ' '.join(summary)


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

    # Создаем выжимку текста
    summarized_text = summarize_text(processed_text, sentences_count=10)

    # Сохраняем текст в файл
    data = {"text": summarized_text}
    with open(os.path.join(text_folder, filename), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    print(f"Файл {filename} сохранен")


user_query = 'значения слова привет'
search_results = search_google(user_query, limit=4)
print(search_results)
for i, link in enumerate(search_results, start=1):
    filename = f"page_{i}.json"  # изменение расширения файла
    save_page_content(link, filename)
