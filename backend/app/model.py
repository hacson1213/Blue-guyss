# backend/app/model.py
import joblib
import numpy as np
import pandas as pd
from typing import List, Dict
import os

MODEL_DEFAULT = "model.joblib"

class Predictor:
    def __init__(self, model_path: str = MODEL_DEFAULT):
        self.model_path = model_path
        self.model = None
        if os.path.exists(self.model_path):
            self.load()
        else:
            self._init_dummy()

    def _init_dummy(self):
        # fallback "dumb" predictor if no model exists
        self.model = None

    def load(self):
        self.model = joblib.load(self.model_path)

    def save(self, model):
        joblib.dump(model, self.model_path)
        self.model = model

    def featurize(self, rounds: List[Dict], extra: Dict = None):
        """
        Convert rounds[] into numeric features for model.
        rounds: list of dicts {index,color,number,timestamp}
        We'll extract:
          - last N numbers
          - counts of colors in last N
          - mean, std of numbers
          - last number
          - last color (encoded)
          - total_bet / payout as features if present
        """
        df = pd.DataFrame(rounds)
        N = 10
        recent = df.tail(N)
        features = {}
        # number stats
        nums = recent['number'].astype(float).fillna(0)
        features['num_mean'] = nums.mean()
        features['num_std'] = nums.std() if len(nums)>1 else 0.0
        # last number
        features['last_number'] = nums.iloc[-1] if len(nums)>0 else 0
        # color counts
        colors = ['green','red','violet']
        for c in colors:
            features[f'count_{c}'] = (recent['color']==c).sum()
        # last color one-hot
        last_color = recent['color'].iloc[-1] if len(recent)>0 else None
        for c in colors:
            features[f'last_{c}'] = 1 if last_color==c else 0
        # optional extra
        if extra:
            features['total_bet'] = float(extra.get('total_bet') or 0.0)
            features['payout'] = float(extra.get('payout') or 0.0)
            features['net'] = features['total_bet'] - features['payout']
        else:
            features['total_bet'] = 0.0
            features['payout'] = 0.0
            features['net'] = 0.0
        return pd.DataFrame([features])

    def predict_next(self, rounds: List[Dict], extra: Dict = None):
        """
        Returns predicted label and confidence.
        We'll predict both color and number using a single model here for simplicity:
         - model predicts next number (0-9) and we map to color heuristics
        This can be expanded to 2 models (color and number).
        """
        if not self.model:
            # dummy behaviour: return last color and (last_number+1)%10
            last = rounds[-1] if rounds else {'color':'green','number':0}
            pred = {"color": last['color'], "number": (last['number']+1) % 10}
            return pred, 0.5

        X = self.featurize(rounds, extra)
        pred_number = int(self.model.predict(X)[0])
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X)
            # choose highest class prob
            conf = float(np.max(probs))
        else:
            conf = 0.7
        # map number to color heuristic (example)
        color_map = {0:'green',1:'red',2:'violet',3:'green',4:'red',5:'violet',6:'green',7:'red',8:'violet',9:'green'}
        return {"color": color_map.get(pred_number, "green"), "number": pred_number}, conf

    def train_from_df(self, df: pd.DataFrame):
        """
        df must include columns: features encoded or raw history and label 'next_number'
        For simplicity assume df contains crafted features (from train script).
        """
        from lightgbm import LGBMClassifier
        X = df.drop(columns=['next_number'])
        y = df['next_number'].astype(int)
        model = LGBMClassifier(n_estimators=200, learning_rate=0.05)
        model.fit(X, y)
        self.save(model)
        return model

    def train_from_json(self, json_list):
        import pandas as pd
        df = pd.DataFrame(json_list)
        # assume json already has features and next_number
        return self.train_from_df(df)
