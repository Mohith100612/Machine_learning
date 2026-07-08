"""
ML Dashboard Backend
=====================
Flask API that trains 5 supervised-learning models on startup (in-memory,
no pickled artifacts needed) and exposes sample-data / predict / info
endpoints for each of them.

Run:
    pip install -r requirements.txt
    python generate_datasets.py   # only needed once, already generated
    python app.py
Server starts on http://localhost:5000
"""
import os
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score, mean_absolute_error, silhouette_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "datasets")

app = Flask(__name__)
CORS(app)

REGISTRY = {}  # populated by each train_* function


# =============================================================================
# 1. LINEAR REGRESSION — Stock Price Prediction
# =============================================================================
def train_linear_regression():
    df = pd.read_csv(os.path.join(DATA_DIR, "stock_prices.csv"))
    features = ["prev_close", "open", "high", "low", "volume"]
    target = "next_close"

    X_train, X_test, y_train, y_test = train_test_split(
        df[features], df[target], test_size=0.2, random_state=42
    )
    model = LinearRegression()
    model.fit(X_train, y_train)
    r2 = r2_score(y_test, model.predict(X_test))
    mae = mean_absolute_error(y_test, model.predict(X_test))

    REGISTRY["linear-regression"] = {
        "model": model,
        "features": features,
        "target": target,
        "df": df,
        "metrics": {"r2_score": round(r2, 4), "mae": round(mae, 2)},
        "task": "regression",
        "name": "Linear Regression",
        "use_case": "Stock Price Prediction",
        "explanation": (
            "Linear Regression learns a straight-line relationship between the input "
            "features (previous close, open, high, low prices and trading volume) and "
            "the target (next day's closing price). It finds the weights that minimize "
            "the sum of squared errors between predicted and actual prices, producing an "
            "equation of the form y = w1*x1 + w2*x2 + ... + b. It works best when the "
            "relationship between inputs and output is approximately linear."
        ),
    }


# =============================================================================
# 2. LOGISTIC REGRESSION — Student Pass/Fail Prediction
# =============================================================================
def train_logistic_regression():
    df = pd.read_csv(os.path.join(DATA_DIR, "student_pass_fail.csv"))
    features = ["hours_studied", "attendance_percentage", "previous_score"]
    target = "passed"

    X_train, X_test, y_train, y_test = train_test_split(
        df[features], df[target], test_size=0.2, random_state=42, stratify=df[target]
    )
    model = LogisticRegression()
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))

    REGISTRY["logistic-regression"] = {
        "model": model,
        "features": features,
        "target": target,
        "df": df,
        "metrics": {"accuracy": round(acc, 4)},
        "task": "classification",
        "classes": {0: "Fail", 1: "Pass"},
        "name": "Logistic Regression",
        "use_case": "Student Pass/Fail Prediction",
        "explanation": (
            "Logistic Regression estimates the probability that a student passes by "
            "applying the sigmoid function to a weighted sum of study hours, attendance "
            "percentage and previous score. Unlike Linear Regression, its output is "
            "squashed between 0 and 1, which is interpreted as a probability. If the "
            "probability is above 0.5 the model predicts 'Pass', otherwise 'Fail'."
        ),
    }


# =============================================================================
# 3. DECISION TREE — Play Tennis Prediction
# =============================================================================
def train_decision_tree():
    df = pd.read_csv(os.path.join(DATA_DIR, "play_tennis.csv"))
    features = ["outlook", "temperature", "humidity", "wind"]
    target = "play"

    encoders = {}
    df_enc = df.copy()
    for col in features + [target]:
        le = LabelEncoder()
        df_enc[col] = le.fit_transform(df[col])
        encoders[col] = le

    X = df_enc[features]
    y = df_enc[target]
    model = DecisionTreeClassifier(criterion="entropy", max_depth=4, random_state=42)
    model.fit(X, y)
    acc = accuracy_score(y, model.predict(X))  # small dataset -> report train fit

    REGISTRY["decision-tree"] = {
        "model": model,
        "features": features,
        "target": target,
        "df": df,
        "encoders": encoders,
        "metrics": {"accuracy": round(acc, 4)},
        "task": "classification",
        "classes": {i: c for i, c in enumerate(encoders[target].classes_)},
        "name": "Decision Tree",
        "use_case": "Play Tennis Prediction",
        "explanation": (
            "A Decision Tree splits the data step by step using the feature that best "
            "separates the classes at each node (measured here with information gain / "
            "entropy). Starting from 'Outlook', the tree asks a sequence of yes/no style "
            "questions about the weather (temperature, humidity, wind) until it reaches a "
            "leaf that predicts whether tennis will be played. It is easy to interpret "
            "because the decision path can be read as a set of simple rules."
        ),
    }


# =============================================================================
# 4. RANDOM FOREST — Fruit Classification
# =============================================================================
def train_random_forest():
    df = pd.read_csv(os.path.join(DATA_DIR, "fruits.csv"))
    features = ["weight_g", "diameter_cm", "red", "green", "blue"]
    target = "fruit"

    le = LabelEncoder()
    y_enc = le.fit_transform(df[target])
    X_train, X_test, y_train, y_test = train_test_split(
        df[features], y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )
    model = RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))

    REGISTRY["random-forest"] = {
        "model": model,
        "features": features,
        "target": target,
        "df": df,
        "encoder": le,
        "metrics": {"accuracy": round(acc, 4)},
        "task": "classification",
        "classes": {i: c for i, c in enumerate(le.classes_)},
        "name": "Random Forest",
        "use_case": "Fruit Classification",
        "explanation": (
            "Random Forest builds many independent Decision Trees, each trained on a "
            "random subset of the data (bagging) and a random subset of features at "
            "every split. To classify a fruit from its weight, diameter and RGB color, "
            "every tree in the forest 'votes' for a class, and the forest returns the "
            "majority vote as the prediction and the vote share as a confidence score. "
            "Averaging many trees reduces overfitting compared to a single tree."
        ),
    }


# =============================================================================
# 5. GRADIENT BOOSTING — House Price Prediction
# =============================================================================
def train_gradient_boosting():
    df = pd.read_csv(os.path.join(DATA_DIR, "house_prices.csv"))
    features = ["area_sqft", "bedrooms", "bathrooms", "age_years", "location_score"]
    target = "price"

    X_train, X_test, y_train, y_test = train_test_split(
        df[features], df[target], test_size=0.2, random_state=42
    )
    model = GradientBoostingRegressor(
        n_estimators=300, learning_rate=0.05, max_depth=3, random_state=42
    )
    model.fit(X_train, y_train)
    r2 = r2_score(y_test, model.predict(X_test))
    mae = mean_absolute_error(y_test, model.predict(X_test))

    REGISTRY["gradient-boosting"] = {
        "model": model,
        "features": features,
        "target": target,
        "df": df,
        "metrics": {"r2_score": round(r2, 4), "mae": round(mae, 2)},
        "task": "regression",
        "name": "Gradient Boosting",
        "use_case": "House Price Prediction",
        "explanation": (
            "Gradient Boosting builds an ensemble of shallow Decision Trees sequentially: "
            "each new tree is trained to correct the errors (residuals) made by the trees "
            "before it, scaled by a learning rate. For house price prediction, it combines "
            "area, bedrooms, bathrooms, age and location score across 300 small trees to "
            "produce a highly accurate, non-linear price estimate."
        ),
    }


# =============================================================================
# 6. K-MEANS — Customer Segmentation
# =============================================================================
def train_kmeans():
    df = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
    features = ["age", "annual_income_k", "spending_score"]

    scaler = StandardScaler()
    Xs = scaler.fit_transform(df[features])
    model = KMeans(n_clusters=4, n_init=10, random_state=42)
    labels = model.fit_predict(Xs)
    sil = silhouette_score(Xs, labels)

    cluster_names, profiles = {}, {}
    for c in range(4):
        seg = df[labels == c]
        income = "high income" if seg["annual_income_k"].mean() > df["annual_income_k"].mean() else "modest income"
        spend = "high spender" if seg["spending_score"].mean() > df["spending_score"].mean() else "careful spender"
        cluster_names[c] = f"Segment {c + 1}"
        profiles[c] = f"{income}, {spend}"

    df_view = df.copy()
    df_view["segment"] = [cluster_names[c] for c in labels]
    metrics = {"silhouette_score": round(float(sil), 4), "clusters": 4}

    def predict_fn(payload):
        x = scaler.transform(
            pd.DataFrame([[float(payload[f]) for f in features]], columns=features)
        )
        dists = np.linalg.norm(model.cluster_centers_ - x, axis=1)
        scores = np.exp(-dists)
        scores = scores / scores.sum()
        idx = int(np.argmin(dists))
        return {
            "prediction": cluster_names[idx],
            "confidence": float(round(scores[idx] * 100, 2)),
            "probabilities": {
                cluster_names[c]: float(round(s * 100, 2)) for c, s in enumerate(scores)
            },
            "note": f"Segment profile: {profiles[idx]}.",
            "task": "clustering",
            "metrics": metrics,
        }

    REGISTRY["kmeans"] = {
        "model": model,
        "features": features,
        "target": "segment",
        "df": df_view,
        "metrics": metrics,
        "task": "clustering",
        "learning": "unsupervised",
        "predict_fn": predict_fn,
        "name": "K-Means",
        "use_case": "Customer Segmentation",
        "explanation": (
            "K-Means partitions customers into K groups (here K=4) without ever seeing "
            "labels. It places K centroids in the feature space (age, annual income, "
            "spending score), assigns every customer to the nearest centroid, then moves "
            "each centroid to the mean of its assigned customers — repeating until stable. "
            "The discovered segments (e.g. 'high income, careful spender') emerge purely "
            "from the structure of the data. A new customer is assigned to the segment "
            "whose centroid is closest."
        ),
    }


# =============================================================================
# 7. HIERARCHICAL CLUSTERING — Country Development Grouping
# =============================================================================
def train_hierarchical():
    df = pd.read_csv(os.path.join(DATA_DIR, "countries.csv"))
    features = ["gdp_per_capita_k", "life_expectancy", "internet_users_pct", "urban_pop_pct"]

    scaler = StandardScaler()
    Xs = scaler.fit_transform(df[features])
    model = AgglomerativeClustering(n_clusters=3, linkage="ward")
    labels = model.fit_predict(Xs)
    sil = silhouette_score(Xs, labels)

    # name clusters by average GDP so the labels are human-readable
    order = np.argsort([df.loc[labels == c, "gdp_per_capita_k"].mean() for c in range(3)])
    tier_labels = ["Developing economies", "Emerging economies", "Advanced economies"]
    cluster_names = {int(c): tier_labels[rank] for rank, c in enumerate(order)}
    centroids = np.vstack([Xs[labels == c].mean(axis=0) for c in range(3)])

    df_view = df.copy()
    df_view["group"] = [cluster_names[c] for c in labels]
    metrics = {"silhouette_score": round(float(sil), 4), "clusters": 3}

    def predict_fn(payload):
        x = scaler.transform(
            pd.DataFrame([[float(payload[f]) for f in features]], columns=features)
        )
        dists = np.linalg.norm(centroids - x, axis=1)
        scores = np.exp(-dists)
        scores = scores / scores.sum()
        idx = int(np.argmin(dists))
        return {
            "prediction": cluster_names[idx],
            "confidence": float(round(scores[idx] * 100, 2)),
            "probabilities": {
                cluster_names[c]: float(round(s * 100, 2)) for c, s in enumerate(scores)
            },
            "note": "Assigned to the closest cluster centroid (agglomerative clusters have no native predict).",
            "task": "clustering",
            "metrics": metrics,
        }

    REGISTRY["hierarchical-clustering"] = {
        "model": model,
        "features": features,
        "target": "group",
        "df": df_view,
        "metrics": metrics,
        "task": "clustering",
        "learning": "unsupervised",
        "predict_fn": predict_fn,
        "name": "Hierarchical Clustering",
        "use_case": "Country Development Grouping",
        "explanation": (
            "Agglomerative (bottom-up) Hierarchical Clustering starts with every country "
            "as its own cluster and repeatedly merges the two closest clusters — using "
            "Ward linkage, which merges the pair that increases within-cluster variance "
            "the least — building a tree (dendrogram) of merges. Cutting the tree at 3 "
            "clusters reveals natural development tiers from GDP per capita, life "
            "expectancy, internet usage and urbanization. Unlike K-Means you don't need "
            "to know K up front: the dendrogram shows every possible number of clusters."
        ),
    }


# =============================================================================
# 8. PCA — Wine Chemical Profile Compression
# =============================================================================
def train_pca():
    df = pd.read_csv(os.path.join(DATA_DIR, "wines.csv"))
    features = ["alcohol", "malic_acid", "flavanoids", "color_intensity", "hue", "proline"]

    scaler = StandardScaler()
    Xs = scaler.fit_transform(df[features])
    model = PCA(n_components=2, random_state=42)
    proj = model.fit_transform(Xs)
    evr = model.explained_variance_ratio_

    df_view = df.copy()
    df_view["pc1"] = np.round(proj[:, 0], 2)
    df_view["pc2"] = np.round(proj[:, 1], 2)
    metrics = {
        "pc1_variance": round(float(evr[0]) * 100, 1),
        "pc2_variance": round(float(evr[1]) * 100, 1),
        "total_variance": round(float(evr.sum()) * 100, 1),
    }

    def predict_fn(payload):
        x = scaler.transform(
            pd.DataFrame([[float(payload[f]) for f in features]], columns=features)
        )
        p = model.transform(x)[0]
        return {
            "projection": {"PC1": float(round(p[0], 3)), "PC2": float(round(p[1], 3))},
            "explained_variance": {
                "PC1": metrics["pc1_variance"],
                "PC2": metrics["pc2_variance"],
            },
            "note": (
                f"6 chemical measurements compressed to 2 coordinates that keep "
                f"{metrics['total_variance']}% of the original variance."
            ),
            "task": "dimensionality-reduction",
            "metrics": metrics,
        }

    REGISTRY["pca"] = {
        "model": model,
        "features": features,
        "target": None,
        "df": df_view,
        "metrics": metrics,
        "task": "dimensionality-reduction",
        "learning": "unsupervised",
        "predict_fn": predict_fn,
        "name": "PCA",
        "use_case": "Wine Chemical Profile Compression",
        "explanation": (
            "Principal Component Analysis finds new axes (principal components) that "
            "capture the largest possible variance in the data. Each component is a "
            "weighted combination of the original 6 wine measurements, and the components "
            "are ordered: PC1 captures the most variance, PC2 the next most, and so on. "
            "Keeping just the first two turns every wine into a 2D point while preserving "
            "most of the information — useful for visualization, noise reduction and "
            "speeding up downstream models. No labels are involved: PCA only looks at "
            "how the features vary together."
        ),
    }


# =============================================================================
# 9. DBSCAN — Taxi Pickup Hotspot Detection
# =============================================================================
def train_dbscan():
    df = pd.read_csv(os.path.join(DATA_DIR, "taxi_pickups.csv"))
    features = ["pickup_x_km", "pickup_y_km"]

    X = df[features].to_numpy()
    eps = 0.6
    model = DBSCAN(eps=eps, min_samples=5)
    labels = model.fit_predict(X)

    cluster_ids = sorted(set(labels) - {-1})
    n_noise = int((labels == -1).sum())
    # biggest hotspot first: Hotspot A, B, C ...
    sizes = {c: int((labels == c).sum()) for c in cluster_ids}
    cluster_names = {
        c: f"Hotspot {chr(65 + rank)}"
        for rank, c in enumerate(sorted(sizes, key=sizes.get, reverse=True))
    }
    noise_name = "Noise / outlier"
    sil = silhouette_score(X[labels != -1], labels[labels != -1]) if len(cluster_ids) > 1 else 0.0

    core_pts = model.components_
    core_labels = labels[model.core_sample_indices_]

    df_view = df.copy()
    df_view["zone"] = [cluster_names.get(c, noise_name) for c in labels]
    metrics = {
        "silhouette_score": round(float(sil), 4),
        "hotspots_found": len(cluster_ids),
        "noise_points": n_noise,
    }

    def predict_fn(payload):
        x = np.array([[float(payload[f]) for f in features]])
        dists = np.linalg.norm(core_pts - x, axis=1)
        min_dist_per_cluster = {
            int(c): float(dists[core_labels == c].min()) for c in cluster_ids
        }
        raw = {cluster_names[c]: float(np.exp(-d / eps)) for c, d in min_dist_per_cluster.items()}
        raw[noise_name] = float(np.exp(-1.0))  # score of a point exactly eps away
        total = sum(raw.values())
        probs = {k: round(v / total * 100, 2) for k, v in raw.items()}

        best = min(min_dist_per_cluster, key=min_dist_per_cluster.get)
        if min_dist_per_cluster[best] <= eps:
            label = cluster_names[best]
            note = (
                f"Within {eps} km of a core point of {label} "
                f"(distance {min_dist_per_cluster[best]:.2f} km)."
            )
        else:
            label = noise_name
            note = (
                f"No dense hotspot within {eps} km "
                f"(nearest core point is {min_dist_per_cluster[best]:.2f} km away)."
            )
        return {
            "prediction": label,
            "confidence": probs[label],
            "probabilities": probs,
            "note": note,
            "task": "clustering",
            "metrics": metrics,
        }

    REGISTRY["dbscan"] = {
        "model": model,
        "features": features,
        "target": "zone",
        "df": df_view,
        "metrics": metrics,
        "task": "clustering",
        "learning": "unsupervised",
        "predict_fn": predict_fn,
        "name": "DBSCAN",
        "use_case": "Taxi Pickup Hotspot Detection",
        "explanation": (
            "DBSCAN groups points by density: a point with at least min_samples "
            "neighbours within a radius eps becomes a 'core point', and connected core "
            "points grow into clusters of arbitrary shape. Points that don't belong to "
            "any dense region are labelled noise instead of being forced into a cluster — "
            "which is exactly what makes DBSCAN great for hotspot and outlier detection. "
            "Here it discovers the dense taxi pickup zones in a city and flags isolated "
            "pickups as noise, without being told how many hotspots exist."
        ),
    }


# =============================================================================
# 10. AUTOENCODER — Machine Sensor Anomaly Detection
# =============================================================================
def train_autoencoder():
    df = pd.read_csv(os.path.join(DATA_DIR, "sensor_readings.csv"))
    features = ["temperature_c", "vibration_mm_s", "pressure_kpa", "rpm", "voltage_v"]

    normal = df[df["status"] == "Normal"]
    scaler = StandardScaler()
    Xn = scaler.fit_transform(normal[features])

    # 5 -> 4 -> 2 -> 4 -> 5: the 2-unit bottleneck forces compression
    model = MLPRegressor(
        hidden_layer_sizes=(4, 2, 4),
        activation="tanh",
        solver="adam",
        max_iter=5000,
        random_state=42,
    )
    model.fit(Xn, Xn)

    train_err = ((model.predict(Xn) - Xn) ** 2).mean(axis=1)
    threshold = float(np.percentile(train_err, 99))

    X_all = scaler.transform(df[features])
    err_all = ((model.predict(X_all) - X_all) ** 2).mean(axis=1)
    predicted = np.where(err_all > threshold, "Anomaly", "Normal")
    acc = float((predicted == df["status"]).mean())

    metrics = {"accuracy": round(acc, 4), "error_threshold": round(threshold, 4)}

    def predict_fn(payload):
        x = scaler.transform(
            pd.DataFrame([[float(payload[f]) for f in features]], columns=features)
        )
        err = float(((model.predict(x) - x) ** 2).mean())
        ratio = err / threshold
        p_anom = float(1 / (1 + np.exp(-4.0 * (ratio - 1))))
        label = "Anomaly" if p_anom > 0.5 else "Normal"
        return {
            "prediction": label,
            "confidence": round(max(p_anom, 1 - p_anom) * 100, 2),
            "probabilities": {
                "Normal": round((1 - p_anom) * 100, 2),
                "Anomaly": round(p_anom * 100, 2),
            },
            "note": (
                f"Reconstruction error {err:.4f} vs threshold {threshold:.4f} — "
                "readings the network can't reconstruct well are flagged as anomalies."
            ),
            "task": "anomaly-detection",
            "metrics": metrics,
        }

    REGISTRY["autoencoder"] = {
        "model": model,
        "features": features,
        "target": "status",
        "df": df,
        "metrics": metrics,
        "task": "anomaly-detection",
        "learning": "unsupervised",
        "predict_fn": predict_fn,
        "name": "Autoencoder",
        "use_case": "Machine Sensor Anomaly Detection",
        "explanation": (
            "An Autoencoder is a neural network trained to reproduce its own input after "
            "squeezing it through a narrow bottleneck layer (here 5 sensors -> 2 neurons "
            "-> 5 sensors). Trained only on normal machine readings, it becomes very good "
            "at reconstructing 'normal' — so when an unusual reading arrives, the "
            "reconstruction error spikes and the reading is flagged as an anomaly. No "
            "anomaly labels are used during training, which makes autoencoders ideal for "
            "detecting failures that have never been seen before."
        ),
    }


def train_all_models():
    train_linear_regression()
    train_logistic_regression()
    train_decision_tree()
    train_random_forest()
    train_gradient_boosting()
    train_kmeans()
    train_hierarchical()
    train_pca()
    train_dbscan()
    train_autoencoder()
    print(f"Trained {len(REGISTRY)} models: {list(REGISTRY.keys())}")


# =============================================================================
# Helpers
# =============================================================================
def confidence_from_proba(proba_row, classes):
    idx = int(np.argmax(proba_row))
    return classes[idx], float(round(proba_row[idx] * 100, 2)), {
        classes[i]: float(round(p * 100, 2)) for i, p in enumerate(proba_row)
    }


def clean_records(df, n=15):
    """Return first n rows as JSON-safe list of dicts."""
    return df.head(n).to_dict(orient="records")


# =============================================================================
# API ROUTES
# =============================================================================
@app.route("/api/models", methods=["GET"])
def list_models():
    out = []
    for key, entry in REGISTRY.items():
        out.append(
            {
                "id": key,
                "name": entry["name"],
                "use_case": entry["use_case"],
                "task": entry["task"],
                "learning": entry.get("learning", "supervised"),
                "features": entry["features"],
                "metrics": entry["metrics"],
            }
        )
    return jsonify(out)


@app.route("/api/<model_id>/sample", methods=["GET"])
def get_sample(model_id):
    entry = REGISTRY.get(model_id)
    if not entry:
        return jsonify({"error": "Model not found"}), 404
    return jsonify(
        {
            "columns": list(entry["df"].columns),
            "rows": clean_records(entry["df"]),
            "total_rows": len(entry["df"]),
        }
    )


@app.route("/api/<model_id>/info", methods=["GET"])
def get_info(model_id):
    entry = REGISTRY.get(model_id)
    if not entry:
        return jsonify({"error": "Model not found"}), 404
    return jsonify(
        {
            "id": model_id,
            "name": entry["name"],
            "use_case": entry["use_case"],
            "task": entry["task"],
            "learning": entry.get("learning", "supervised"),
            "features": entry["features"],
            "target": entry.get("target"),
            "metrics": entry["metrics"],
            "explanation": entry["explanation"],
            "classes": entry.get("classes"),
        }
    )


@app.route("/api/<model_id>/predict", methods=["POST"])
def predict(model_id):
    entry = REGISTRY.get(model_id)
    if not entry:
        return jsonify({"error": "Model not found"}), 404

    payload = request.get_json(force=True, silent=True) or {}
    features = entry["features"]

    missing = [f for f in features if f not in payload]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        # unsupervised models carry their own prediction logic
        if "predict_fn" in entry:
            return jsonify(entry["predict_fn"](payload))

        if model_id == "decision-tree":
            encoders = entry["encoders"]
            row = []
            for f in features:
                val = str(payload[f])
                if val not in encoders[f].classes_:
                    return jsonify(
                        {"error": f"Invalid value '{val}' for field '{f}'. "
                                  f"Expected one of {list(encoders[f].classes_)}"}
                    ), 400
                row.append(encoders[f].transform([val])[0])
            X = pd.DataFrame([row], columns=features)
        else:
            X = pd.DataFrame([[float(payload[f]) for f in features]], columns=features)

        model = entry["model"]

        if entry["task"] == "regression":
            pred = float(model.predict(X)[0])
            response = {
                "prediction": round(pred, 2),
                "task": "regression",
                "metrics": entry["metrics"],
            }
        else:
            classes = entry["classes"]
            pred_label_idx = int(model.predict(X)[0])
            proba = model.predict_proba(X)[0]
            label, confidence, full_proba = confidence_from_proba(proba, classes)
            response = {
                "prediction": label,
                "confidence": confidence,
                "probabilities": full_proba,
                "task": "classification",
                "metrics": entry["metrics"],
            }

        return jsonify(response)

    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "models_loaded": list(REGISTRY.keys())})


if __name__ == "__main__":
    train_all_models()
    app.run(host="0.0.0.0", port=5000, debug=True)
