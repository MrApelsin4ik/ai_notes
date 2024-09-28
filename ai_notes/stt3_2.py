import os
import whisper
import requests
import torch
import time
import re
import base64
import soundfile as sf
import numpy as np



# Установка кэша моделей в директорию ./model_cache
cache_dir = "./model_cache"
key = '@]p$}&/IaF0g7?jl?@8+AdK!dj,@9AxY:'
whisper_model = whisper.load_model("base")

# Функция для распознавания речи из аудиофайла
def transcribe_audio(audio_file):
    global whisper_model

    # Read the audio file into a NumPy array
    audio, sample_rate = sf.read(audio_file)

    # Convert audio to float32
    audio = audio.astype(np.float32)

    # Ensure the audio is mono
    if audio.ndim > 1:
        audio = audio.mean(axis=1)  # Average the channels

    result = whisper_model.transcribe(audio)
    return result["text"]


# Функция для обработки текста через Yandex GPT
def process_text_with_yandex_gpt(text, task):
    prompt = {
        "modelUri": "gpt://b1gvoaoui9vn33q5fha8/yandexgpt-lite",
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
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Api-Key AQVN3Vu9qIaIV3-0fjGgMj8Vcz56VM9YlSMvz-jS"
    }

    response = requests.post(url, headers=headers, json=prompt)

    if response.status_code != 200:
        print("Ошибка:", response.status_code, response.text)
        return False

    result = response.json()
    return result.get('result', {}).get('alternatives', [{}])[0].get('message', {}).get('text', '').strip()

# Разделение текста на части
def split_text(text, max_length=1000):
    # Разделяем текст на предложения
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Проверяем длину текущего куска и добавляем предложение
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            if current_chunk:
                current_chunk += " "  # Добавляем пробел между предложениями
            current_chunk += sentence
        else:
            # Если текущий кусок превышает длину, сохраняем его и начинаем новый
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence

    # Добавляем последний кусок, если он не пустой
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# Генерация конспекта
def create_summary(chunks, topic, images):
    summary = ""
    for chunk in chunks:
        processed_text = process_text_with_yandex_gpt(chunk, f'Перепиши текст, сократив его, оставь только самое главное. В тексте есть лишние фразы, не касающиеся основной темы "{topic}", их вставлять в текст не нужно.')
        summary += processed_text + " "
    return summary.strip()

# Генерация тезисного плана
def create_thesis_plan(chunks):
    thesis_plan = ""
    for chunk in chunks:
        processed_text = process_text_with_yandex_gpt(chunk, f'Создай тезисный план из следующего текста: {chunk}')
        thesis_plan += processed_text + " "
    return thesis_plan.strip()

# Генерация теста
def create_test(chunks):
    test = ""
    for chunk in chunks:
        processed_text = process_text_with_yandex_gpt(chunk, f'Сформулируй вопрос и ответ на основе следующего текста: {chunk}')
        test += processed_text + " "
    return test.strip()


# Функция для получения данных с сервера
def get_note_data(server, key=''):
    session = requests.Session()  # Create a session to persist cookies
    response = session.get(f"http://{server}/get_summary_data")

    # Check if response is successful
    if response.status_code != 200:
        print("Ошибка при получении данных:", response.status_code, response.text)
        return None

    csrf_token = session.cookies.get('csrftoken')
    print(csrf_token)
    url = f"http://{server}/get_summary_data/"
    print(url)

    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token  # Передаем CSRF токен
    }
    payload = {
        "key": key
    }
    print('post')
    response = session.post(url, headers=headers, json=payload)


    if response.status_code == 200:
        data = response.json()
        return data #данные заметки
    else:
        print("Ошибка при получении данных:", response.status_code, response.text)
        return None

# Функция для отправки данных на сервер
def send_summary_data(note_id, summary_text=None, thesis_plan=None, test_text=None, files=[], server='', key=''):
    session = requests.Session()  # Create a session to persist cookies
    response = session.get(f"http://{server}/update_summary_data")

    # Check if response is successful
    if response.status_code != 200:
        print("Ошибка при получении данных:", response.status_code, response.text)
        return None

    csrf_token = session.cookies.get('csrftoken')


    url = f"http://{server}/update_summary_data/"  # Укажите URL вашего сервера
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token  # Передаем CSRF токен
    }
    payload = {
        "key": key,
        "id": note_id,
        "summary_text": summary_text,
        "thesis_plan": thesis_plan,
        "test_text": test_text,
        "files": files
    }

    response = session.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Данные успешно отправлены:", response.json())
    else:
        print("Ошибка при отправке данных:", response.status_code, response.text)

# Функция для извлечения аудиофайлов
def extract_audio_files(file_list, file_names):
    audio_files = []
    # Create the ./tmp directory if it doesn't exist
    os.makedirs('./tmp', exist_ok=True)

    for file, name in zip(file_list, file_names):
        if name.endswith(('.mp3', '.wav', '.m4a')):
            # Use only the base name of the file, without any directories
            base_name = os.path.basename(name)
            tmp_file_path = os.path.join('./tmp', base_name)  # Save in ./tmp directory
            with open(tmp_file_path, 'wb') as tmp_file:  # Open the file in binary write mode
                tmp_file.write(file)  # Write the byte content to the temporary file
                audio_files.append(tmp_file_path)  # Save the temp file path
    return audio_files

def extract_images_from_text(text):
    pass


def describe_image(image):
    pass


# Основной код генерации
if __name__ == "__main__":
    server = '192.168.0.117:80'


    while True:
        try:
            note_data = get_note_data(server=server, key=key)

            if note_data is None:
                time.sleep(5)  # Подождите перед следующей попыткой


            note_id = note_data["note_id"]
            if_summary = note_data["summary"]
            if_outline = note_data["outline"]
            if_test = note_data["test"]
            text = note_data["note_text"]
            files = [base64.b64decode(file) for file in note_data["files"]]
            file_names = note_data["file_names"]

            audio_files = extract_audio_files(files, file_names)

            # Распознавание аудиофайлов
            transcribed_texts = []
            for audio_file in audio_files:
                text_from_audio = transcribe_audio(audio_file)
                transcribed_texts.append(text_from_audio)

            full_text = " ".join(transcribed_texts) + ' ' + text

            # Определение темы
            chunks = split_text(text)
            topic = process_text_with_yandex_gpt(chunks[0], "Определи тему лекции.")

            # Генерация конспекта, тезисного плана и теста
            summary = create_summary(chunks, topic)
            thesis_plan = create_thesis_plan(chunks)
            test = create_test(chunks)

            # Сохранение на сервер
            files_to_send = []
            send_summary_data(note_id=note_id, summary_text=summary, thesis_plan=thesis_plan, test_text=test,
                              files=files_to_send,
                              server=server, key=key)



        except Exception as e:
            print(e)
