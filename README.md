# CryptoTradingBot

## Açıklama (Description)

Bu Python tabanlı bot, Binance Futures API'si ve Telegram bot entegrasyonu kullanarak otomatik kripto para ticareti yapmak için tasarlanmıştır.  
This Python-based bot is designed for automated cryptocurrency trading using Binance Futures API and Telegram bot integration.

---

## Özellikler (Features)

- **Türkçe:**  
  - Binance Futures API ile otomatik kripto ticareti.
  - Telegram bot üzerinden kontrol edilebilir.
  - Teknik analiz indikatörlerini (RSI, MACD, ADX, ATR) hesaplar.
  - Pozisyon açma, kapama ve emir yönetimi.
  - JSON yapılandırma dosyası ile özelleştirilebilir ayarlar.

- **English:**  
  - Automated cryptocurrency trading via Binance Futures API.
  - Controllable through Telegram bot.
  - Calculates technical indicators (RSI, MACD, ADX, ATR).
  - Opens, closes positions, and manages orders.
  - Customizable settings via a JSON configuration file.

---

## Gereksinimler (Requirements)

- Python 3.9 veya üstü (Python 3.9 or higher)
- Gerekli Python kütüphaneleri (Required Python libraries):
  ```bash
  pip install ccxt pandas ta python-telegram-bot
## Kullanım (Usage)
config.json dosyasını düzenleyin (Edit the config.json file):

- **Türkçe:**
  - config.json dosyasındaki apiKey, secretKey ve bot alanlarını Binance ve Telegram API anahtarlarınızla doldurun.
- **English:**
  - Update the config.json file with your Binance apiKey, secretKey, and Telegram bot key.
### Botu başlatın (Start the bot):

- **Türkçe:** 
  - main.py dosyasını çalıştırarak botu başlatın:
  ##### Kodu kopyala
    ```bash
    python main.py
- **English:**
  - Run the main.py file to start the bot:
  ##### Copy code
    ```bash
    python main.py

## Telegram bot komutları (Telegram bot commands):

- **Türkçe:**
  - /start: Botu başlatır.
  - /stop: Botu duraklatır.
  - /close: Açık pozisyonları kapatır.
  - /indicator: İndikatör değerlerini gönderir.
- **English:**
  - /start: Starts the bot.
  - /stop: Pauses the bot.
  - /close: Closes open positions.
  - /indicator: Sends indicator values.
