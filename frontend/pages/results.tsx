
import React, { useState } from 'react';
import TransactionsTable from '../components/TransactionsTable';
import RiskTimelineChart from '../components/RiskTimelineChart';
import SpendingPieChart from '../components/SpendingPieChart';
import MerchantBarChart from '../components/MerchantBarChart';
import FraudSummaryCard from '../components/FraudSummaryCard';

interface AnalysisResult {
  summary?: {
    total_transactions: number;
    high_risk: number;
    medium_risk: number;
    low_risk: number;
  };
  flaggedTransactions?: any[];
  insights?: any;
  transactions?: any[];
  spending_analytics?: any;
}


const ResultsPage: React.FC = () => {
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);

  // Safe defaults for demo
  const summary = analysis?.summary ?? {
    total_transactions: 0,
    high_risk: 0,
    medium_risk: 0,
    low_risk: 0,
  };
  const transactions = analysis?.transactions ?? [];
  const spending_analytics = analysis?.spending_analytics ?? {};

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>
      {!analysis && <div className="text-gray-500">No analysis loaded. Please upload a statement first.</div>}
      {analysis && (
        <>
          <div className="my-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            <FraudSummaryCard summary={summary} />
            <RiskTimelineChart transactions={transactions} />
            <SpendingPieChart analytics={spending_analytics} />
          </div>
          <div className="my-6">
            <MerchantBarChart analytics={spending_analytics} />
          </div>
          <div className="my-6">
            <TransactionsTable transactions={transactions} />
          </div>
        </>
      )}
    </div>
  );
};

export default ResultsPage;
