import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface RiskTimelineChartProps {
  transactions: Array<{ date: string; time: string; fraud_probability: number }>;
}

const RiskTimelineChart: React.FC<RiskTimelineChartProps> = ({ transactions }) => {
  if (!transactions || transactions.length === 0) return <div className="text-gray-500">No data for timeline.</div>;
  const data = transactions.map(t => ({
    datetime: `${t.date} ${t.time}`,
    fraud_probability: t.fraud_probability,
  }));
  return (
    <div className="bg-white rounded shadow p-4">
      <div className="font-semibold mb-2">Risk Timeline</div>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <XAxis dataKey="datetime" tick={{ fontSize: 10 }} minTickGap={20} />
          <YAxis domain={[0, 1]} tickFormatter={v => `${Math.round(v * 100)}%`} />
          <Tooltip formatter={v => `${Math.round((v as number) * 100)}%`} />
          <Line type="monotone" dataKey="fraud_probability" stroke="#2563eb" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RiskTimelineChart;
