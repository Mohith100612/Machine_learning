"""
Generates the stock_prices.csv dataset used by every model in the ML
Dashboard backend.
Run once: python generate_datasets.py
Written to ./datasets/stock_prices.csv
"""
import numpy as np
import pandas as pd
import os

np.random.seed(42)
OUT_DIR = os.path.join(os.path.dirname(__file__), "datasets")
os.makedirs(OUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Stock Prices -> shared by all 5 models
# ---------------------------------------------------------------------------
def gen_stock_prices(n=200):
    prev_close = 100 + np.cumsum(np.random.normal(0.3, 2, n))
    open_p = prev_close + np.random.normal(0, 0.8, n)
    high = open_p + np.abs(np.random.normal(1.5, 0.7, n))
    low = open_p - np.abs(np.random.normal(1.5, 0.7, n))
    volume = np.random.randint(50000, 500000, n)
    volume_z = (volume - volume.mean()) / volume.std()

    # tomorrow's close mostly follows today's open-vs-prev-close move and
    # volume pressure, so both the price itself and its up/down direction
    # relative to prev_close are learnable from the same features
    momentum = 1.8 * (open_p - prev_close) + 1.0 * volume_z
    next_close = prev_close + momentum + np.random.normal(0, 0.5, n)

    df = pd.DataFrame(
        {
            "prev_close": prev_close.round(2),
            "open": open_p.round(2),
            "high": high.round(2),
            "low": low.round(2),
            "volume": volume,
            "next_close": next_close.round(2),
        }
    )
    df.to_csv(os.path.join(OUT_DIR, "stock_prices.csv"), index=False)


if __name__ == "__main__":
    gen_stock_prices()
    print("All datasets generated in", OUT_DIR)
