FROM python:3.11-slim

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app/app
COPY ./model.joblib /app/model.joblib

ENV MODEL_PATH=/app/model.joblib
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
