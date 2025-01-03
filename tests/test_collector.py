import pytest
from src.data.collector import CryptoDataCollector
import pandas as pd

@pytest.fixture
def collector():
    return CryptoDataCollector()

def test_fetch_crypto_data(collector):
    # Test fetching Bitcoin data
    data = collector.fetch_crypto_data('BTC-USD', '1mo')
    assert isinstance(data, pd.DataFrame)
    assert not data.empty
    assert 'Close' in data.columns
    assert 'Volume' in data.columns

def test_fetch_multiple_cryptos(collector):
    # Test fetching multiple cryptocurrencies
    symbols = ['BTC-USD', 'ETH-USD']
    data_dict = collector.fetch_multiple_cryptos(symbols, '1mo')
    
    assert isinstance(data_dict, dict)
    assert len(data_dict) == len(symbols)
    for symbol in symbols:
        assert symbol in data_dict
        assert isinstance(data_dict[symbol], pd.DataFrame)
        assert not data_dict[symbol].empty

def test_get_market_sentiment(collector):
    # Test market sentiment retrieval
    sentiment = collector.get_market_sentiment('bitcoin')
    
    assert isinstance(sentiment, dict)
    assert 'price_usd' in sentiment
    assert 'price_change_24h' in sentiment
    assert 'market_cap' in sentiment

def test_save_to_csv(collector, tmp_path):
    # Test saving data to CSV
    data = collector.fetch_crypto_data('BTC-USD', '1mo')
    filename = tmp_path / "test_data.csv"
    collector.save_to_csv(data, str(filename))
    
    # Verify file was created and can be read
    assert filename.exists()
    loaded_data = pd.read_csv(str(filename))
    assert not loaded_data.empty