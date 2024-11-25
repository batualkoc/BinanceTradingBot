import ccxt
import pandas as pd
import os
import json
import time
from indicators import calculate_indicators
from telegram.ext import Updater, CommandHandler

running = True
paused = False


def load_json():
    with open('config.json', 'r') as f:
        return json.load(f)


data = load_json()
update = Updater(data['bot'], use_context=True)
update.start_polling()


def save_json(data):
    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)

def initialize_positions():
    data = load_json()
    if 'positions' in data:
        for symbol in data['positions']:
            data['positions'][symbol] = {
                "long_position_a": True,
                "short_position_a": True,
                "long_position": True,
                "short_position": True,
                "long_tk": True,
                "short_tk": True,
                "open_orders": True,
            }
    save_json(data)


def stop(update, context):
    global paused
    paused = True
    update.message.reply_text("Program duraklatıldı.")

def start(update, context):
    global paused
    paused = False
    update.message.reply_text("Program kaldığı yerden devam ediyor.")


update.dispatcher.add_handler(CommandHandler("stop", stop))
update.dispatcher.add_handler(CommandHandler("start", start))


def main():
    global running, paused
    initialize_positions()
    data = load_json()
    symbols = data["symbols"]
    exchange = ccxt.binance(dict(apiKey=data["apiKey"], secret=data["secretKey"], options={'defaultType': 'future'}, enableRateLimit=True))
    leverage = data["leverage"]
    balance = exchange.fetch_balance()
    starting_money = float(balance["total"]["USDT"])

    while running:
        if paused:
            time.sleep(1)  # Duraklatılmış durumda beklemeye devam et
            continue

        try:
            for symbol_name in symbols:
                symbol = symbol_name + "/USDT"
                symbol_name1 = symbol_name + "USDT"
                balance = exchange.fetch_balance()
                exchange.set_leverage(leverage, symbol)
                exchange.set_margin_mode('cross', symbol)
                open_orders = data['positions'].get(symbol_name, {}).get("open_orders")
                long_position = data['positions'].get(symbol_name, {}).get("long_position")
                short_position = data['positions'].get(symbol_name, {}).get("short_position")
                long_position_a = data['positions'].get(symbol_name, {}).get("long_position_a")
                short_position_a = data['positions'].get(symbol_name, {}).get("short_position_a")
                long_tk = data['positions'].get(symbol_name, {}).get("long_tk")
                short_tk = data['positions'].get(symbol_name, {}).get("short_tk")

                def send(update,context):
                    update.message.reply_text(output_message)

                update.dispatcher.add_handler(CommandHandler("send", send))

                def indicator_value(update,context):
                    update.message.reply_text(indicator_message)

                update.dispatcher.add_handler(CommandHandler("indicator", indicator_value))

                def close(update,context):
                    try:
                        # Tüm açık pozisyonları alın
                        balance = exchange.fetch_balance({'type': 'future'})
                        positions = balance['info']['positions']

                        # Açık pozisyonları kontrol et ve piyasa fiyatından kapat
                        for position in positions:
                            symbol = position['symbol']
                            position_amt = float(position['positionAmt'])

                            # Pozisyon miktarı sıfırdan farklı ise açık pozisyon var demektir
                            if position_amt != 0:
                                side = 'sell' if position_amt > 0 else 'buy'  # Long pozisyonu kapatmak için 'sell', short pozisyon için 'buy'

                                # Piyasa emri ile pozisyonu kapat

                                update.message.reply_text(f"Closing position for {symbol} - Amount: {position_amt}")
                                exchange.create_order(symbol=symbol, type='market', side=side, amount=abs(position_amt))

                    except Exception as e:
                        update.message.reply_text(f"Error closing positions: {e}")

                update.dispatcher.add_handler(CommandHandler("close", close))

                total_money = float(balance["total"]["USDT"])
                trade_money = total_money / leverage
                minus_money = total_money - trade_money
                excess_balance = total_money - minus_money
                if excess_balance > 0:
                    percentage_of_trade_money = int(((excess_balance / total_money) * 20) * leverage)
                else:
                    percentage_of_trade_money = 0

                baslangic = time.time()
                order_book = exchange.fetch_order_book(symbol)
                bars = exchange.fetch_ohlcv(symbol, timeframe="15m", since=None, limit=100)
                df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])
                current_price = order_book["asks"][0][0] if long_position or short_position else order_book["bids"][0][0]
                df = calculate_indicators(df)

                positions = balance["info"]["positions"]
                for position in positions:
                    if position["symbol"] == symbol_name1:
                        amount = float(position["positionAmt"])
                        pnl = float(position["unrealizedProfit"])
                        entry_Price = float(position['entryPrice'])
                        isolated_wallet = float(position["positionInitialMargin"])

                        if amount == 0:
                            exchange.cancel_all_orders(symbol)

                        if open_orders == True and amount == 0:
                            short_position_a = True
                            long_position_a = True

                def message(update,context):
                    if long_tk == True:
                        update.message.reply_text(f"Long Pozition Entered {symbol} Entered Price - {round(df['close'].iloc[-1],5)}")
                    if short_tk == True:
                        update.message.reply_text(f"Short Pozition Entered {symbol} - Entered Price {round(df['close'].iloc[-1],5)}")



                if short_position_a == True and df['rsi'].iloc[-1] < 25:
                    long_position = False
                    short_position = False
                    short_position_a = False
                    open_orders = False

                if long_position_a == True and df['rsi'].iloc[-1] > 75:
                    short_position = False
                    long_position = False
                    long_position_a = False
                    open_orders = False

                if long_position == False and df['rsi'].iloc[-1] >= 31 and df['rsi'].iloc[-2] <= 30 and df['rsi'].iloc[-3] <= 30 and df['rsi'].iloc[-4] <= 30 and df['adx'].iloc[-1] >= df['adx'].iloc[-2] and df['adx'].iloc[-2] >= df['adx'].iloc[-3]:
                    long_enter(symbol, exchange, total_money, percentage_of_trade_money, leverage, current_price)
                    long_position = True
                    long_tk = True

                if short_position == False and df['rsi'].iloc[-1] <= 69 and df['rsi'].iloc[-2] >= 70 and df['rsi'].iloc[-3] >= 70 and df['rsi'].iloc[-4] >= 70 and df['adx'].iloc[-1] <= df['adx'].iloc[-2] and df['adx'].iloc[-2] <= df['adx'].iloc[-3]:
                    short_enter(symbol, exchange, total_money, percentage_of_trade_money, leverage, current_price)
                    short_position = True
                    short_tk = True

                if long_tk == True and entry_Price > 0 and amount > 0:
                    message(update,context=None)
                    long_take_profit = entry_Price + (1 * df['atr'].iloc[-1])
                    long_stop_loss = entry_Price - (2 * df['atr'].iloc[-1])
                    exchange.create_take_profit_order(symbol=symbol, type='market', side='sell', amount=amount, takeProfitPrice=long_take_profit)
                    exchange.create_stop_loss_order(symbol=symbol, type='market', side='sell', amount=amount, stopLossPrice=long_stop_loss)
                    long_tk = False
                    open_orders = True



                if short_tk == True and entry_Price > 0 and amount < 0:
                    message(update,context=None)
                    short_take_profit = entry_Price - (1 * df['atr'].iloc[-1])
                    short_stop_loss = entry_Price + (2 * df['atr'].iloc[-1])
                    exchange.create_take_profit_order(symbol=symbol, type='market', side='buy', amount=abs(amount), takeProfitPrice=short_take_profit)
                    exchange.create_stop_loss_order(symbol=symbol, type='market', side='buy', amount=abs(amount), stopLossPrice=short_stop_loss)
                    short_tk = False
                    open_orders = True

                if long_position_a == False:
                    position_value = "Short Position Search"
                if short_position_a == False:
                    position_value = "Long Position Search"
                if long_position_a and short_position_a == False:
                    position_value = "BOTH Position Search"
                if long_position_a and short_position_a == True:
                    position_value = "Search Position"

                os.system("clear")
                print("Starting USDT:", round(starting_money, 8))
                print("Total USDT:", round(total_money, 8))
                print("Trade Coin: " + str(symbol_name))
                print("Position:", str(position_value))
                print("Percentage Trade: %", int(percentage_of_trade_money))

                if amount > 0:
                    if isolated_wallet != 0:
                        roi = (pnl / isolated_wallet) * 100
                        print("Long Position Roe: %" + str(roi))
                elif amount < 0:
                    if isolated_wallet != 0:
                        roi = (pnl / isolated_wallet) * 100
                        print("Short Position Roe: %" + str(roi))
                else:
                    print("Total Profit:", round(float(balance["total"]["USDT"]) - starting_money, 8),
                          "USDT || %" + str(round(((float(balance["total"]["USDT"]) - starting_money) / starting_money) * 100, 8)))
                son = time.time()
                print("Delay:", round(son - baslangic, 3), "seconds")

                indicator_message = f"Symbol Name: {str(symbol_name)}\n"
                indicator_message += f"Close : {round(df['close'].iloc[-1],8)}\n"
                indicator_message += f"RSI1: {round(df['rsi'].iloc[-1], 3)}\n"
                indicator_message += f"RSI2: {round(df['rsi'].iloc[-2], 3)}\n"
                indicator_message += f"RSI3: {round(df['rsi'].iloc[-3], 3)}\n"
                indicator_message += f"RSI4: {round(df['rsi'].iloc[-4], 3)}\n"
                indicator_message += f"ADX1: {round(df['adx'].iloc[-1], 3)}\n"
                indicator_message += f"ADX2: {round(df['adx'].iloc[-2], 3)}\n"
                indicator_message += f"ADX3: {round(df['adx'].iloc[-3], 3)}\n"

                output_message = f"Starting USDT: {round(starting_money, 8)}\n"
                output_message += f"Total USDT: {round(total_money, 8)}\n"
                output_message += f"Trade Coin: {str(symbol_name)}\n"
                output_message += f"Position: {str(position_value)}\n"
                output_message += f"Percentage Trade: % {int(percentage_of_trade_money)}\n"
                if amount > 0:
                    if isolated_wallet != 0:
                        roi = (pnl / isolated_wallet) * 100
                        output_message += f"Long Position. Roe: %{str(roi)}\n"
                elif amount < 0:
                    if isolated_wallet != 0:
                        roi = (pnl / isolated_wallet) * 100
                        output_message += f"Short Position. Roe: %{str(roi)}\n"
                else:
                    output_message += f"Total Profit: {round(total_money - starting_money, 8)} USDT || %" \
                                        f"{str(round(((float(balance['total']['USDT']) - starting_money) / starting_money) * 100, 8))}\n"

                son = time.time()
                output_message += f"Delay: {round(son - baslangic, 3)} seconds\n"

                if symbol_name not in data['positions']:
                    data['positions'][symbol_name] = {}

                data['positions'][symbol_name].update({
                    "long_position_a": long_position_a,
                    "short_position_a": short_position_a,
                    "long_position": long_position,
                    "short_position": short_position,
                    "long_tk": long_tk,
                    "short_tk": short_tk,
                    "open_orders": open_orders
                })

                save_json(data)

                if paused:
                    break

        except ccxt.BaseError as Error:
            print("[ERROR] ", Error)
            with open("error_log.txt", "a") as error_file:
                error_file.write(f"[ERROR] {str(Error)}\n")

if __name__ == "__main__":
    main()
