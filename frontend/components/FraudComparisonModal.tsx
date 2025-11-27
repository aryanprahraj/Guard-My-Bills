      import React, { useState } from 'react';
        import Modal from './Modal';
        import { checkTransaction } from '../services/api';

        interface Txn {
          date: string;
          time: string;
          amount: string;
          city: string;
          country: string;
          merchant: string;
          category: string;
          [key: string]: string;
        }

        type Props = {
          isOpen: boolean;
          onClose: () => void;
        };


        const FraudComparisonModal: React.FC<Props> = ({ isOpen, onClose }) => {
          if (!isOpen) return null;

          const [form, setForm] = useState<{
            suspect: Txn;
            ref1: Txn;
            ref2: Txn;
          }>({
            suspect: { date: '', time: '', amount: '', city: '', country: '', merchant: '', category: '' },
            ref1: { date: '', time: '', amount: '', city: '', country: '', merchant: '', category: '' },
            ref2: { date: '', time: '', amount: '', city: '', country: '', merchant: '', category: '' },
          });
          const [loading, setLoading] = useState(false);
          const [result, setResult] = useState<any>(null);
          const [error, setError] = useState<string | null>(null);

          const handleChange = (section: 'suspect' | 'ref1' | 'ref2', field: string, value: string) => {
            setForm(prev => ({ ...prev, [section]: { ...prev[section], [field]: value } }));
          };

          const handleSubmit = async (e: React.FormEvent) => {
            e.preventDefault();
            setLoading(true);
            setError(null);
            setResult(null);
            // Validate all required fields
            for (const section of ['suspect', 'ref1', 'ref2'] as const) {
              for (const field of ['date', 'time', 'amount', 'city', 'country', 'merchant']) {
                if (!form[section][field]) {
                  setError('Please fill all required fields.');
                  setLoading(false);
                  return;
                }
              }
            }
            // Validate all dates are the same
            const d = form.suspect.date;
            if (form.ref1.date !== d || form.ref2.date !== d) {
              setError('All transactions must be from the same day.');
              setLoading(false);
              return;
            }
            try {
              const payload = {
                suspect_transaction: {
                  ...form.suspect,
                  date: form.suspect.date + 'T' + form.suspect.time,
                },
                reference_transactions: [
                  {
                    ...form.ref1,
                    date: form.ref1.date + 'T' + form.ref1.time,
                  },
                  {
                    ...form.ref2,
                    date: form.ref2.date + 'T' + form.ref2.time,
                  }
                ]
              };
              console.log("sending request", payload);
              const res = await checkTransaction(payload);
              setResult(res);
            } catch (err: any) {
              if (err?.response && err.response.data) {
                setError(err.response.data.detail || JSON.stringify(err.response.data));
              } else {
                setError(err?.message || 'Failed to check transaction.');
              }
            } finally {
              setLoading(false);
            }
          };

          return (
            <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-60 z-50">
              <div className="w-[95%] max-w-[1500px] mx-auto bg-white rounded-lg p-6 overflow-visible">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-bold text-gray-800">Check if a Transaction is Fraud</h2>
                  <button type="button" onClick={onClose} className="text-2xl text-gray-400 hover:text-gray-700 ml-4" aria-label="Close">❌</button>
                </div>
                {/* Form */}
                <form onSubmit={handleSubmit}>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
                    {/* Transaction to Check */}
                    <div className="border rounded-xl p-4 bg-white">
                      <div className="font-bold text-lg mb-4 text-blue-700">Transaction to Check</div>
                      <label className="text-sm font-medium mb-1 block">Date<span className="text-red-500">*</span>
                        <input type="date" className="input w-full border px-2 py-1 rounded mt-1" value={form.suspect.date} onChange={e => handleChange('suspect', 'date', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Time<span className="text-red-500">*</span>
                        <input type="time" className="input w-full border px-2 py-1 rounded mt-1" value={form.suspect.time} onChange={e => handleChange('suspect', 'time', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Amount<span className="text-red-500">*</span>
                        <input type="number" className="input w-full border px-2 py-1 rounded mt-1" value={form.suspect.amount} onChange={e => handleChange('suspect', 'amount', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">City<span className="text-red-500">*</span>
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.suspect.city} onChange={e => handleChange('suspect', 'city', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Country<span className="text-red-500">*</span>
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.suspect.country} onChange={e => handleChange('suspect', 'country', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Merchant<span className="text-red-500">*</span>
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.suspect.merchant} onChange={e => handleChange('suspect', 'merchant', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Category
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.suspect.category} onChange={e => handleChange('suspect', 'category', e.target.value)} />
                      </label>
                    </div>
                    {/* Reference Transaction 1 */}
                    <div className="border rounded-xl p-4 bg-white">
                      <div className="font-bold text-lg mb-4 text-green-700">Reference Transaction 1</div>
                      <label className="text-sm font-medium mb-1 block">Date<span className="text-red-500">*</span>
                        <input type="date" className="input w-full border px-2 py-1 rounded mt-1" value={form.ref1.date} onChange={e => handleChange('ref1', 'date', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Time<span className="text-red-500">*</span>
                        <input type="time" className="input w-full border px-2 py-1 rounded mt-1" value={form.ref1.time} onChange={e => handleChange('ref1', 'time', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Amount<span className="text-red-500">*</span>
                        <input type="number" className="input w-full border px-2 py-1 rounded mt-1" value={form.ref1.amount} onChange={e => handleChange('ref1', 'amount', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">City<span className="text-red-500">*</span>
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.ref1.city} onChange={e => handleChange('ref1', 'city', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Country<span className="text-red-500">*</span>
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.ref1.country} onChange={e => handleChange('ref1', 'country', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Merchant<span className="text-red-500">*</span>
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.ref1.merchant} onChange={e => handleChange('ref1', 'merchant', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Category
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.ref1.category} onChange={e => handleChange('ref1', 'category', e.target.value)} />
                      </label>
                    </div>
                    {/* Reference Transaction 2 */}
                    <div className="border rounded-xl p-4 bg-white">
                      <div className="font-bold text-lg mb-4 text-green-700">Reference Transaction 2</div>
                      <label className="text-sm font-medium mb-1 block">Date<span className="text-red-500">*</span>
                        <input type="date" className="input w-full border px-2 py-1 rounded mt-1" value={form.ref2.date} onChange={e => handleChange('ref2', 'date', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Time<span className="text-red-500">*</span>
                        <input type="time" className="input w-full border px-2 py-1 rounded mt-1" value={form.ref2.time} onChange={e => handleChange('ref2', 'time', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Amount<span className="text-red-500">*</span>
                        <input type="number" className="input w-full border px-2 py-1 rounded mt-1" value={form.ref2.amount} onChange={e => handleChange('ref2', 'amount', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">City<span className="text-red-500">*</span>
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.ref2.city} onChange={e => handleChange('ref2', 'city', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Country<span className="text-red-500">*</span>
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.ref2.country} onChange={e => handleChange('ref2', 'country', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Merchant<span className="text-red-500">*</span>
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.ref2.merchant} onChange={e => handleChange('ref2', 'merchant', e.target.value)} required />
                      </label>
                      <label className="text-sm font-medium mb-1 mt-2 block">Category
                        <input className="input w-full border px-2 py-1 rounded mt-1" value={form.ref2.category} onChange={e => handleChange('ref2', 'category', e.target.value)} />
                      </label>
                    </div>
                  </div>
                  <button
                    type="submit"
                    className="mt-6 w-full md:w-64 mx-auto block rounded-lg bg-blue-600 text-white font-semibold py-2"
                    disabled={loading}
                  >
                    {loading ? 'Checking...' : 'Check Fraud'}
                  </button>
                </form>
                {/* Error message */}
                {error && (
                  <div className="mt-4 text-center text-red-600 font-semibold">{error}</div>
                )}
                {/* Result card */}
                {result && (
                  <div className="mt-6 w-full flex flex-col items-center">
                    <div className={`text-3xl font-bold mb-2 ${result.verdict === 'Fraud' ? 'text-red-600' : result.verdict === 'Possible Fraud' ? 'text-yellow-500' : 'text-green-600'}`}>{result.verdict}</div>
                  </div>
                )}
              </div>
            </div>
          );
        };

      export default FraudComparisonModal;
