import React, { useState } from 'react';
import Modal from './Modal';

const FraudResultCard: React.FC<{
  result: {
    distance_km: number;
    time_diff_min: number;
    velocity_kmh: number;
    anomaly_score: number;
    fraud_probability: number;
    risk_level: string;
    explanations: string[];
  };
}> = ({ result }) => (
  <div className="bg-white rounded shadow p-4 flex flex-col items-center mt-4">
    <div className="text-lg font-semibold mb-2">Fraud Check Result</div>
    <div className="grid grid-cols-2 gap-4 w-full max-w-xs">
      <div><span className="font-bold">Distance:</span> {result.distance_km} km</div>
      <div><span className="font-bold">Time Diff:</span> {result.time_diff_min} min</div>
      <div><span className="font-bold">Velocity:</span> {result.velocity_kmh} km/h</div>
      <div><span className="font-bold">Anomaly Score:</span> {result.anomaly_score}</div>
      <div><span className="font-bold">Fraud Probability:</span> {(result.fraud_probability * 100).toFixed(1)}%</div>
      <div><span className="font-bold">Risk Level:</span> <span className={`font-bold ${result.risk_level === 'High' ? 'text-red-600' : result.risk_level === 'Medium' ? 'text-yellow-500' : 'text-green-600'}`}>{result.risk_level}</span></div>
    </div>
    <div className="mt-2 text-xs text-gray-600 text-center">
      {result.explanations.map((e, i) => <div key={i}>• {e}</div>)}
    </div>
  </div>
);

export default FraudResultCard;
