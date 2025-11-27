import logging
from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import tempfile
import os
from ..services import report_generator
from ..services.pdf_utils import extract_transactions_from_pdf
import pandas as pd
from ..core.normalize import normalize_columns

router = APIRouter(tags=["Report"])

class ReportRequest(BaseModel):
	summary: dict
	transactions: list
	spending_analytics: dict
	charts: dict = None  # base64 images from frontend (optional)

@router.post("/generate-report")
async def generate_report(req: ReportRequest):
	try:
		with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
			report_generator.generate_pdf_report(req.summary, req.transactions, req.spending_analytics, req.charts, tmp.name)
			tmp_path = tmp.name
		return FileResponse(tmp_path, filename="guard_my_bills_report.pdf", media_type="application/pdf")
	except Exception as e:
		logging.exception(f"Failed to generate report: {e}")
		raise HTTPException(status_code=500, detail=f"Failed to generate report: {e}")

@router.post("/fraud-report")
async def fraud_report(file: UploadFile = File(...)):
    if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx') or file.filename.endswith('.pdf')):
        raise HTTPException(status_code=400, detail="File must be CSV, XLSX, or PDF")
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file.file)
        else:
            df = extract_transactions_from_pdf(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {e}")
    df = normalize_columns(df)
    # Feature engineering, ML, rules, etc. (reuse logic from /upload-statement)
    from ..core.feature_engineering import prepare_features
    from ..core.ml_model import get_fraud_scores
    from ..core.rules_engine import explain_fraud
    features_df = prepare_features(df)
    scores, probs = get_fraud_scores(features_df)
    results = []
    risk_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for i, row in features_df.iterrows():
        risk, reasons = explain_fraud(row.to_dict(), probs[i])
        risk_counts[risk] += 1
        results.append({
            **df.iloc[i].to_dict(),
            **{k: row[k] for k in features_df.columns if k not in df.columns},
            "fraud_probability": float(probs[i]),
            "anomaly_score": float(scores[i]),
            "risk_level": risk,
            "reasons": reasons
        })
    summary = {
        "total_transactions": len(df),
        "high_risk": risk_counts["HIGH"],
        "medium_risk": risk_counts["MEDIUM"],
        "low_risk": risk_counts["LOW"]
    }
    from ..services.report_generator import generate_pdf_report
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        generate_pdf_report(summary, results, {}, None, tmp.name)
        tmp_path = tmp.name
    return FileResponse(tmp_path, filename="guard_my_bills_fraud_report.pdf", media_type="application/pdf")