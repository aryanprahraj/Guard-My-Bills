import React from 'react';

interface Transaction {
  date: string;
  time: string;
  merchant_name: string;
  amount: number;
  city: string;
  fraud_probability: number;
  risk_level: string;
  reasons?: string[];
}

interface TransactionsTableProps {
  transactions: Transaction[];
}

const riskColors: Record<string, string> = {
  HIGH: 'bg-red-500',
  MEDIUM: 'bg-yellow-400',
  LOW: 'bg-green-500',
};

const TransactionsTable: React.FC<TransactionsTableProps> = ({ transactions }) => {
  if (!transactions || transactions.length === 0) {
    return <div className="text-gray-500">No transactions to display.</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white rounded shadow">
        <thead>
          <tr>
            <th className="px-4 py-2">Date</th>
            <th className="px-4 py-2">Time</th>
            <th className="px-4 py-2">Merchant</th>
            <th className="px-4 py-2">Amount</th>
            <th className="px-4 py-2">City</th>
            <th className="px-4 py-2">Fraud Probability</th>
            <th className="px-4 py-2">Risk</th>
            <th className="px-4 py-2">Explanations</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((txn, idx) => (
            <tr key={idx} className="border-t">
              <td className="px-4 py-2">{txn.date}</td>
              <td className="px-4 py-2">{txn.time}</td>
              <td className="px-4 py-2">{txn.merchant_name}</td>
              <td className="px-4 py-2">{txn.amount}</td>
              <td className="px-4 py-2">{txn.city}</td>
              <td className="px-4 py-2">{(txn.fraud_probability * 100).toFixed(1)}%</td>
              <td className="px-4 py-2">
                <span className={`text-white px-2 py-1 rounded ${riskColors[txn.risk_level] || 'bg-gray-400'}`}>{txn.risk_level}</span>
              </td>
              <td className="px-4 py-2">
                {txn.reasons && txn.reasons.length > 0 ? (
                  <div className="flex flex-wrap gap-1">
                    {txn.reasons.map((reason, i) => (
                      <span key={i} className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs">{reason}</span>
                    ))}
                  </div>
                ) : (
                  <span className="text-gray-400">-</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TransactionsTable;
