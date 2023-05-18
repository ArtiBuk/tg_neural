import os
import torch
from transformers import BertTokenizer, BertModel

# Загрузка предварительно обученной модели BERT
model_name = 'bert-base-multilingual-cased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Путь к папке с входными файлами
input_folder = 'text'
# Путь к папке для сохранения результатов
output_folder = 'result'

# Функция для реферирования текста
def summarize(text):
    # Токенизация текста
    encoded_inputs = tokenizer.encode_plus(
        text,
        padding=True,
        truncation=True,
        return_tensors='pt'
    )
    
    # Предсказание скрытых представлений с помощью модели BERT
    with torch.no_grad():
        outputs = model(**encoded_inputs)
        hidden_states = outputs.last_hidden_state
    
    # Суммирование скрытых представлений
    summarized_vector = torch.mean(hidden_states, dim=1)
    
    # Декодирование обобщающего текста из скрытого представления
    decoded_summary = tokenizer.decode(
        summarized_vector.squeeze().tolist(),
        skip_special_tokens=True
    )
    
    return decoded_summary

# Получение списка файлов в папке "text"
files = os.listdir(input_folder)

for file_name in files:
    # Чтение содержимого файла
# Чтение содержимого файла
    with open(os.path.join(input_folder, file_name), 'r') as file:
        texts = file.readlines()

    # Объединение строк в одну строку
    text = ' '.join(texts)

    # Реферирование текста
    summary = summarize(text)
    
    # Сохранение результатов в файл в папке "result"
    output_file = os.path.join(output_folder, f"{file_name}_summary.txt")
    with open(output_file, 'w') as file:
        file.write(summary)
