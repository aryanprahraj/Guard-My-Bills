from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import pandas as pd
from ..core.feature_engineering import prepare_features
from ..core.ml_model import get_fraud_scores
from ..core.rules_engine import explain_fraud
from ..core.sanitize import sanitize_dict
from ..services.compare_transaction import compare_transaction

router = APIRouter(tags=["Manual Compare"])

class ManualCompareRequest(BaseModel):
	txn1: dict
	txn2: dict

@router.post("/manual-compare")
async def manual_compare(req: ManualCompareRequest):
	import traceback, logging
	try:
		# Build DataFrame
		df = pd.DataFrame([req.txn1, req.txn2])
		features_df = prepare_features(df)
		scores, probs = get_fraud_scores(features_df)
		verdicts = []
		for i, row in features_df.iterrows():
			risk, reasons = explain_fraud(row.to_dict(), probs[i])
			verdicts.append({
				"distance_km": row.get("distance_from_last_txn_km"),
				"time_delta_minutes": row.get("time_since_last_txn_minutes"),
				"velocity_kmh": row.get("velocity_kmh"),
				"anomaly_score": float(scores[i]),
				"fraud_probability": float(probs[i]),
				"risk_level": risk,
				"explanation_labels": reasons
			})
		# Verdict logic
		if any(v["risk_level"] == "HIGH" for v in verdicts):
			fraud_verdict = "likely fraud"
		elif any(v["risk_level"] == "MEDIUM" for v in verdicts):
			fraud_verdict = "possible"
		else:
			fraud_verdict = "unlikely"
		return sanitize_dict({
			"comparison": verdicts,
			"fraud_verdict": fraud_verdict
		})
	except Exception as e:
		logging.error("Exception in /manual-compare: %s\n%s", str(e), traceback.format_exc())
		return JSONResponse(status_code=500, content={"error": str(e), "trace": traceback.format_exc()})

class CheckTransactionRequest(BaseModel):
    suspect_transaction: dict
    reference_transactions: list

@router.post("/check-transaction")
async def check_transaction(req: CheckTransactionRequest):
    # Validate input
    if len(req.reference_transactions) != 2:
        raise HTTPException(status_code=400, detail="Must provide exactly 2 reference transactions.")
    suspect_date = req.suspect_transaction.get('date', '')[:10]
    for ref in req.reference_transactions:
        if ref.get('date', '')[:10] != suspect_date:
            raise HTTPException(status_code=400, detail="Reference transactions must be from the same day as suspect.")
    result = compare_transaction(req.suspect_transaction, req.reference_transactions)
    return sanitize_dict(result)