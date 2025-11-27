import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

interface SpendingPieChartProps {
  analytics: { total_per_category: Record<string, number> };
}

const COLORS = ['#2563eb', '#22d3ee', '#f59e42', '#f43f5e', '#10b981', '#a78bfa', '#fbbf24', '#6366f1'];

const SpendingPieChart: React.FC<SpendingPieChartProps> = ({ analytics }) => {
  if (!analytics || !analytics.total_per_category) return <div className="text-gray-500">No category data.</div>;
  const data = Object.entries(analytics.total_per_category).map(([cat, value]) => ({ name: cat, value }));
  return (
    <div className="bg-white rounded shadow p-4">
      <div className="font-semibold mb-2">Spending by Category</div>
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={70} label>
            {data.map((_, i) => (
              <Cell key={`cell-${i}`} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={v => `$${v}`} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SpendingPieChart;
