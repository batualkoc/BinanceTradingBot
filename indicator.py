from ta.trend import MACD, ADXIndicator, CCIIndicator, SMAIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volume import MFIIndicator, ChaikinMoneyFlowIndicator
from ta.volatility import AverageTrueRange


def calculate_indicators(df):

    # RSI
    rsi = RSIIndicator(close=df['close'], window=12)
    df['rsi'] = rsi.rsi()

    # Stochastic Oscillator

    stochastic_oscillator = StochasticOscillator(high=df['high'],low=df['low'], close=df['close'], window=14, smooth_window=3)
    df['stochastic_oscillator'] = stochastic_oscillator.stoch()
    df['stochastic_signal'] = stochastic_oscillator.stoch_signal()

    # MACD
    macd = MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=9)
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()

    # ADX
    adx = ADXIndicator(df['high'], df['low'], df['close'], window=14)
    df['adx'] = adx.adx()
    df['positive'] = adx.adx_pos()
    df['negative'] = adx.adx_neg()

    # EMA 20
    ema_20 = SMAIndicator(close=df['close'], window=20)
    df["ema_20"] = ema_20.sma_indicator()

    # EMA 50
    ema_50 = SMAIndicator(close=df['close'], window=50)
    df["ema_50"] = ema_50.sma_indicator()
    
    # CCI
    cci = CCIIndicator(high=df['high'], low=df['low'], close=df['close'], window=20)
    df['cci'] = cci.cci()

    # Momentum (MOM)
    mom = df['close'].diff(periods=14)
    df['momentum'] = mom

    # Money Flow Index (MFI)
    mfi = MFIIndicator(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], window=14)
    df['mfi'] = mfi.money_flow_index()

    # Chakin Money Flow Index

    cmf = ChaikinMoneyFlowIndicator(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], window=20)
    df['cmf'] = cmf.chaikin_money_flow()

    # Average True Range

    atr = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14)
    df['atr'] = atr.average_true_range()
    return df
    
def calculate_pivots(df2):

    # Önce lookback periyod için high, low, close değerlerini belirle
    pivot_high = df2['high'].iloc[-2]
    pivot_low = df2['low'].iloc[-2]
    pivot_close = df2['close'].iloc[-2]  # Son kapanış

    # PP (Pivot Point) hesaplama
    df2['pp'] = (pivot_high + pivot_low + pivot_close) / 3

    # Range hesaplama
    range_hl = pivot_high - pivot_low

    # Resistance Levels
    df2['r1'] = df2['pp'] + (range_hl * 0.382)
    df2['r2'] = df2['pp'] + (range_hl * 0.618)
    df2['r3'] = df2['pp'] + range_hl

    # Support Levels
    df2['s1'] = df2['pp'] - (range_hl * 0.382)
    df2['s2'] = df2['pp'] - (range_hl * 0.618)
    df2['s3'] = df2['pp'] - range_hl

    return df2
