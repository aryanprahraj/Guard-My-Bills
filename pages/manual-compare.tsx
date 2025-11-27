import React, { useState } from 'react';
import CompareForm from '../components/CompareForm';
import { manualCompare } from '../services/api';

const ManualComparePage: React.FC = () => {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCompare = async (data: any) => {
    setLoading(true);
    setError(null);
    try {
      const res = await manualCompare(data);
      setResult(res);
    } catch (e: any) {
      setError(e.message || 'Comparison failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Manual Compare Two Transactions</h2>
      <CompareForm onCompare={handleCompare} loading={loading} />
      {error && <div className="text-red-600 mt-2">{error}</div>}
      {result && (
        <div className="mt-6 bg-white rounded shadow p-4">
          <h3 className="font-semibold mb-2">Comparison Result</h3>
          <pre className="text-sm bg-gray-100 p-2 rounded overflow-x-auto">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default ManualComparePage;
