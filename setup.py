from setuptools import setup, find_packages

setup(
    name="bgbtc",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "yfinance>=0.2.36",
        "pandas>=2.2.0",
        "numpy>=1.26.3",
        "requests>=2.31.0",
        "plotly>=5.18.0",
        "ta>=0.11.0",
        "cryptocmd>=0.6.1",
        "streamlit>=1.31.0",
        "scikit-learn>=1.4.0",
        "transformers>=4.37.2",
        "sentence-transformers>=2.3.1",
        "python-dotenv>=1.0.0",
    ],
    author="Mahmoud Omar",
    author_email="your.email@example.com",
    description="A comprehensive cryptocurrency analysis tool with RAG capabilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mahmoudomarus/BGBTC",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)