import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceDot } from "recharts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface CashflowDataPoint {
  date: string;
  cashIn: number;
  cashOut: number;
  anomaly: boolean;
}

interface CashflowChartData {
  daily: CashflowDataPoint[];
  weekly: CashflowDataPoint[];
  monthly: CashflowDataPoint[];
}

interface CashflowChartProps {
  chartData: CashflowChartData;
}

type TimeFrame = "daily" | "weekly" | "monthly";

export const CashflowChart = ({ chartData }: CashflowChartProps) => {
  const [timeFrame, setTimeFrame] = useState<TimeFrame>("daily"); // Keep default as daily

  const dataMap = {
    daily: chartData?.daily || [],
    weekly: chartData?.weekly || [],
    monthly: chartData?.monthly || [],
  };

  // Get the current data based on selected time frame
  let data = dataMap[timeFrame];

  // Special handling for daily chart when there's sparse data (0 or 1 data points)
  // Expand to show all 7 days of the week for better context
  if (timeFrame === "daily" && data.length <= 1) {
    // Create full week data in chronological order: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    const allDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const expandedData = allDays.map(day => {
      // Check if this day exists in the original sparse data
      const originalDataPoint = data.find(d => d.date === day);
      if (originalDataPoint) {
        // Use original values if day exists
        return originalDataPoint;
      } else {
        // Return zero values for days without data
        return {
          date: day,
          cashIn: 0,
          cashOut: 0,
          anomaly: false,
        };
      }
    });
    data = expandedData;
  }

  return (
    <Card className="p-6 animate-slide-up">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold">Cashflow Timeline</h3>
        <div className="flex gap-2">
          {(["daily", "weekly", "monthly"] as TimeFrame[]).map((frame) => (
            <Button
              key={frame}
              variant={timeFrame === frame ? "default" : "outline"}
              size="sm"
              onClick={() => setTimeFrame(frame)}
              className="capitalize"
            >
              {frame}
            </Button>
          ))}
        </div>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" />
          <YAxis stroke="hsl(var(--muted-foreground))" />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "var(--radius)",
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="cashIn"
            stroke="hsl(var(--chart-2))"
            strokeWidth={2}
            dot={{ fill: "hsl(var(--chart-2))" }}
            name="Cash In"
          />
          <Line
            type="monotone"
            dataKey="cashOut"
            stroke="hsl(var(--chart-1))"
            strokeWidth={2}
            dot={{ fill: "hsl(var(--chart-1))" }}
            name="Cash Out"
          />
          {data.map((entry, index) =>
            entry.anomaly ? (
              <ReferenceDot
                key={index}
                x={entry.date}
                y={entry.cashOut}
                r={8}
                fill="hsl(var(--destructive))"
                stroke="hsl(var(--card))"
                strokeWidth={2}
              />
            ) : null
          )}
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
};
