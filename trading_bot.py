import yfinance as yf
import pandas as pd

def fetch_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """Fetch historical data for a ticker using yfinance."""
    data = yf.download(ticker, period=period, progress=False)
    return data


def compute_sma(data: pd.DataFrame, window: int) -> pd.Series:
    """Compute simple moving average."""
    return data['Close'].rolling(window=window).mean()


def generate_signals(data: pd.DataFrame, short_window: int = 20, long_window: int = 50) -> pd.DataFrame:
    """Generate buy/sell signals based on SMA crossovers."""
    data = data.copy()
    data['SMA_Short'] = compute_sma(data, short_window)
    data['SMA_Long'] = compute_sma(data, long_window)
    data['Signal'] = 0
    data.loc[data['SMA_Short'] > data['SMA_Long'], 'Signal'] = 1
    data.loc[data['SMA_Short'] < data['SMA_Long'], 'Signal'] = -1
    data['Position'] = data['Signal'].diff()
    return data


def backtest(ticker: str, period: str = "1y") -> pd.DataFrame:
    """Fetch data, generate signals, and return the dataframe."""
    data = fetch_data(ticker, period)
    signals = generate_signals(data)
    return signals


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple SMA crossover trading bot")
    parser.add_argument("ticker", help="Ticker symbol, e.g., AAPL or BTC-USD")
    parser.add_argument("--period", default="1y", help="Historical period to download")
    args = parser.parse_args()

    signals = backtest(args.ticker, args.period)
    print(signals.tail())
