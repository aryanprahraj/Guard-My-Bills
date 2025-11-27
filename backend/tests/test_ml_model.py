import pandas as pd
from backend.core.ml_model import get_fraud_scores

def test_get_fraud_scores_runs():
    # 3 dummy feature rows with 10 features (as in dummy model)
    X = pd.DataFrame({f'f{i}': [0.1, 0.2, 0.3] for i in range(10)})
    scores, probs = get_fraud_scores(X)
    assert len(scores) == 3
    assert len(probs) == 3
    assert all(isinstance(s, float) for s in scores)
    assert all(0 <= p <= 1 for p in probs)
