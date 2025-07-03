# OpenAI ve Flask ile Sohbet Botu

Bu proje, OpenAI API'si ile entegre çalışan, Flask tabanlı web arayüzüne sahip bir sohbet botudur. Kullanıcılar web arayüzü üzerinden mesaj göndererek, OpenAI destekli asistan ile etkileşime geçebilir.

## Özellikler
- OpenAI API ile gerçek zamanlı sohbet
- Her kullanıcı için ayrı oturum yönetimi
- Modern ve mobil uyumlu web arayüzü
- Sohbet geçmişi görüntüleme ve sıfırlama

## Gereksinimler
- Python 3.8+
- [OpenAI Python SDK](https://pypi.org/project/openai/)
- Flask
- python-dotenv

## Kurulum
1. **Depoyu klonlayın veya dosyaları indirin.**
2. Gerekli Python paketlerini yükleyin:
   ```bash
   pip install flask openai python-dotenv
   ```
3. Proje dizininde bir `.env` dosyası oluşturun ve OpenAI API anahtarınızı ekleyin:
   ```env
   OPENAI_API_KEY=sk-...buraya-anahtarınızı-yazın...
   ```

## Kullanım
1. Sunucuyu başlatın:
   ```bash
   python app.py
   ```
2. Tarayıcınızda [http://127.0.0.1:5000](http://127.0.0.1:5000) adresine gidin.
3. Mesajınızı yazın ve "Gönder" butonuna tıklayın. Sohbet geçmişiniz ekranda görüntülenecektir.
4. "Sohbeti Sıfırla" butonu ile yeni bir oturum başlatabilirsiniz.

## Dosya Yapısı
- `app.py` : Flask web uygulaması ve arayüz
- `agents.py` : OpenAI API ile sohbet oturumu ve mesaj yönetimi
- `.env` : (Gizli) OpenAI API anahtarınızı içerir

## Notlar
- API anahtarınızı kimseyle paylaşmayın.
- Sohbet oturumları sunucu belleğinde tutulur, sunucu yeniden başlatılırsa geçmiş silinir.

## Lisans
Bu proje eğitim ve kişisel kullanım içindir. 