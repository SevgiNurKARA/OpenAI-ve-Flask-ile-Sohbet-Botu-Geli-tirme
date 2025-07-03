import openai
import os
from dotenv import load_dotenv
import uuid

# .env dosyasındaki API anahtarını yükle
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Oturumları tutacağımız sözlük yapısı
chat_sessions = {}

system_prompt = {
    "role": "system",
    "content": "You are a playful poet who speaks only in rhymes."
}

def create_chat():
    """
    Yeni bir sohbet oturumu oluşturur ve sistem mesajını dahil eder.
    """
    chat_id = str(uuid.uuid4())  # Benzersiz bir kimlik oluştur
    chat_sessions[chat_id] = [system_prompt]
    return chat_id

def send_message(chat_id, user_message):
    """
    Belirtilen oturuma kullanıcı mesajı ekler ve OpenAI API'den yanıt alır.
    """
    if chat_id not in chat_sessions:
        raise ValueError("Chat session not found!")
    chat_sessions[chat_id].append({"role": "user", "content": user_message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # veya elinde varsa gpt-4o
        messages=chat_sessions[chat_id]
    )
    answer = response.choices[0].message['content'].strip()
    chat_sessions[chat_id].append({"role": "assistant", "content": answer})
    return answer

def get_chat_history(chat_id):
    """
    Belirtilen oturumun sohbet geçmişini döndürür.
    """
    if chat_id not in chat_sessions:
        raise ValueError("Chat session not found!")
    return chat_sessions[chat_id]

if __name__ == "__main__":
    # Yeni bir sohbet başlat
    chat_id = create_chat()
    print(f"Oluşturulan chat_id: {chat_id}")

    # Kullanıcıdan mesaj al (veya örnek mesaj gönder)
    user_message = "Merhaba, bana bir şiir yazar mısın?"
    cevap = send_message(chat_id, user_message)
    print("Asistan:", cevap)

    # Sohbet geçmişini göster
    print("Sohbet Geçmişi:", get_chat_history(chat_id))

