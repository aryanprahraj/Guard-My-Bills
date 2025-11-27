import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from typing import List
from ..core.feature_engineering import prepare_features
from ..core.ml_model import get_fraud_scores
from ..core.rules_engine import explain_fraud
from ..models.transaction import Transaction
from ..models.transaction_features import TransactionFeatures
from ..models.fraud_result import FraudResult
from ..models.statement_analysis_result import StatementAnalysisResult
from ..core.sanitize import sanitize_dict
from ..services.pdf_utils import extract_transactions_from_pdf
from ..core.normalize import normalize_columns

router = APIRouter(tags=["Fraud Detection"])

@router.post("/upload-statement", response_model=StatementAnalysisResult)
async def upload_statement(file: UploadFile = File(...)):
	try:
		if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx') or file.filename.endswith('.pdf')):
			raise HTTPException(status_code=400, detail="File must be CSV, XLSX, or PDF")
		# Parse file
		if file.filename.endswith('.csv'):
			df = pd.read_csv(file.file)
		elif file.filename.endswith('.xlsx'):
			df = pd.read_excel(file.file)
		else:
			df = extract_transactions_from_pdf(file.file)
		if df is None or (hasattr(df, 'empty') and df.empty):
			raise HTTPException(status_code=400, detail="No transactions found")
		# Debug: print columns and head
		import sys
		print("[DEBUG] Columns after parsing:", df.columns.tolist(), file=sys.stderr)
		print("[DEBUG] First 5 rows after parsing:\n", df.head().to_string(), file=sys.stderr)
		df = normalize_columns(df)
		print("[DEBUG] Columns after normalization:", df.columns.tolist(), file=sys.stderr)
		print("[DEBUG] First 5 rows after normalization:\n", df.head().to_string(), file=sys.stderr)
		# Feature engineering, ML, rules
		features_df = prepare_features(df)
		scores, probs = get_fraud_scores(features_df)
		results = []
		for i, row in features_df.iterrows():
			risk, reasons = explain_fraud(row.to_dict(), probs[i])
			results.append({
				**df.iloc[i].to_dict(),
				**{k: row[k] for k in features_df.columns if k not in df.columns},
				"fraud_probability": float(probs[i]),
				"anomaly_score": float(scores[i]),
				"risk_level": risk,
				"reasons": reasons
			})
		risk_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
		for r in results:
			risk_counts[r["risk_level"]] += 1
		summary = {
			"total_transactions": len(df),
			"high_risk": risk_counts["HIGH"],
			"medium_risk": risk_counts["MEDIUM"],
			"low_risk": risk_counts["LOW"]
		}
		return sanitize_dict({
			"transactions": results,
			"summary": summary
		})
	except Exception as e:
		import sys
		import traceback
		print("\n\n--- Exception in upload_statement ---", file=sys.stderr)
		print(e, file=sys.stderr)
		print(traceback.format_exc(), file=sys.stderr)
		logging.error(f"Failed to analyze statement: {e}")
		logging.error(traceback.format_exc())
		return JSONResponse(status_code=400, content={"detail": f"Failed to analyze statement: {e}", "trace": traceback.format_exc()})