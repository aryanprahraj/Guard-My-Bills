import React, { useState } from 'react';

interface CompareFormProps {
  onCompare: (data: any) => void;
  loading?: boolean;
}

const initialTxn = {
  date: '',
  time: '',
  amount: '',
  merchant_name: '',
  merchant_category: '',
  city: '',
  state: '',
  country: '',
};

const CompareForm: React.FC<CompareFormProps> = ({ onCompare, loading }) => {
  const [txn1, setTxn1] = useState({ ...initialTxn });
  const [txn2, setTxn2] = useState({ ...initialTxn });

  const handleChange = (idx: 1 | 2, field: string, value: string) => {
    if (idx === 1) setTxn1({ ...txn1, [field]: value });
    else setTxn2({ ...txn2, [field]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCompare({ txn1, txn2 });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded shadow p-4 flex flex-col gap-4">
      <div className="font-semibold mb-2">Transaction 1</div>
      <div className="grid grid-cols-2 gap-2">
        <input className="input" placeholder="Date (YYYY-MM-DD)" value={txn1.date} onChange={e => handleChange(1, 'date', e.target.value)} required />
        <input className="input" placeholder="Time (HH:MM:SS)" value={txn1.time} onChange={e => handleChange(1, 'time', e.target.value)} required />
        <input className="input" placeholder="Amount" type="number" value={txn1.amount} onChange={e => handleChange(1, 'amount', e.target.value)} required />
        <input className="input" placeholder="Merchant Name" value={txn1.merchant_name} onChange={e => handleChange(1, 'merchant_name', e.target.value)} required />
        <input className="input" placeholder="Category" value={txn1.merchant_category} onChange={e => handleChange(1, 'merchant_category', e.target.value)} required />
        <input className="input" placeholder="City" value={txn1.city} onChange={e => handleChange(1, 'city', e.target.value)} required />
        <input className="input" placeholder="State" value={txn1.state} onChange={e => handleChange(1, 'state', e.target.value)} />
        <input className="input" placeholder="Country" value={txn1.country} onChange={e => handleChange(1, 'country', e.target.value)} required />
      </div>
      <div className="font-semibold mb-2 mt-4">Transaction 2</div>
      <div className="grid grid-cols-2 gap-2">
        <input className="input" placeholder="Date (YYYY-MM-DD)" value={txn2.date} onChange={e => handleChange(2, 'date', e.target.value)} required />
        <input className="input" placeholder="Time (HH:MM:SS)" value={txn2.time} onChange={e => handleChange(2, 'time', e.target.value)} required />
        <input className="input" placeholder="Amount" type="number" value={txn2.amount} onChange={e => handleChange(2, 'amount', e.target.value)} required />
        <input className="input" placeholder="Merchant Name" value={txn2.merchant_name} onChange={e => handleChange(2, 'merchant_name', e.target.value)} required />
        <input className="input" placeholder="Category" value={txn2.merchant_category} onChange={e => handleChange(2, 'merchant_category', e.target.value)} required />
        <input className="input" placeholder="City" value={txn2.city} onChange={e => handleChange(2, 'city', e.target.value)} required />
        <input className="input" placeholder="State" value={txn2.state} onChange={e => handleChange(2, 'state', e.target.value)} />
        <input className="input" placeholder="Country" value={txn2.country} onChange={e => handleChange(2, 'country', e.target.value)} required />
      </div>
      <button
        type="submit"
        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded shadow mt-4"
        disabled={loading}
      >
        {loading ? 'Comparing...' : 'Compare Transactions'}
      </button>
    </form>
  );
};

export default CompareForm;
