import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface MerchantBarChartProps {
  analytics: { total_per_merchant: Record<string, number> };
}

const MerchantBarChart: React.FC<MerchantBarChartProps> = ({ analytics }) => {
  if (!analytics || !analytics.total_per_merchant) return <div className="text-gray-500">No merchant data.</div>;
  const data = Object.entries(analytics.total_per_merchant)
    .map(([merchant, value]) => ({ merchant, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 10);
  return (
    <div className="bg-white rounded shadow p-4">
      <div className="font-semibold mb-2">Top Merchants by Spending</div>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} layout="vertical">
          <XAxis type="number" hide />
          <YAxis dataKey="merchant" type="category" width={100} />
          <Tooltip formatter={v => `$${v}`} />
          <Bar dataKey="value" fill="#2563eb" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default MerchantBarChart;
