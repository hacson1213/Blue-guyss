# backend/train/train_model.py
import pandas as pd
import numpy as np
from app.model import Predictor
import joblib
import os

# Example script: convert historical raw rounds into training features
# You must provide `example_dataset.csv` with columns:
# round_index, color, number, timestamp, total_bet, payout, next_number

CSV = "example_dataset.csv"
if not os.path.exists(CSV):
    print("No example_dataset.csv found - please provide historical data.")
    exit(1)

df_raw = pd.read_csv(CSV)
# This script will create aggregated features per row
records = []
window = 10
for idx in range(len(df_raw)-1):
    block = df_raw.iloc[max(0, idx-window+1): idx+1]
    features = {}
    features['num_mean'] = block['number'].mean()
    features['num_std'] = block['number'].std() if len(block)>1 else 0.0
    features['last_number'] = block['number'].iloc[-1]
    for c in ['green','red','violet']:
        features[f'count_{c}'] = (block['color']==c).sum()
    last_color = block['color'].iloc[-1]
    for c in ['green','red','violet']:
        features[f'last_{c}'] = 1 if last_color==c else 0
    # include bets if present
    features['total_bet'] = float(block['total_bet'].iloc[-1]) if 'total_bet' in block else 0.0
    features['payout'] = float(block['payout'].iloc[-1]) if 'payout' in block else 0.0
    # label:
    next_number = int(df_raw['number'].iloc[idx+1])
    features['next_number'] = next_number
    records.append(features)

df_train = pd.DataFrame(records)
print("Training shape:", df_train.shape)
predictor = Predictor("model.joblib")
model = predictor.train_from_df(df_train)
print("Model trained and saved to model.joblib")
