# 📊 NFT Trading Strategies Backtesting System

This project is a **comprehensive NFT trading assistant**, integrating data analysis, technical indicators, time series forecasting, and pattern recognition to support strategy development and decision-making in the NFT market.

---

## 📁 Table of Contents

- [🧠 General Context](#-general-context)
- [🛠️ Technical Specifications](#️-technical-specifications)
- [🧩 System Design](#-system-design)
- [🚀 Implementation](#-implementation)
- [📊 Dashboard](#-dashboard)
- [📌 Screenshots](#-screenshots)
- [📈 Example Use Case](#-example-use-case)
- [📚 Future Improvements](#-future-improvements)
- [📄 License](#-license)

---

## 🧠 General Context

### 1. Introduction
This project addresses the growing complexity of NFT markets by providing data-driven insights and strategies for traders and analysts.

### 2. Situation Analysis
- **Challenges**: Volatility, low liquidity, limited structured data.
- **Opportunities**: Detect patterns, apply predictive models, and backtest strategies.
- **Study of the Existing**: Lacks robust tools tailored for NFTs.

### 3. Project Guidelines
- **Host Entity**: [LAEVITAS](https://app.laevitas.ch/assets/home)
- **Technologies**: Python, Plotly, Streamlit, Scikit-learn, Statsmodels
- **Functional Needs**: Trading signal generation, pattern recognition, data visualization
- **Non-Functional Needs**: Performance, usability, modularity

---

## 🛠️ Technical Specifications

### 1. Technologies Used

- **Programming Language**: Python 3.x
- **Frameworks & Libraries**:
  - `pandas`, `numpy`, JSON – data manipulation
  - `matplotlib`, `plotly` – visualization
  - `scikit-learn`, statsmodels, 'PyTorch'– machine learning and time series
- **Database**: PostgreSQL
- **Machine Learning**: ARIMAX, Gaussian Process Regressor, Prophet

---

## 🧩 System Design

### 1. Technical Indicators Used

- **Oscillating**: RSI, Stochastic RSI
- **Volatility**: Average True Range (ATR), Bollinger Bands
- **Trend**: Moving Average (SMA, EMA)
- **Momentum**: Triple RSI, Volume spikes

### 2. Pattern Detection
- Double Top / Bottom
- Head and Shoulders
- Floor Price Reversal

### 3. Time Series Forecasting
- Stationarity tests
- ACF and PACF analysis
- ARIMA model fitting and validation

---

## 🚀 Implementation

### Implemented Trading Strategies

- ✅ **Buy the Floor**: Buy when price nears historic lows
- ✅ **Bollinger Band Squeeze**: Detect periods of low volatility before breakouts
- ✅ **Moving Average Crossover**: Classic fast/slow EMA strategy
- ✅ **Triple RSI Strategy**: Confirm trends across 3 RSI levels
- ✅ **Pattern-based Trading**: Use detected chart patterns as signals

### Backtesting
- Evaluate historical performance of strategies
- Compare buy/sell signals with actual NFT price movements

---

## 📊 Dashboard

A visual dashboard built with **Streamlit** to:
- Display signals on price charts
- Show forecast results
- Monitor backtest performance
- Interactive filter by date, NFT collection, or strategy

> 🖼️ *Add screenshots in the section below*

---

## 📌 Screenshots

### Strategy Signal Example
![Buy/Sell Signal Example](screenshots/signal-example.png)

### Time Series Forecast Output
![Forecast Example](screenshots/forecast-output.png)

### Pattern Recognition
![Pattern Detection](screenshots/pattern-detection.png)

### Dashboard Interface
![Dashboard](screenshots/dashboard.png)
