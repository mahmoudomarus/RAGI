# BGBTC (Bitcoin & Crypto Analysis with RAG)

A comprehensive cryptocurrency analysis tool that combines technical analysis, market data, and AI-powered insights using freely available tools and APIs.

## 🚀 Features

- 📊 Real-time cryptocurrency price data
- 📈 Technical analysis with multiple indicators
- 🤖 AI-powered market insights using RAG (Retrieval Augmented Generation)
- 📱 Interactive Streamlit dashboard
- 🔄 Multiple timeframe analysis
- 💹 Trading signals generation
- 📑 Historical data analysis

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/BGBTC.git
cd BGBTC
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Running the Streamlit Dashboard
```bash
streamlit run app.py
```

### Using the Jupyter Notebook
1. Navigate to the notebooks directory
2. Open `BGBTC_Analysis.ipynb` in Jupyter Notebook or Jupyter Lab
3. Run the cells sequentially

### Using in Kaggle
1. Create a new notebook in Kaggle
2. Add the following to the first cell:
```python
!git clone https://github.com/yourusername/BGBTC.git
%cd BGBTC
!pip install -r requirements.txt
```

## 📊 Components

### Data Collector (`src/data/collector.py`)
- Fetches real-time cryptocurrency data
- Supports multiple data sources (Yahoo Finance, CoinGecko)
- Historical data retrieval
- Market sentiment analysis

### RAG Agent (`src/rag_agent.py`)
- Implements simple but effective RAG architecture
- Uses free, lightweight models for embeddings
- Generates market insights
- Answers user queries about market conditions

### Streamlit App (`app.py`)
- Interactive dashboard
- Real-time price charts
- Technical indicators
- AI-powered insights
- Query interface

## 📈 Available Technical Indicators

- Moving Averages (SMA 20, 50, 200)
- Relative Strength Index (RSI)
- Moving Average Convergence Divergence (MACD)
- Bollinger Bands
- Volume Analysis
- Price Momentum

## 🤖 AI Features

- Market trend analysis
- Pattern recognition
- Natural language query processing
- Historical pattern matching
- Trading signal generation

## 📝 Running Tests

```bash
python -m pytest tests/
```

## 🔄 Updating Data

The system automatically fetches real-time data when running the dashboard or notebooks. Historical data can be updated using the data collector:

```python
from src.data.collector import CryptoDataCollector

collector = CryptoDataCollector()
data = collector.fetch_crypto_data('BTC-USD', '1y')
collector.save_to_csv(data, 'btc_yearly_data.csv')
```

## 📊 Example Queries

The RAG agent can answer questions like:
- "What's the current market trend?"
- "Show me the trading volume analysis"
- "Identify potential support and resistance levels"
- "Analyze the market sentiment"

## 🔧 Customization

You can customize the analysis by:
1. Adding new technical indicators
2. Modifying the RAG knowledge base
3. Adjusting trading signal parameters
4. Adding new data sources

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Yahoo Finance API Documentation](https://python-yahoofinance.readthedocs.io/)
- [Technical Analysis Library Documentation](https://technical-analysis-library-python.readthedocs.io/)
- [Sentence Transformers Documentation](https://www.sbert.net/)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.