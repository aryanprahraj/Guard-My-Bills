import os

class Config:
    MODEL_PATH = os.getenv("MODEL_PATH", "model/isolation_forest.pkl")
    N_ESTIMATORS = int(os.getenv("N_ESTIMATORS", 100))
    CONTAMINATION = float(os.getenv("CONTAMINATION", 0.01))
    MAX_SAMPLES = os.getenv("MAX_SAMPLES", "auto")
    RANDOM_STATE = int(os.getenv("RANDOM_STATE", 42))
    PDF_REPORT_PATH = os.getenv("PDF_REPORT_PATH", "reports/")
