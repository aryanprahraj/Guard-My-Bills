import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from ..config import Config

MODEL_PATH = Config.MODEL_PATH

class FraudModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.pipeline = None
        self.feature_cols = None
        self.is_trained = False
        self.load_model()

    def load_model(self):
        model_dir = os.path.dirname(MODEL_PATH)
        if model_dir and not os.path.exists(model_dir):
            os.makedirs(model_dir, exist_ok=True)
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                self.pipeline, self.feature_cols = pickle.load(f)
                self.is_trained = True
        else:
            self.pipeline = None
            self.feature_cols = None
            self.is_trained = False

    def train(self, features: pd.DataFrame):
        X = features.select_dtypes(include=[float, int, bool]).fillna(0)
        self.feature_cols = list(X.columns)
        scaler = StandardScaler()
        clf = IsolationForest(n_estimators=Config.N_ESTIMATORS, contamination=Config.CONTAMINATION, max_samples=Config.MAX_SAMPLES, random_state=Config.RANDOM_STATE)
        pipeline = Pipeline([
            ('scaler', scaler),
            ('clf', clf)
        ])
        pipeline.fit(X)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump((pipeline, self.feature_cols), f)
        self.pipeline = pipeline
        self.is_trained = True
        
    def predict_anomaly_scores(self, X: pd.DataFrame):
        # If not trained, or feature columns do not match, retrain on this data
        X_numeric = X.select_dtypes(include=[float, int, bool]).fillna(0)
        if (not self.is_trained) or (self.feature_cols is None) or (set(self.feature_cols) != set(X_numeric.columns)):
            self.train(X)
        X_model = X[self.feature_cols] if self.feature_cols else X
        scores = -self.pipeline.decision_function(X_model)
        # Normalize to [0,1] for fraud probability
        prob = (scores - scores.min()) / (scores.max() - scores.min() + 1e-6)
        return scores, prob

fraud_model = FraudModel()

def get_fraud_scores(features_df: pd.DataFrame):
    scores, prob = fraud_model.predict_anomaly_scores(features_df)
    return scores, prob
