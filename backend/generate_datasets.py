"""
Generates the 5 sample datasets used by the ML Dashboard backend.
Run once: python generate_datasets.py
All datasets are written to ./datasets/*.csv
"""
import numpy as np
import pandas as pd
import os

np.random.seed(42)
OUT_DIR = os.path.join(os.path.dirname(__file__), "datasets")
os.makedirs(OUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Linear Regression -> Stock Price Prediction
# ---------------------------------------------------------------------------
def gen_stock_prices(n=80):
    prev_close = 100 + np.cumsum(np.random.normal(0.3, 2, n))
    open_p = prev_close + np.random.normal(0, 0.8, n)
    high = open_p + np.abs(np.random.normal(1.5, 0.7, n))
    low = open_p - np.abs(np.random.normal(1.5, 0.7, n))
    volume = np.random.randint(50000, 500000, n)
    # next day close depends mostly on prev_close/open/high/low + a bit of volume noise
    next_close = (
        0.4 * prev_close
        + 0.3 * open_p
        + 0.15 * high
        + 0.15 * low
        + (volume - volume.mean()) / volume.std() * 0.5
        + np.random.normal(0, 1.0, n)
    )
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


# ---------------------------------------------------------------------------
# 2. Logistic Regression -> Student Pass/Fail Prediction
# ---------------------------------------------------------------------------
def gen_student_pass_fail(n=90):
    hours_studied = np.round(np.random.uniform(0, 12, n), 1)
    attendance = np.round(np.random.uniform(40, 100, n), 1)
    previous_score = np.round(np.random.uniform(30, 100, n), 1)
    score = (
        0.45 * hours_studied
        + 0.05 * attendance
        + 0.04 * previous_score
        - 4.5
        + np.random.normal(0, 1.2, n)
    )
    prob = 1 / (1 + np.exp(-score))
    passed = (prob > 0.5).astype(int)
    df = pd.DataFrame(
        {
            "hours_studied": hours_studied,
            "attendance_percentage": attendance,
            "previous_score": previous_score,
            "passed": passed,
        }
    )
    df.to_csv(os.path.join(OUT_DIR, "student_pass_fail.csv"), index=False)


# ---------------------------------------------------------------------------
# 3. Decision Tree -> Play Tennis Prediction (classic dataset, extended)
# ---------------------------------------------------------------------------
def gen_play_tennis():
    rows = [
        ("Sunny", "Hot", "High", "Weak", "No"),
        ("Sunny", "Hot", "High", "Strong", "No"),
        ("Overcast", "Hot", "High", "Weak", "Yes"),
        ("Rain", "Mild", "High", "Weak", "Yes"),
        ("Rain", "Cool", "Normal", "Weak", "Yes"),
        ("Rain", "Cool", "Normal", "Strong", "No"),
        ("Overcast", "Cool", "Normal", "Strong", "Yes"),
        ("Sunny", "Mild", "High", "Weak", "No"),
        ("Sunny", "Cool", "Normal", "Weak", "Yes"),
        ("Rain", "Mild", "Normal", "Weak", "Yes"),
        ("Sunny", "Mild", "Normal", "Strong", "Yes"),
        ("Overcast", "Mild", "High", "Strong", "Yes"),
        ("Overcast", "Hot", "Normal", "Weak", "Yes"),
        ("Rain", "Mild", "High", "Strong", "No"),
        ("Sunny", "Hot", "Normal", "Weak", "Yes"),
        ("Rain", "Hot", "High", "Strong", "No"),
        ("Overcast", "Cool", "High", "Weak", "Yes"),
        ("Sunny", "Cool", "High", "Strong", "No"),
        ("Rain", "Cool", "High", "Weak", "Yes"),
        ("Overcast", "Mild", "Normal", "Weak", "Yes"),
    ]
    df = pd.DataFrame(rows, columns=["outlook", "temperature", "humidity", "wind", "play"])
    df.to_csv(os.path.join(OUT_DIR, "play_tennis.csv"), index=False)


# ---------------------------------------------------------------------------
# 4. Random Forest -> Fruit Classification
# ---------------------------------------------------------------------------
def gen_fruits(n_per_class=25):
    def make(label, weight_mean, weight_sd, size_mean, size_sd, red, green, blue):
        weight = np.round(np.random.normal(weight_mean, weight_sd, n_per_class), 1)
        size = np.round(np.random.normal(size_mean, size_sd, n_per_class), 1)
        red_c = np.clip(np.round(np.random.normal(red, 15, n_per_class)), 0, 255).astype(int)
        green_c = np.clip(np.round(np.random.normal(green, 15, n_per_class)), 0, 255).astype(int)
        blue_c = np.clip(np.round(np.random.normal(blue, 15, n_per_class)), 0, 255).astype(int)
        return pd.DataFrame(
            {
                "weight_g": weight,
                "diameter_cm": size,
                "red": red_c,
                "green": green_c,
                "blue": blue_c,
                "fruit": label,
            }
        )

    apple = make("Apple", 150, 15, 7.5, 0.5, 190, 40, 40)
    orange = make("Orange", 170, 12, 7.8, 0.4, 230, 130, 30)
    banana = make("Banana", 120, 10, 3.5, 0.3, 230, 210, 60)
    grape = make("Grape", 6, 1.2, 1.4, 0.2, 100, 40, 120)

    df = pd.concat([apple, orange, banana, grape], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(os.path.join(OUT_DIR, "fruits.csv"), index=False)


# ---------------------------------------------------------------------------
# 5. Gradient Boosting -> House Price Prediction
# ---------------------------------------------------------------------------
def gen_house_prices(n=100):
    area = np.round(np.random.uniform(500, 4500, n))
    bedrooms = np.random.randint(1, 6, n)
    bathrooms = np.random.randint(1, 4, n)
    age = np.random.randint(0, 40, n)
    location_score = np.round(np.random.uniform(1, 10, n), 1)
    price = (
        area * 120
        + bedrooms * 8000
        + bathrooms * 6000
        - age * 900
        + location_score * 9000
        + np.random.normal(0, 12000, n)
        + 20000
    )
    price = np.round(np.clip(price, 25000, None), -2)
    df = pd.DataFrame(
        {
            "area_sqft": area.astype(int),
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "age_years": age,
            "location_score": location_score,
            "price": price.astype(int),
        }
    )
    df.to_csv(os.path.join(OUT_DIR, "house_prices.csv"), index=False)


# ---------------------------------------------------------------------------
# 6. K-Means -> Customer Segmentation
# ---------------------------------------------------------------------------
def gen_customers(n_per_segment=30):
    # (age_mean, age_sd, income_mean, income_sd, spending_mean, spending_sd)
    segments = [
        (26, 4, 35, 6, 78, 8),   # young, modest income, high spenders
        (43, 6, 95, 10, 80, 7),  # affluent high spenders
        (52, 8, 88, 12, 24, 8),  # affluent careful spenders
        (38, 9, 38, 7, 30, 9),   # budget-conscious low spenders
    ]
    frames = []
    for age_m, age_s, inc_m, inc_s, sp_m, sp_s in segments:
        frames.append(
            pd.DataFrame(
                {
                    "age": np.clip(
                        np.random.normal(age_m, age_s, n_per_segment).round(), 18, 75
                    ).astype(int),
                    "annual_income_k": np.round(
                        np.clip(np.random.normal(inc_m, inc_s, n_per_segment), 12, 160), 1
                    ),
                    "spending_score": np.clip(
                        np.random.normal(sp_m, sp_s, n_per_segment).round(), 1, 100
                    ).astype(int),
                }
            )
        )
    df = pd.concat(frames, ignore_index=True).sample(frac=1, random_state=42)
    df.reset_index(drop=True).to_csv(os.path.join(OUT_DIR, "customers.csv"), index=False)


# ---------------------------------------------------------------------------
# 7. Hierarchical Clustering -> Country Development Grouping
# ---------------------------------------------------------------------------
def gen_countries(n_per_tier=20):
    # (gdp_mean, gdp_sd, life_mean, life_sd, internet_mean, internet_sd, urban_mean, urban_sd)
    tiers = [
        (52, 9, 81, 2.0, 91, 4, 82, 7),   # advanced economies
        (17, 5, 73, 2.5, 68, 8, 62, 9),   # emerging economies
        (3.5, 1.5, 62, 3.0, 32, 9, 38, 9),  # developing economies
    ]
    frames = []
    for gdp_m, gdp_s, life_m, life_s, net_m, net_s, urb_m, urb_s in tiers:
        frames.append(
            pd.DataFrame(
                {
                    "gdp_per_capita_k": np.round(
                        np.clip(np.random.normal(gdp_m, gdp_s, n_per_tier), 0.8, 90), 1
                    ),
                    "life_expectancy": np.round(
                        np.clip(np.random.normal(life_m, life_s, n_per_tier), 50, 90), 1
                    ),
                    "internet_users_pct": np.round(
                        np.clip(np.random.normal(net_m, net_s, n_per_tier), 2, 99), 1
                    ),
                    "urban_pop_pct": np.round(
                        np.clip(np.random.normal(urb_m, urb_s, n_per_tier), 10, 98), 1
                    ),
                }
            )
        )
    df = pd.concat(frames, ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)
    df.insert(0, "country", [f"Country-{i + 1:02d}" for i in range(len(df))])
    df.to_csv(os.path.join(OUT_DIR, "countries.csv"), index=False)


# ---------------------------------------------------------------------------
# 8. PCA -> Wine Chemical Profile Compression
# ---------------------------------------------------------------------------
def gen_wines(n_per_style=35):
    # (alcohol, malic_acid, flavanoids, color_intensity, hue, proline)
    styles = [
        (13.7, 2.0, 3.0, 5.5, 1.05, 1100),  # bold red
        (12.3, 1.9, 2.1, 3.0, 1.05, 520),   # light red
        (13.1, 3.3, 0.8, 7.3, 0.68, 630),   # fortified / dessert
    ]
    sds = (0.45, 0.55, 0.35, 1.1, 0.09, 130)
    frames = []
    for means in styles:
        frames.append(
            pd.DataFrame(
                {
                    "alcohol": np.round(np.random.normal(means[0], sds[0], n_per_style), 2),
                    "malic_acid": np.round(
                        np.clip(np.random.normal(means[1], sds[1], n_per_style), 0.5, 6), 2
                    ),
                    "flavanoids": np.round(
                        np.clip(np.random.normal(means[2], sds[2], n_per_style), 0.2, 5), 2
                    ),
                    "color_intensity": np.round(
                        np.clip(np.random.normal(means[3], sds[3], n_per_style), 1, 13), 2
                    ),
                    "hue": np.round(
                        np.clip(np.random.normal(means[4], sds[4], n_per_style), 0.4, 1.8), 2
                    ),
                    "proline": np.clip(
                        np.random.normal(means[5], sds[5], n_per_style), 250, 1700
                    ).astype(int),
                }
            )
        )
    df = pd.concat(frames, ignore_index=True).sample(frac=1, random_state=42)
    df.reset_index(drop=True).to_csv(os.path.join(OUT_DIR, "wines.csv"), index=False)


# ---------------------------------------------------------------------------
# 9. DBSCAN -> Taxi Pickup Hotspot Detection
# ---------------------------------------------------------------------------
def gen_taxi_pickups():
    # dense hotspots: (center_x, center_y, spread, n_points)
    hotspots = [
        (2.0, 3.0, 0.30, 60),   # downtown
        (7.5, 6.5, 0.40, 50),   # airport
        (4.5, 8.5, 0.28, 40),   # stadium
    ]
    xs, ys = [], []
    for cx, cy, sd, n in hotspots:
        xs.append(np.random.normal(cx, sd, n))
        ys.append(np.random.normal(cy, sd, n))
    # scattered noise pickups across the city
    xs.append(np.random.uniform(0, 10, 18))
    ys.append(np.random.uniform(0, 10, 18))
    df = pd.DataFrame(
        {
            "pickup_x_km": np.round(np.concatenate(xs), 2),
            "pickup_y_km": np.round(np.concatenate(ys), 2),
        }
    )
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(os.path.join(OUT_DIR, "taxi_pickups.csv"), index=False)


# ---------------------------------------------------------------------------
# 10. Autoencoder -> Machine Sensor Anomaly Detection
# ---------------------------------------------------------------------------
def gen_sensor_readings(n_normal=140, n_anomaly=20):
    def normal_batch(n):
        return pd.DataFrame(
            {
                "temperature_c": np.round(np.random.normal(65, 3, n), 1),
                "vibration_mm_s": np.round(np.clip(np.random.normal(2.0, 0.3, n), 0.5, 10), 2),
                "pressure_kpa": np.round(np.random.normal(101, 2.5, n), 1),
                "rpm": np.random.normal(1500, 60, n).astype(int),
                "voltage_v": np.round(np.random.normal(230, 4, n), 1),
            }
        )

    normal = normal_batch(n_normal)
    normal["status"] = "Normal"

    anomalies = normal_batch(n_anomaly)
    anomalies["rpm"] = anomalies["rpm"].astype(float)
    # each anomaly gets 1-3 sensors pushed far outside the normal range
    shifts = {
        "temperature_c": 18,
        "vibration_mm_s": 2.5,
        "pressure_kpa": 14,
        "rpm": 350,
        "voltage_v": 25,
    }
    cols = list(shifts.keys())
    for i in range(n_anomaly):
        for col in np.random.choice(cols, size=np.random.randint(1, 4), replace=False):
            direction = np.random.choice([-1, 1])
            anomalies.loc[i, col] = round(
                anomalies.loc[i, col] + direction * shifts[col] * np.random.uniform(0.8, 1.4), 2
            )
    anomalies["rpm"] = anomalies["rpm"].astype(int)
    anomalies["status"] = "Anomaly"

    df = pd.concat([normal, anomalies], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(os.path.join(OUT_DIR, "sensor_readings.csv"), index=False)


if __name__ == "__main__":
    gen_stock_prices()
    gen_student_pass_fail()
    gen_play_tennis()
    gen_fruits()
    gen_house_prices()
    gen_customers()
    gen_countries()
    gen_wines()
    gen_taxi_pickups()
    gen_sensor_readings()
    print("All datasets generated in", OUT_DIR)
