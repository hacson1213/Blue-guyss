# Blue Guyss Backend

## Run locally
1. Create a virtualenv and install deps:
2. python -m venv .venv source .venv/bin/
activate pip install -r requirements.txt
3. Place `model.joblib` in the backend folder (or run `train/train_model.py` with `example_dataset.csv`).
4. Start server:
5. uvicorn app.main:app --reload --host 0.0.0.0
--port 8000
6. 4. Test:
   5. curl -X POST "http://127.0.0.1:8000/predict"-H
"Content-Type: application/json" -d`""rounds"
[("index":1,"color":"green","number":2),
("index":2,"color":"red","number":5;],
total_bet":1000, "payout":200}'
## Deploy to Render / Railway
- Create service and point to repo. Use Dockerfile or Python environment.
- Expose port 8000.
- Set MODEL_PATH if custom.
