import React, { useState } from 'react';
import FileUpload from '../components/FileUpload';
import FraudSummaryCard from '../components/FraudSummaryCard';
import RiskTimelineChart from '../components/RiskTimelineChart';
import SpendingPieChart from '../components/SpendingPieChart';
import MerchantBarChart from '../components/MerchantBarChart';
import TransactionsTable from '../components/TransactionsTable';
import { uploadStatement, downloadReport } from '../services/api';

const UploadPage: React.FC = () => {
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState(false);

  const handleFileUpload = async (file: File) => {
    setLoading(true);
    setError(null);
    try {
      const result = await uploadStatement(file);
      setAnalysis(result);
    } catch (e: any) {
      setError(e.message || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!analysis) return;
    setDownloading(true);
    try {
      await downloadReport(analysis);
    } catch (e: any) {
      setError('Failed to download report');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Upload Statement</h2>
      <FileUpload onUpload={handleFileUpload} loading={loading} />
      {error && <div className="text-red-600 mt-2">{error}</div>}
      {analysis && (
        <>
          <div className="my-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            <FraudSummaryCard summary={analysis.summary} />
            <RiskTimelineChart transactions={analysis.transactions} />
            <SpendingPieChart analytics={analysis.spending_analytics} />
          </div>
          <div className="my-6">
            <MerchantBarChart analytics={analysis.spending_analytics} />
          </div>
          <div className="my-6">
            <TransactionsTable transactions={analysis.transactions} />
          </div>
          <button
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded shadow mt-4"
            onClick={handleDownloadReport}
            disabled={downloading}
          >
            {downloading ? 'Downloading...' : 'Download Fraud Report (PDF)'}
          </button>
        </>
      )}
    </div>
  );
};

export default UploadPage;
