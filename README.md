# Signal Lab — Machine Learning Dashboard

A full-stack dashboard covering 10 classic machine-learning models — 5
supervised and 5 unsupervised — each with its own page: sample dataset, input
form, live prediction, confidence score, and a plain-English explanation of
how the model works.

### Supervised learning

| # | Model | Use case | Task |
|---|-------|----------|------|
| 01 | Linear Regression | Stock Price Prediction | Regression |
| 02 | Logistic Regression | Student Pass/Fail Prediction | Classification |
| 03 | Decision Tree | Play Tennis Prediction | Classification |
| 04 | Random Forest | Fruit Classification | Classification |
| 05 | Gradient Boosting | House Price Prediction | Regression |

### Unsupervised learning

| # | Model | Use case | Task |
|---|-------|----------|------|
| 06 | K-Means | Customer Segmentation | Clustering |
| 07 | Hierarchical Clustering | Country Development Grouping | Clustering |
| 08 | PCA | Wine Chemical Profile Compression | Dimensionality reduction |
| 09 | DBSCAN | Taxi Pickup Hotspot Detection | Clustering + outliers |
| 10 | Autoencoder | Machine Sensor Anomaly Detection | Anomaly detection |

## Stack

- **Backend:** Python, Flask, scikit-learn, pandas — trains all 10 models
  in-memory on startup (a few seconds) and serves a REST API.
- **Frontend:** React 18 + Vite + Tailwind CSS + React Router + Axios.

## Project structure

```
ml-dashboard/
├── backend/
│   ├── app.py                 # Flask app: training + API routes
│   ├── generate_datasets.py   # Generates the 10 sample CSV datasets
│   ├── requirements.txt
│   └── datasets/              # Pre-generated sample data (CSV)
└── frontend/
    ├── src/
    │   ├── pages/              # One page per model
    │   ├── components/         # DataTable, ConfidenceGauge, Navbar, layout
    │   ├── api.js               # API client
    │   └── App.jsx / main.jsx / index.css
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

## Running it locally

### 1. Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
python generate_datasets.py   # already generated, re-run only if you want fresh data
python app.py
```

The API starts on **http://localhost:5000**. Health check: `GET /api/health`.

### 2. Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The app starts on **http://localhost:5173** and proxies all `/api/*`
requests to the Flask backend (see `vite.config.js`), so no CORS
configuration is needed in development.

To build for production:

```bash
npm run build   # outputs static files to frontend/dist
npm run preview # serve the production build locally
```

If you deploy the backend somewhere other than `localhost:5000`, set
`VITE_API_BASE_URL` (e.g. in a `.env` file in `frontend/`) to the deployed
API URL before building.

## API reference

| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/models` | List all models with metrics |
| GET | `/api/:modelId/sample` | Sample dataset rows for the model |
| GET | `/api/:modelId/info` | Metadata, features, metrics, explanation |
| POST | `/api/:modelId/predict` | Run a prediction. Body = `{feature: value, ...}` |
| GET | `/api/health` | Health check |

`modelId` is one of: `linear-regression`, `logistic-regression`,
`decision-tree`, `random-forest`, `gradient-boosting`, `kmeans`,
`hierarchical-clustering`, `pca`, `dbscan`, `autoencoder`.

### Example predict call

```bash
curl -X POST http://localhost:5000/api/logistic-regression/predict \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 8, "attendance_percentage": 90, "previous_score": 75}'
```

Response:

```json
{
  "prediction": "Pass",
  "confidence": 97.4,
  "probabilities": { "Fail": 2.6, "Pass": 97.4 },
  "task": "classification",
  "metrics": { "accuracy": 1.0 }
}
```

## Notes on the models

- All models are trained fresh in memory every time `app.py` starts —
  there are no pickled model files to go stale. Training takes a few seconds
  for all 10 models combined (the autoencoder is the slowest).
- Regression models (Linear Regression, Gradient Boosting) return a numeric
  prediction plus the model's R² / MAE on a held-out test split.
- Classification models (Logistic Regression, Decision Tree, Random Forest)
  return the predicted class, a confidence percentage, and the full
  probability distribution across classes.
- Datasets are synthetic but realistic, generated with a fixed random seed
  (`generate_datasets.py`) so results are reproducible. The Play Tennis
  dataset is the classic textbook dataset used to teach Decision Trees.

### Notes on the unsupervised models

- **K-Means** (customer data) reports the silhouette score and assigns a new
  customer to the nearest of 4 discovered segments; "confidence" is a softmax
  over distances to the centroids.
- **Hierarchical Clustering** (country data) has no native `predict`, so new
  countries are assigned to the nearest cluster centroid of the 3 tiers cut
  from the Ward-linkage merge tree.
- **PCA** (wine data) returns the 2D projection of a new sample plus the
  variance explained by each principal component.
- **DBSCAN** (taxi pickups) assigns a new pickup to a hotspot only if it lies
  within `eps` of a core point — otherwise it is flagged as noise/outlier,
  exactly like DBSCAN treats training points.
- **Autoencoder** (sensor readings) is a small scikit-learn `MLPRegressor`
  with a 5→4→2→4→5 bottleneck architecture, trained only on normal readings.
  A reading whose reconstruction error exceeds the 99th percentile of normal
  training errors is flagged as an anomaly.
- The unsupervised sample tables include the model's discovered grouping as an
  extra column (`segment`, `group`, `zone`, `pc1`/`pc2`) so you can see what
  the algorithm found in the data.
