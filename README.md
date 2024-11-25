# CryptoTradingBot

## Açıklama (Description)
Bu Python tabanlı bot, Binance Futures API'si ve Telegram bot entegrasyonu kullanarak otomatik kripto para ticareti yapmak için tasarlanmıştır.

This Python-based bot is designed for automated cryptocurrency trading using Binance Futures API and Telegram bot integration.

---

## Özellikler (Features)
- **Binance Futures API** ile kripto ticareti.
- **Telegram bot** üzerinden bot kontrolü.
- Teknik analiz indikatörlerinin hesaplanması (RSI, MACD, ADX, ATR).
- Pozisyon açma, kapama ve emir yönetimi.
- Özelleştirilebilir ayarlar için JSON yapılandırma dosyası.

Automated features include:
- Trading cryptocurrencies using **Binance Futures API**.
- Controlling the bot through **Telegram bot**.
- Calculating technical indicators (RSI, MACD, ADX, ATR).
- Opening, closing positions, and managing orders.
- Customizable settings via a JSON configuration file.

---

## Gereksinimler (Requirements)
- Python 3.9 veya üstü.
- Aşağıdaki Python kütüphaneleri:
  - `ccxt`
  - `pandas`
  - `ta`
  - `python-telegram-bot`

Required dependencies:
```bash
pip install ccxt pandas ta python-telegram-bot
