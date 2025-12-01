import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { Card } from "@/components/ui/card";

interface IncomeData {
  source: string;
  amount: number;
}

interface IncomeChartProps {
  incomeData: IncomeData[];
}

export const IncomeChart = ({ incomeData }: IncomeChartProps) => {
  const data = incomeData || [
    { source: "Product Sales", amount: 45000 },
    { source: "Services", amount: 32000 },
    { source: "Subscriptions", amount: 18000 },
    { source: "Consulting", amount: 12000 },
  ];

  return (
    <Card className="p-6 animate-slide-up">
      <h3 className="text-lg font-semibold mb-4">Income Stream Breakdown</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis dataKey="source" stroke="hsl(var(--muted-foreground))" tick={{ fontSize: 12 }} />
          <YAxis stroke="hsl(var(--muted-foreground))" />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "var(--radius)",
            }}
          />
          <Bar dataKey="amount" fill="hsl(var(--chart-2))" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
};
