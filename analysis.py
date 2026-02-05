import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# LOAD DATA
# =========================
sentiment = pd.read_csv("fear_greed.csv")
trades = pd.read_csv("hyperliquid_trades.csv")

print("Sentiment shape:", sentiment.shape)
print("Trades shape:", trades.shape)

# =========================
# BASIC DATA CHECKS
# =========================
print("\nMissing values in trades:")
print(trades.isna().sum())

print("\nDuplicate rows in trades:", trades.duplicated().sum())

# =========================
# DATE PROCESSING
# =========================
sentiment['date'] = pd.to_datetime(sentiment['date']).dt.date

trades = trades.rename(columns={
    'Account': 'account',
    'Side': 'side',
    'Closed PnL': 'pnl',
    'Size Tokens': 'size',
    'Timestamp': 'timestamp'
})

trades['date'] = pd.to_datetime(trades['timestamp']).dt.date

# =========================
# MERGE (LEFT JOIN ON PURPOSE)
# =========================
merged = trades.merge(
    sentiment[['date', 'classification']],
    on='date',
    how='left'
)

merged['classification'] = merged['classification'].fillna('Unknown')

print("\nMerged shape:", merged.shape)
print("\nSentiment distribution after merge:")
print(merged['classification'].value_counts())

# =========================
# DAILY TRADER METRICS
# =========================
daily_metrics = (
    merged
    .groupby(['account', 'date', 'classification'])
    .agg(
        daily_pnl=('pnl', 'sum'),
        trades_count=('pnl', 'count'),
        avg_trade_size=('size', 'mean'),
        long_trades=('side', lambda x: (x == 'BUY').sum()),
        short_trades=('side', lambda x: (x == 'SELL').sum())
    )
    .reset_index()
)

daily_metrics['long_short_ratio'] = (
    daily_metrics['long_trades'] /
    (daily_metrics['short_trades'] + 1)
)

# =========================
# AGGREGATE ANALYSIS
# =========================
print("\nMean PnL by sentiment:")
print(daily_metrics.groupby('classification')['daily_pnl'].mean())

print("\nTrade behavior by sentiment:")
print(
    daily_metrics
    .groupby('classification')[['trades_count', 'avg_trade_size']]
    .mean()
)

# =========================
# TRADER SEGMENTATION
# =========================
if not daily_metrics.empty:
    daily_metrics['freq_segment'] = pd.qcut(
        daily_metrics['trades_count'],
        q=2,
        labels=['Infrequent', 'Frequent']
    )

    daily_metrics['performance_segment'] = daily_metrics['daily_pnl'].apply(
        lambda x: 'Winner' if x > 0 else 'Loser'
    )

    print("\nPerformance by frequency segment:")
    print(
        daily_metrics
        .groupby(['classification', 'freq_segment'])['daily_pnl']
        .mean()
    )

# =========================
# VISUALIZATION
# =========================
sns.boxplot(
    x='classification',
    y='daily_pnl',
    data=daily_metrics
)
plt.title("Daily Trader PnL by Market Sentiment")
plt.tight_layout()
plt.savefig("pnl_by_sentiment.png")
plt.close()

# =========================
# SAVE OUTPUT
# =========================
daily_metrics.to_csv("daily_trader_metrics.csv", index=False)
print("\nSaved daily_trader_metrics.csv and pnl_by_sentiment.png")
