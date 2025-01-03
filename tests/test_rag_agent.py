import pytest
from src.rag_agent import SimpleRAGAgent
import pandas as pd
import numpy as np

@pytest.fixture
def rag_agent():
    return SimpleRAGAgent()

@pytest.fixture
def sample_data():
    # Create sample price data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    data = {
        'Close': np.random.randn(31).cumsum() + 100,
        'Volume': np.random.randint(1000, 10000, 31),
        'High': np.random.randn(31).cumsum() + 102,
        'Low': np.random.randn(31).cumsum() + 98
    }
    return pd.DataFrame(data, index=dates)

def test_add_knowledge(rag_agent):
    documents = [
        "Bitcoin is a cryptocurrency",
        "Technical analysis uses charts"
    ]
    rag_agent.add_knowledge(documents)
    
    assert len(rag_agent.knowledge_base) == len(documents)
    assert rag_agent.embeddings is not None
    assert len(rag_agent.embeddings) == len(documents)

def test_query(rag_agent):
    documents = [
        "Bitcoin is a cryptocurrency",
        "Technical analysis uses charts"
    ]
    rag_agent.add_knowledge(documents)
    
    results = rag_agent.query("What is Bitcoin?")
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert 'document' in results[0]
    assert 'similarity' in results[0]
    assert isinstance(results[0]['similarity'], float)

def test_analyze_crypto_data(rag_agent, sample_data):
    insights = rag_agent.analyze_crypto_data(sample_data)
    
    assert isinstance(insights, list)
    assert len(insights) > 0
    assert all(isinstance(insight, str) for insight in insights)

def test_generate_trading_signals(rag_agent, sample_data):
    signals = rag_agent.generate_trading_signals(sample_data)
    
    assert isinstance(signals, dict)
    assert 'trend' in signals
    assert 'position' in signals
    assert signals['trend'] in ['Bullish', 'Bearish']
    assert signals['position'] in ['Strong bullish', 'Strong bearish', 'Neutral']