import React from 'react';

interface FraudSummaryCardProps {
  summary: {
    total_transactions: number;
    high_risk: number;
    medium_risk: number;
    low_risk: number;
  };
}

const FraudSummaryCard: React.FC<FraudSummaryCardProps> = ({ summary }) => {
  if (!summary) return null;
  return (
    <div className="bg-white rounded shadow p-4 flex flex-col items-center">
      <div className="text-lg font-semibold mb-2">Fraud Summary</div>
      <div className="flex gap-4 mb-2">
        <div className="flex flex-col items-center">
          <span className="text-red-600 font-bold text-xl">{summary.high_risk}</span>
          <span className="text-xs text-gray-500">High Risk</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-yellow-500 font-bold text-xl">{summary.medium_risk}</span>
          <span className="text-xs text-gray-500">Medium Risk</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-green-600 font-bold text-xl">{summary.low_risk}</span>
          <span className="text-xs text-gray-500">Low Risk</span>
        </div>
      </div>
      <div className="text-xs text-gray-700">Total analyzed: {summary.total_transactions}</div>
    </div>
  );
};

export default FraudSummaryCard;
