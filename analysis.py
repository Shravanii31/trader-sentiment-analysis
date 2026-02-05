import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# Load datasets
# ---------------------------
sentiment = pd.read_csv("fear_greed.csv")
trades = pd.read_csv("hyperliquid_trades.csv")

print("Sentiment shape:", sentiment.shape)
print("Trades shape:", trades.shape)

# ---------------------------
# Clean & align sentiment data
# ---------------------------
sentiment['date'] = pd.to_datetime(sentiment['date']).dt.date
sentiment['classification'] = sentiment['classification'].str.capitalize()

# ---------------------------
# Clean & align trades data
# ---------------------------
trades = trades.rename(columns={
    'Account': 'account',
    'Side': 'side',
    'Closed PnL': 'pnl',
    'Size Tokens': 'size',
    'Timestamp': 'timestamp'
})

trades['date'] = pd.to_datetime(trades['timestamp'], unit='ms').dt.date

# ---------------------------
# Merge on date
# ---------------------------
merged = trades.merge(
    sentiment[['date', 'classification']],
    on='date',
    how='left'
)

print("\nMerged shape:", merged.shape)
print("\nSentiment distribution after merge:")
print(merged['classification'].value_counts(dropna=False))

merged['classification'] = merged['classification'].fillna('Unknown')

# ---------------------------
# Daily metrics
# ---------------------------
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
    daily_metrics['long_trades'] / (daily_metrics['short_trades'] + 1)
)

# ---------------------------
# Analysis outputs
# ---------------------------
print("\nMean PnL by sentiment:")
print(daily_metrics.groupby('classification')['daily_pnl'].mean())

print("\nTrade behavior by sentiment:")
print(
    daily_metrics
    .groupby('classification')[['trades_count', 'avg_trade_size']]
    .mean()
)

# ---------------------------
# Visualization
# ---------------------------
plt.figure(figsize=(8,5))
sns.boxplot(
    x='classification',
    y='daily_pnl',
    data=daily_metrics[daily_metrics['classification'] != 'Unknown']
)
plt.title("Daily Trader PnL by Market Sentiment")
plt.tight_layout()
plt.savefig("pnl_by_sentiment.png")
plt.show()

# ---------------------------
# Save output
# ---------------------------
daily_metrics.to_csv("daily_trader_metrics.csv", index=False)
print("\nSaved daily_trader_metrics.csv")
