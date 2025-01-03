import pandas as pd
import numpy as np
from typing import Dict, List, Union, Optional
import logging
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate various technical indicators for cryptocurrency data.
    
    Args:
        df: DataFrame with OHLCV data
        
    Returns:
        DataFrame with additional technical indicators
    """
    try:
        # Make a copy to avoid modifying original data
        df = df.copy()
        
        # Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # Exponential Moving Averages
        df['EMA_12'] = df['Close'].ewm(span=12).mean()
        df['EMA_26'] = df['Close'].ewm(span=26).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (std * 2)
        
        # Average True Range (ATR)
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['ATR'] = true_range.rolling(14).mean()
        
        return df
        
    except Exception as e:
        logger.error(f"Error calculating technical indicators: {e}")
        raise

def calculate_volatility(df: pd.DataFrame, window: int = 20) -> pd.Series:
    """
    Calculate historical volatility.
    
    Args:
        df: DataFrame with price data
        window: Rolling window for volatility calculation
        
    Returns:
        Series with volatility values
    """
    try:
        returns = np.log(df['Close'] / df['Close'].shift(1))
        volatility = returns.rolling(window=window).std() * np.sqrt(252)  # Annualized
        return volatility
        
    except Exception as e:
        logger.error(f"Error calculating volatility: {e}")
        raise

def identify_support_resistance(df: pd.DataFrame, window: int = 20, num_points: int = 5) -> Dict[str, List[float]]:
    """
    Identify potential support and resistance levels.
    
    Args:
        df: DataFrame with price data
        window: Rolling window for level identification
        num_points: Number of support/resistance points to identify
        
    Returns:
        Dictionary with support and resistance levels
    """
    try:
        levels = {
            'support': [],
            'resistance': []
        }
        
        # Find local minimums (support)
        for i in range(window, len(df) - window):
            if all(df['Low'].iloc[i] <= df['Low'].iloc[i-window:i]) and \
               all(df['Low'].iloc[i] <= df['Low'].iloc[i+1:i+window+1]):
                levels['support'].append(df['Low'].iloc[i])
        
        # Find local maximums (resistance)
        for i in range(window, len(df) - window):
            if all(df['High'].iloc[i] >= df['High'].iloc[i-window:i]) and \
               all(df['High'].iloc[i] >= df['High'].iloc[i+1:i+window+1]):
                levels['resistance'].append(df['High'].iloc[i])
        
        # Sort and take top points
        levels['support'] = sorted(levels['support'])[-num_points:]
        levels['resistance'] = sorted(levels['resistance'])[-num_points:]
        
        return levels
        
    except Exception as e:
        logger.error(f"Error identifying support/resistance levels: {e}")
        raise

def calculate_risk_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate various risk metrics for the asset.
    
    Args:
        df: DataFrame with price data
        
    Returns:
        Dictionary with risk metrics
    """
    try:
        metrics = {}
        
        # Calculate daily returns
        returns = df['Close'].pct_change()
        
        # Sharpe Ratio (assuming risk-free rate of 2%)
        risk_free_rate = 0.02
        excess_returns = returns - risk_free_rate/252
        metrics['sharpe_ratio'] = np.sqrt(252) * (excess_returns.mean() / returns.std())
        
        # Maximum Drawdown
        cumulative_returns = (1 + returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdowns = cumulative_returns / rolling_max - 1
        metrics['max_drawdown'] = drawdowns.min()
        
        # Value at Risk (95% confidence)
        metrics['var_95'] = np.percentile(returns, 5)
        
        # Beta (compared to broader market - using BTC as proxy)
        if 'Market_Return' in df.columns:
            market_returns = df['Market_Return'].pct_change()
            covariance = returns.cov(market_returns)
            market_variance = market_returns.var()
            metrics['beta'] = covariance / market_variance
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error calculating risk metrics: {e}")
        raise

def generate_summary_statistics(df: pd.DataFrame) -> Dict[str, Union[float, str]]:
    """
    Generate summary statistics for the asset.
    
    Args:
        df: DataFrame with price data
        
    Returns:
        Dictionary with summary statistics
    """
    try:
        stats = {}
        
        # Price statistics
        stats['current_price'] = df['Close'].iloc[-1]
        stats['price_change_24h'] = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / 
                                   df['Close'].iloc[-2] * 100)
        stats['price_change_7d'] = ((df['Close'].iloc[-1] - df['Close'].iloc[-7]) / 
                                  df['Close'].iloc[-7] * 100)
        
        # Volume statistics
        stats['current_volume'] = df['Volume'].iloc[-1]
        stats['avg_volume_7d'] = df['Volume'].tail(7).mean()
        
        # Volatility
        stats['volatility_30d'] = calculate_volatility(df, 30).iloc[-1]
        
        # Technical indicators
        df_tech = calculate_technical_indicators(df)
        stats['rsi'] = df_tech['RSI'].iloc[-1]
        stats['macd'] = df_tech['MACD'].iloc[-1]
        
        # Trend
        stats['trend'] = 'Bullish' if df_tech['SMA_20'].iloc[-1] > df_tech['SMA_50'].iloc[-1] else 'Bearish'
        
        return stats
        
    except Exception as e:
        logger.error(f"Error generating summary statistics: {e}")
        raise

def format_number(number: float, decimals: int = 2) -> str:
    """
    Format numbers for display with appropriate suffixes (K, M, B).
    
    Args:
        number: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted string
    """
    try:
        if number >= 1e9:
            return f"${number/1e9:.{decimals}f}B"
        elif number >= 1e6:
            return f"${number/1e6:.{decimals}f}M"
        elif number >= 1e3:
            return f"${number/1e3:.{decimals}f}K"
        else:
            return f"${number:.{decimals}f}"
    except Exception as e:
        logger.error(f"Error formatting number: {e}")
        return str(number)

if __name__ == "__main__":
    # Example usage
    try:
        # Create sample data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        data = {
            'Open': np.random.randn(100).cumsum() + 100,
            'High': np.random.randn(100).cumsum() + 102,
            'Low': np.random.randn(100).cumsum() + 98,
            'Close': np.random.randn(100).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 100)
        }
        df = pd.DataFrame(data, index=dates)
        
        # Test functions
        print("Testing technical indicators...")
        df_tech = calculate_technical_indicators(df)
        print("Technical indicators added:", df_tech.columns.tolist())
        
        print("\nTesting support/resistance levels...")
        levels = identify_support_resistance(df)
        print("Support levels:", [format_number(x) for x in levels['support']])
        print("Resistance levels:", [format_number(x) for x in levels['resistance']])
        
        print("\nTesting risk metrics...")
        metrics = calculate_risk_metrics(df)
        print("Risk metrics:", metrics)
        
        print("\nTesting summary statistics...")
        stats = generate_summary_statistics(df)
        print("Summary statistics:", stats)
        
    except Exception as e:
        logger.error(f"Error in example usage: {e}")
