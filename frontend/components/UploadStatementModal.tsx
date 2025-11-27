import React, { useState } from 'react';
import Modal from './Modal';
import FileUpload from './FileUpload';
import FraudSummaryCard from './FraudSummaryCard';
import { uploadStatement, downloadFraudReport } from '../services/api';


interface FraudSummary {
  total_transactions: number;
  high_risk: number;
  medium_risk: number;
  low_risk: number;
}

const UploadStatementModal: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  onViewResults: () => void;
}> = ({ isOpen, onClose, onViewResults }) => {
  const [summary, setSummary] = useState<FraudSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (file: File) => {
    setLoading(true);
    setError(null);
    setFile(file);
    try {
      const data = await uploadStatement(file);
      setSummary(data.summary);
    } catch (e: any) {
      setError('Failed to analyze statement. Please try again.');
    }
    setLoading(false);
  };

  const handleDownloadReport = async () => {
    if (file) await downloadFraudReport(file);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Upload Bank Statement for Fraud Analysis">
      <FileUpload onUpload={handleUpload} />
      {loading && <div className="mt-4 text-center text-blue-600">Analyzing...</div>}
      {error && <div className="mt-4 text-center text-red-600">{error}</div>}
      {summary && (
        <div className="mt-6">
          <FraudSummaryCard summary={summary} />
          <div className="mt-4 flex flex-col items-center gap-2">
            <button onClick={handleDownloadReport} className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded shadow">Download Fraud Report (PDF)</button>
          </div>
        </div>
      )}
    </Modal>
  );
};

export default UploadStatementModal;
