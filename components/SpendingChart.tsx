import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface SpendingChartProps {
  data: Array<{ date: string; amount: number }>;
}

const SpendingChart: React.FC<SpendingChartProps> = ({ data }) => {
  if (!data || data.length === 0) return <div className="text-gray-500">No timeline data.</div>;
  return (
    <div className="bg-white rounded shadow p-4">
      <div className="font-semibold mb-2">Spending Over Time</div>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip formatter={v => `$${v}`} />
          <Line type="monotone" dataKey="amount" stroke="#2563eb" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SpendingChart;
