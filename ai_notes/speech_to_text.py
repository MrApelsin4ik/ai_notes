import whisper
import torch
from transformers import GPT2Tokenizer, T5ForConditionalGeneration

# Модель Whisper для STT
whisper_model = whisper.load_model("base")

# Транскрипция аудио
audio_file = "videoplayback.mp3"
result = whisper_model.transcribe(audio_file)
transcribed_text = result["text"]
print("Распознанный текст:", transcribed_text)

# Укажите путь для кэша модели
cache_dir = './model_cache'  # Путь к директории для кэша модели

# Загрузка модели T5 с указанием директории кэша
tokenizer = GPT2Tokenizer.from_pretrained('ai-forever/FRED-T5-1.7B', eos_token='</s>', cache_dir=cache_dir)
model = T5ForConditionalGeneration.from_pretrained('ai-forever/FRED-T5-1.7B', cache_dir=cache_dir)
device = 'cuda'
model.to(device)


# Функция для разбивки текста на части
def chunk_text(text, chunk_size=1024):
    chunks = []
    words = text.split()
    current_chunk = []
    current_length = 0

    for word in words:
        current_length += len(word) + 1  # +1 для пробела
        if current_length > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = len(word) + 1
        current_chunk.append(word)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


# Разбивка текста на части
text_chunks = chunk_text(transcribed_text)


# Функция для обработки текста с помощью T5
def process_with_t5(text, prefix):
    lm_text = f'<{prefix}>{text}'
    input_ids = torch.tensor([tokenizer.encode(lm_text)]).to(device)
    outputs = model.generate(input_ids, eos_token_id=tokenizer.eos_token_id, early_stopping=True)
    return tokenizer.decode(outputs[0][1:])


# Исправление текста
corrected_text = ""
for chunk in text_chunks:
    corrected_chunk = process_with_t5(chunk, "SC1")  # Используем префикс для исправления
    corrected_text += corrected_chunk + " "

print("Исправленный текст:", corrected_text)

# Создание конспекта
summary = ""
for chunk in text_chunks:
    summary_chunk = process_with_t5(chunk, "SC5")  # Используем префикс для конспекта
    summary += summary_chunk + " "

print("Конспект:", summary)
