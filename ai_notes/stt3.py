# -*- coding: utf-8 -*-
import os
import whisper
import requests
import torch
import time



# Распознавание речи из аудиофайла
audio_file = "videoplayback.mp3"

whisper_model = whisper.load_model("base")
result = whisper_model.transcribe(audio_file)
text = result["text"]
text = ''

print("Распознанный текст:", text)

# Функция для обработки текста через Yandex GPT
def process_text_with_yandex_gpt(text, task):
    prompt = {
        "modelUri": "gpt://<ВАШ_ИДЕНТИФИКАТОР_КАТАЛОГА>/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {"role": "system", "text": "Ты языковая модель для обработки текста. В твоём ответе должен быть только обработанный текст и ничто больше."},
            {"role": "user", "text": f"{task}: {text}"}
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json;  charset=utf-8",
        "Authorization": "Api-Key <ВАШ_API_КЛЮЧ>"
    }

    response = requests.post(url, headers=headers, json=prompt)

    if response.status_code != 200:
        print("Ошибка:", response.status_code, response.text)
        return False  # Возвращаем False при ошибке

    result = response.json()

    if 'error' in result:
        error_code = result['error'].get('httpCode')
        if error_code == 429:
            print("Слишком много запросов. Повторите позже.")
            return False  # Возвращаем False при превышении квоты


    return result.get('result', {}).get('alternatives', [{}])[0].get('message', {}).get('text', '').strip()

# Разделение текста на части, если он слишком длинный
def split_text(text, max_length=1500):
    words = text.split()
    current_chunk = []
    chunks = []

    for word in words:
        current_chunk.append(word)
        if len(' '.join(current_chunk)) > max_length:
            chunks.append(' '.join(current_chunk[:-1]))
            current_chunk = [word]

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Исправление ошибок распознавания
"""
corrected_text = ""
for i, chunk in enumerate(split_text(text)):
    print(i)
    success = False
    while not success:
        processed_text = process_text_with_yandex_gpt(chunk, "Исправь ошибки распознавания")
        if processed_text is False:
            time.sleep(2)
            # Если получили False, можно сделать паузу или просто повторить запрос
            print("Повторный запрос для части текста...")
            continue  # Попробуем снова
        corrected_text += processed_text + " "
        success = True  # Успех, выходим из цикла

print("Исправленный текст:", corrected_text)
"""

#определение темы:
chunks = split_text(text)
print(chunks)
topic = process_text_with_yandex_gpt(chunks[0], "Ты получишь транскрибацию записи лекции. Определи тему этой лекции. В ответе напиши только тему")
print(topic)

# Создание конспекта
summary = ""
for i, chunk in enumerate(chunks):
    success = False
    while not success:
        processed_text = process_text_with_yandex_gpt(chunk, f"Создай конспект по тексту. Учти, что в тексте есть лишние фразы, например НАПРЯМУЮ ПОЛНОСТЬЮ не касающиеся основной темы ('{topic}'), их конспектировать не нужно.")
        if processed_text is False:
            # Если получили False, можно сделать паузу или просто повторить запрос
            print("Повторный запрос для части текста...")
            continue  # Попробуем снова
        summary += processed_text + " "
        success = True  # Успех, выходим из цикла


print("Конспект:", summary)
