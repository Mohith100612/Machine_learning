# Signal Lab — Machine Learning Dashboard

A full-stack dashboard covering 5 classic supervised machine-learning models,
all trained on a single stock price dataset, each with its own page: sample
dataset, input form, live prediction, confidence score, and a plain-English
explanation of how the model works.

### Supervised learning

| # | Model | Use case | Task |
|---|-------|----------|------|
| 01 | Linear Regression | Stock Price Change Prediction | Regression |
| 02 | Logistic Regression | Stock Price Movement Prediction | Classification |
| 03 | Decision Tree | Stock Price Movement Prediction | Classification |
| 04 | Random Forest | Stock Price Movement Prediction | Classification |
| 05 | Gradient Boosting | Stock Price Change Prediction | Regression |

All 5 models train on the same features — previous close, open, high, low
price and trading volume. The two regression models (Linear Regression,
Gradient Boosting) predict a derived `price_change` target — the dollar size
of tomorrow's move (next close minus previous close) — rather than the raw
next-day price level, since predicting a raw price level trivially inherits
day-to-day price autocorrelation and inflates R² without reflecting real
predictive skill. The three classification models (Logistic Regression,
Decision Tree, Random Forest) predict a derived `movement` label — whether
next-day close will be Up or Down relative to previous close.

Note that Gradient Boosting's R² lands noticeably behind Linear Regression's
on this dataset (see metrics below) — the underlying price move is close to
linear and the training set is small, so boosting's extra flexibility adds
variance rather than accuracy here. This isn't a bug; it's a realistic
illustration that a simpler model can beat a more complex one when the data
doesn't call for the extra capacity.

## Stack

- **Backend:** Python, Flask, scikit-learn, pandas — trains all 5 models
  in-memory on startup (a few seconds) and serves a REST API.
- **Frontend:** React 18 + Vite + Tailwind CSS + React Router + Axios.

## Project structure

```
ml-dashboard/
├── backend/
│   ├── app.py                 # Flask app: training + API routes
│   ├── generate_datasets.py   # Generates the stock_prices.csv dataset
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
`decision-tree`, `random-forest`, `gradient-boosting`.

### Example predict call

```bash
curl -X POST http://localhost:5000/api/logistic-regression/predict \
  -H "Content-Type: application/json" \
  -d '{"prev_close": 101.25, "open": 101.8, "high": 103.4, "low": 100.6, "volume": 245000}'
```

Response:

```json
{
  "prediction": "Up",
  "confidence": 87.1,
  "probabilities": { "Down": 12.9, "Up": 87.1 },
  "task": "classification",
  "metrics": { "accuracy": 0.825 }
}
```

## Notes on the models

- All models are trained fresh in memory every time `app.py` starts —
  there are no pickled model files to go stale. Training takes a few seconds
  for all 5 models combined.
- Regression models (Linear Regression, Gradient Boosting) return a numeric
  price-change prediction (dollars, signed) plus the model's R² / MAE on a
  held-out test split.
- Classification models (Logistic Regression, Decision Tree, Random Forest)
  return the predicted movement (`Up`/`Down`), a confidence percentage, and
  the full probability distribution across classes.
- The dataset is synthetic but realistic, generated with a fixed random seed
  (`generate_datasets.py`) so results are reproducible. Tomorrow's close is
  driven mainly by today's open-vs-previous-close move and trading volume,
  which keeps both the numeric price and its up/down direction learnable.
