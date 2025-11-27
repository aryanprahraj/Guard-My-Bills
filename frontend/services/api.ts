

// Define TypeScript interfaces matching backend Pydantic models
export interface Transaction {
  date: string;
  time: string;
  amount: number;
  merchant_name: string;
  merchant_category: string;
  city: string;
  state: string;
  country: string;
  channel?: string;
}

export interface TransactionFeatures {
  timestamp: string;
  hour_of_day: number;
  day_of_week: number;
  is_weekend: boolean;
  time_since_last_txn_minutes?: number;
  distance_from_last_txn_km?: number;
  velocity_kmh?: number;
  amount_zscore?: number;
  amount_to_user_avg_ratio?: number;
  is_new_merchant: boolean;
  is_new_city: boolean;
  transactions_last_10min: number;
  transactions_last_60min: number;
  sum_amount_last_60min: number;
  merchant_category_encoded?: number;
  is_night_time: boolean;
}

export interface FraudResult {
  risk_level: string;
  fraud_probability: number;
  anomaly_score: number;
  reasons: string[];
}

export interface StatementAnalysisResult {
  summary: Record<string, any>;
  transactions: Record<string, any>[];
  spending_analytics: Record<string, any>;
}

export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://guard-my-bills.onrender.com';
export async function checkFraud(payload: any) {
  // Convert modal payload to backend expected format
  const req = {
    txn1: payload.suspect,
    txn2: { ...payload.ref1, ...payload.ref2 } // fallback, but backend expects two txns, so send only ref1 for now
  };
  // If you want to compare all three, use /check-transaction endpoint instead
  console.log("Sending payload:", req, "to", `${API_BASE}/manual-compare`);
  try {
    const res = await fetch(`${API_BASE}/manual-compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req),
    });
    if (!res.ok) {
      let errMsg = 'API error';
      try {
        const err = await res.json();
        errMsg = err.detail || JSON.stringify(err);
      } catch {}
      throw new Error(errMsg);
    }
    return await res.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
}


export async function uploadStatement(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  // Timeout logic
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000); // 15s timeout
  let res;
  try {
    res = await fetch(`${API_BASE}/upload-statement`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    });
  } catch (err) {
    clearTimeout(timeout);
    if (err.name === 'AbortError') {
      throw new Error('Request timed out. Backend may be unreachable.');
    }
    throw new Error('Network error: ' + err.message);
  }
  clearTimeout(timeout);
  if (!res.ok) {
    let errorText = await res.text();
    let errorJson;
    try {
      errorJson = JSON.parse(errorText);
    } catch {}
    if (errorJson && errorJson.detail) {
      throw new Error('API error: ' + errorJson.detail + (errorJson.trace ? `\nTrace: ${errorJson.trace}` : ''));
    }
    throw new Error('Upload failed: ' + errorText);
  }
  try {
    return await res.json();
  } catch (e) {
    throw new Error('Invalid JSON response from backend.');
  }
}

export async function manualCompare(data: any) {
  const res = await fetch(`${API_BASE}/manual-compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Manual compare failed');
  return await res.json();
}

export async function downloadReport(data: any) {
  const res = await fetch(`${API_BASE}/generate-report`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Report generation failed');
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'guard_my_bills_report.pdf');
  document.body.appendChild(link);
  link.click();
  link.parentNode?.removeChild(link);
}

export async function downloadFraudReport(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/fraud-report`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Fraud report download failed');
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'guard_my_bills_fraud_report.pdf');
  document.body.appendChild(link);
  link.click();
  link.parentNode?.removeChild(link);
}

export async function checkTransaction(data: any) {
  const res = await fetch(`${API_BASE}/check-transaction`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Check transaction failed');
  return await res.json();
}

export async function spendingAnalysis(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/spending-analysis`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Spending analysis failed');
  return await res.json();
}

export async function downloadSpendingReport(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/spending-report`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Spending report download failed');
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'guard_my_bills_spending_report.pdf');
  document.body.appendChild(link);
  link.click();
  link.parentNode?.removeChild(link);
}
