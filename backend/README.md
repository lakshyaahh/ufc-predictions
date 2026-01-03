# UFC Predictions Backend

This directory contains a FastAPI backend that loads a trained model and exposes endpoints:

- `POST /predict` - send JSON with `fights` list (each item is a dict of features) → returns predictions
- `POST /upload` - upload a CSV file of fights → parses CSV, predicts, stores in SQLite
- `GET /results` - returns stored predictions
- `GET /health` - returns status and whether model is loaded

Place your trained model at `backend/models/ufc_prediction_model.pkl` before starting.

## Quick Start

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
Interactive API docs: `http://localhost:8000/docs`
