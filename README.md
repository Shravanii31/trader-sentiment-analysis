Trader Performance vs Market Sentiment (Fear & Greed)

📌 Objective

This project analyzes how **Bitcoin market sentiment (Fear vs Greed)** influences **trader behavior and performance on the Hyperliquid exchange.
The goal is to uncover behavioral patterns and derive **actionable trading insights** based on sentiment regimes.

📊 Datasets Used

1)  Bitcoin Market Sentiment (Fear & Greed Index)

* Columns: `timestamp`, `date`, `classification`, `value`
* Classification indicates market sentiment: **Fear / Greed**
* Source: Provided by Primetrade.ai assignment

2) Hyperliquid Historical Trader Data

* Trade-level data including:

  * Account
  * Trade side (BUY/SELL)
  * Trade size
  * Timestamp
  * Closed PnL
* Covers ~211K trades across multiple accounts

⚙️ Setup & How to Run
- Requirements

* Python 3.9+
* pandas
* matplotlib
* seaborn

- Steps
```bash
# Activate virtual environment
source venv/bin/activate
# Run analysis
python3 analysis.py
```
- Outputs

* `daily_trader_metrics.csv` — aggregated daily trader metrics
* `pnl_by_sentiment.png` — visualization of PnL by sentiment
* Console summary of key statistics

🧹 Data Preparation (Part A)

* Loaded and validated both datasets
* Checked for:

  * Missing values (none found in trades)
  * Duplicate rows (none found)
* Converted timestamps to daily granularity
* Aligned trades with sentiment data by **date**
* Engineered key metrics:

  * Daily PnL per trader
  * Trade count per day
  * Average trade size
  * Long / Short trade counts
  * Long–Short ratio
  * Trader frequency and performance segments

- Analysis & Key Findings (Part B)
1) Trader Performance

* Daily PnL varies significantly across traders
* Frequent traders show higher average PnL compared to infrequent traders

2) Behavioral Patterns

* Trade frequency and position sizing differ across trader segments
* Long/short imbalance provides insight into directional bias

3) Trader Segmentation

* Frequency Segment**: Frequent vs Infrequent traders
* Performance Segment**: Winners vs Losers (based on daily PnL)

These segments help identify which trader profiles perform better under specific market conditions.

💡 Strategy Recommendations (Part C)

- Strategy 1: Risk Control for Low-Performance Traders

* Infrequent or losing traders should **reduce trade frequency and position size**
* Helps limit downside during volatile sentiment periods

- Strategy 2: Leverage Trade Frequency for Consistent Winners

* Frequent and profitable traders can **capitalize on higher trade activity**
* Particularly effective during stable sentiment regimes

These rules of thumb can inform **adaptive trading strategies** based on market sentiment and trader profile.

📂 Repository Structure

```
Trader_Sentiment_Analysis/
│
├── analysis.py                  # Main analysis script
├── README.md                    # Project documentation
├── daily_trader_metrics.csv     # Aggregated metrics output
├── pnl_by_sentiment.png         # Visualization
├── fear_greed.csv               # Sentiment dataset
├── hyperliquid_trades.csv       # Trader dataset
└── venv/                        # Virtual environment
```
🚀 Conclusion

This analysis demonstrates that **market sentiment and trader behavior are closely linked**.
By segmenting traders and analyzing their performance under different sentiment regimes, we can derive practical, data-driven trading strategies**.

✨ Author

Shravani Jadhav
Data Science / Analytics Intern Applicant
Primetrade.ai Assignment
