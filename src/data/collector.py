import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests
from cryptocmd import CmcScraper

class CryptoDataCollector:
    def __init__(self):
        self.supported_coins = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'SOL-USD']
        
    def fetch_crypto_data(self, symbol='BTC-USD', period='1y', interval='1d'):
        """
        Fetch cryptocurrency data using yfinance
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            return df
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
            
    def fetch_multiple_cryptos(self, symbols=None, period='1y'):
        """
        Fetch data for multiple cryptocurrencies
        """
        if symbols is None:
            symbols = self.supported_coins
            
        data_dict = {}
        for symbol in symbols:
            data_dict[symbol] = self.fetch_crypto_data(symbol, period)
        
        return data_dict
    
    def fetch_historical_data(self, symbol='BTC', start_date=None, end_date=None):
        """
        Fetch historical data using CmcScraper
        """
        try:
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=365)).strftime('%d-%m-%Y')
            if end_date is None:
                end_date = datetime.now().strftime('%d-%m-%Y')
                
            scraper = CmcScraper(symbol, start_date, end_date)
            df = scraper.get_dataframe()
            return df
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return None
    
    def get_market_sentiment(self, symbol='bitcoin'):
        """
        Get basic market sentiment from available APIs
        """
        try:
            # Using CoinGecko public API
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
            response = requests.get(url)
            data = response.json()
            
            sentiment_data = {
                'price_usd': data[symbol]['usd'],
                'price_change_24h': data[symbol]['usd_24h_change'],
                'market_cap': data[symbol]['usd_market_cap']
            }
            return sentiment_data
        except Exception as e:
            print(f"Error fetching sentiment data: {e}")
            return None

    def save_to_csv(self, data, filename):
        """
        Save data to CSV file
        """
        try:
            if isinstance(data, dict):
                # Save multiple datasets
                for symbol, df in data.items():
                    df.to_csv(f"{filename}_{symbol.replace('-', '_')}.csv")
            else:
                # Save single dataset
                data.to_csv(filename)
            print(f"Data saved successfully to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")

if __name__ == "__main__":
    # Example usage
    collector = CryptoDataCollector()
    
    # Fetch Bitcoin data
    btc_data = collector.fetch_crypto_data()
    print("Bitcoin data shape:", btc_data.shape)
    
    # Fetch multiple cryptocurrencies
    multi_data = collector.fetch_multiple_cryptos(['BTC-USD', 'ETH-USD'])
    print("Fetched data for multiple cryptocurrencies")
    
    # Get market sentiment
    sentiment = collector.get_market_sentiment()
    print("Market sentiment:", sentiment)