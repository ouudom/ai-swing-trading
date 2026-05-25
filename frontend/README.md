# Trading Brain Frontend

Local-only candlestick viewer for XAUUSD. Reads CSVs in `data/twelvedata/xauusd/` via FastAPI backend.

## Run

### Backend (port 8000)
```bash
cd ..
pip install -r requirements.txt
.venv/bin/uvicorn backend.main:app --reload --port 8000
```

### Frontend (port 5173)
```bash
npm install
npm run dev
```

Open http://localhost:5173. Vite proxies `/api/*` → backend.

## Data refresh
Run `python scripts/weekly_pull.py` to fetch fresh bars from Twelve Data. Backend reads CSVs with 60s in-memory cache.

## Endpoints
- `GET /api/candles?tf={15m|1h|4h|1d}&limit=N`
- `GET /api/health`
