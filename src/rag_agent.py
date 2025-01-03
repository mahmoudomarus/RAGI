from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from typing import List, Dict, Any

class SimpleRAGAgent:
    def __init__(self):
        # Using a free, lightweight model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = []
        self.embeddings = None
        
    def add_knowledge(self, documents: List[str]):
        """
        Add documents to the knowledge base
        """
        self.knowledge_base.extend(documents)
        # Create embeddings for all documents
        self.embeddings = self.model.encode(self.knowledge_base)
        
    def query(self, question: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Query the knowledge base
        """
        if not self.knowledge_base:
            return []
            
        # Create question embedding
        question_embedding = self.model.encode([question])[0]
        
        # Calculate similarities
        similarities = cosine_similarity([question_embedding], self.embeddings)[0]
        
        # Get top-k most similar documents
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                'document': self.knowledge_base[idx],
                'similarity': similarities[idx]
            })
            
        return results
        
    def analyze_crypto_data(self, data: pd.DataFrame) -> List[str]:
        """
        Generate analysis insights from crypto data
        """
        insights = []
        
        # Price trend analysis
        current_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2]
        price_change = ((current_price - prev_price) / prev_price) * 100
        
        if price_change > 0:
            insights.append(f"Price increased by {price_change:.2f}% in the last period")
        else:
            insights.append(f"Price decreased by {abs(price_change):.2f}% in the last period")
            
        # Volume analysis
        avg_volume = data['Volume'].mean()
        current_volume = data['Volume'].iloc[-1]
        
        if current_volume > avg_volume:
            insights.append("Trading volume is above average, indicating strong market activity")
        else:
            insights.append("Trading volume is below average, indicating reduced market activity")
            
        # Volatility analysis
        returns = data['Close'].pct_change()
        volatility = returns.std() * np.sqrt(252)  # Annualized volatility
        insights.append(f"Current annualized volatility: {volatility:.2f}")
        
        return insights
        
    def generate_trading_signals(self, data: pd.DataFrame) -> Dict[str, str]:
        """
        Generate trading signals based on technical indicators
        """
        # Calculate basic technical indicators
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        
        current_price = data['Close'].iloc[-1]
        sma20 = data['SMA20'].iloc[-1]
        sma50 = data['SMA50'].iloc[-1]
        
        # Generate signals
        signals = {}
        
        # Trend signal
        if sma20 > sma50:
            signals['trend'] = 'Bullish'
        else:
            signals['trend'] = 'Bearish'
            
        # Price position
        if current_price > sma20 and current_price > sma50:
            signals['position'] = 'Strong bullish'
        elif current_price < sma20 and current_price < sma50:
            signals['position'] = 'Strong bearish'
        else:
            signals['position'] = 'Neutral'
            
        return signals

if __name__ == "__main__":
    # Example usage
    agent = SimpleRAGAgent()
    
    # Add some example knowledge
    knowledge = [
        "Bitcoin is a decentralized cryptocurrency.",
        "Technical analysis uses chart patterns to predict price movements.",
        "Trading volume can indicate market strength or weakness."
    ]
    agent.add_knowledge(knowledge)
    
    # Example query
    results = agent.query("What is Bitcoin?")
    print("Query results:", results)