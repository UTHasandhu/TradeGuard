import yfinance as yf

def fetch_asset_data(symbol: str):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1mo")

    price = hist["Close"].iloc[-1]
    volatility = hist["Close"].pct_change().std()

    return {
        "price": float(price),
        "volatility": float(volatility)
    }
