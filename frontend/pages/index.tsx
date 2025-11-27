

import Link from 'next/link';
import { useState } from 'react';
import UploadStatementModal from '../components/UploadStatementModal';
import FraudComparisonModal from '../components/FraudComparisonModal';


const Home: React.FC = () => {
  const [showUpload, setShowUpload] = useState(false);
  const [showCompare, setShowCompare] = useState(false);
  const handleViewResults = () => { window.location.href = '/results'; };
  return (
  <div className="min-h-screen flex flex-col justify-between bg-[#f5f8fb]">
    {/* Header - visually prominent, lower, larger */}
    <div className="mt-24 flex flex-col items-center justify-center text-center">
      <div className="flex items-center justify-center">
        <span className="inline-block w-24 h-24">
          <svg width="96" height="96" viewBox="0 0 40 40" fill="none" className="w-24 h-24"><rect width="40" height="40" rx="8" fill="#2563eb"/><path d="M20 10l10 4v5c0 7-4.5 11.5-10 13-5.5-1.5-10-6-10-13v-5l10-4z" fill="#fff"/><path d="M16.5 21.5l3 3 5-5" stroke="#22c55e" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
        </span>
      </div>
      <span className="text-4xl font-semibold mt-4">Guard My Bills</span>
      <div className="text-lg text-gray-500 mt-1">Your Financial Guardian</div>
    </div>

    {/* Main Cards */}
    <main className="flex flex-col items-center flex-1 justify-center w-full">
      <div className="mt-16">
        <div className="mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 place-items-center max-w-4xl justify-center">
        {/* Upload Card */}
        <div className="w-80 h-full bg-white shadow-lg rounded-2xl p-6 flex flex-col items-center justify-between hover:shadow-xl transition cursor-pointer" onClick={() => setShowUpload(true)}>
          <div className="flex flex-col items-center">
            <div className="mb-4">
              <svg width="48" height="48" fill="none"><rect width="48" height="48" rx="12" fill="#e0e7ef"/><path d="M24 32v-8m0 0l-4 4m4-4l4 4" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><rect x="16" y="36" width="16" height="2" rx="1" fill="#2563eb"/></svg>
            </div>
            <div className="font-semibold text-lg mb-2 text-center">Upload Bank Statement for Fraud Analysis</div>
          </div>
          <div className="mt-4 w-full flex justify-center">
            <button className="w-32 text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded shadow">Choose File</button>
          </div>
        </div>
        {/* Manual Compare Card */}
        <div className="w-80 h-full bg-white shadow-lg rounded-2xl p-6 flex flex-col items-center justify-between hover:shadow-xl transition cursor-pointer" onClick={() => setShowCompare(true)}>
          <div className="flex flex-col items-center">
            <div className="mb-4">
              <svg width="48" height="48" fill="none"><rect width="48" height="48" rx="12" fill="#e0e7ef"/><path d="M16 32h16M24 16v16" stroke="#2563eb" strokeWidth="2" strokeLinecap="round"/><rect x="20" y="20" width="8" height="8" rx="2" fill="#22c55e"/></svg>
            </div>
            <div className="font-semibold text-lg mb-2 text-center">Check if a Transaction is Fraud</div>
          </div>
          <div className="mt-4 w-full flex justify-center">
            <button className="w-32 text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded shadow">Check Fraud</button>
          </div>
        </div>
        {/* Analyse My Spending card removed */}
      </div>
      {/* Optionally, add a summary or info here if needed */}
      </div>
    </main>

    <footer className="py-6 text-center text-sm text-gray-500">© 2025 Guard My Bills</footer>

    {/* Modals */}
    <UploadStatementModal isOpen={showUpload} onClose={() => setShowUpload(false)} onViewResults={handleViewResults} />
    <FraudComparisonModal isOpen={showCompare} onClose={() => setShowCompare(false)} />

  </div>
  );
};

export default Home;
