import streamlit as st
import plotly.graph_objects as go
from src.data.collector import CryptoDataCollector
from src.rag_agent import SimpleRAGAgent
import pandas as pd

# Page config
st.set_page_config(page_title="BGBTC Analysis", layout="wide")

# Initialize our components
@st.cache_resource
def init_components():
    collector = CryptoDataCollector()
    rag_agent = SimpleRAGAgent()
    return collector, rag_agent

collector, rag_agent = init_components()

# Sidebar
st.sidebar.title("BGBTC Analysis")
crypto_symbol = st.sidebar.selectbox(
    "Select Cryptocurrency",
    ["BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "SOL-USD"]
)
timeframe = st.sidebar.selectbox(
    "Select Timeframe",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
)

# Main content
st.title("🚀 Crypto Analysis Dashboard")

# Fetch data
data = collector.fetch_crypto_data(crypto_symbol, timeframe)

if data is not None:
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📈 Price Analysis", "📊 Technical Indicators", "🤖 AI Insights"])
    
    with tab1:
        st.subheader("Price Chart")
        
        # Create candlestick chart
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
        
        fig.update_layout(
            title=f"{crypto_symbol} Price Chart",
            yaxis_title="Price (USD)",
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Market stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            current_price = data['Close'].iloc[-1]
            st.metric("Current Price", f"${current_price:,.2f}")
            
        with col2:
            price_change = ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / 
                          data['Close'].iloc[-2] * 100)
            st.metric("24h Change", f"{price_change:.2f}%")
            
        with col3:
            volume = data['Volume'].iloc[-1]
            st.metric("Volume", f"${volume:,.0f}")
    
    with tab2:
        st.subheader("Technical Analysis")
        
        # Generate trading signals
        signals = rag_agent.generate_trading_signals(data)
        
        # Display signals
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"Trend Signal: {signals['trend']}")
            
        with col2:
            st.info(f"Position: {signals['position']}")
            
        # Technical indicators plot
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'],
                                mode='lines',
                                name='Price'))
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'],
                                mode='lines',
                                name='SMA 20'))
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA50'],
                                mode='lines',
                                name='SMA 50'))
                                
        fig.update_layout(
            title="Price with Moving Averages",
            yaxis_title="Price (USD)",
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("AI Analysis")
        
        # Generate insights
        insights = rag_agent.analyze_crypto_data(data)
        
        for insight in insights:
            st.write(f"• {insight}")
            
        # Add interactive Q&A
        st.subheader("Ask Questions")
        question = st.text_input("What would you like to know about the market?")
        
        if question:
            # Add market context to knowledge base
            market_context = [
                f"The current price of {crypto_symbol} is ${data['Close'].iloc[-1]:,.2f}",
                f"The market trend is {signals['trend']}",
                f"The trading volume is ${data['Volume'].iloc[-1]:,.0f}"
            ]
            rag_agent.add_knowledge(market_context)
            
            # Get response
            responses = rag_agent.query(question)
            
            for response in responses:
                st.write(response['document'])
else:
    st.error("Error fetching data. Please try again.")