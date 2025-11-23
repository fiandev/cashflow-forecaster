import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceDot } from "recharts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const dailyData = [
  { date: "Mon", cashIn: 12000, cashOut: 8000, anomaly: false },
  { date: "Tue", cashIn: 15000, cashOut: 9500, anomaly: false },
  { date: "Wed", cashIn: 11000, cashOut: 13000, anomaly: true },
  { date: "Thu", cashIn: 18000, cashOut: 10000, anomaly: false },
  { date: "Fri", cashIn: 20000, cashOut: 12000, anomaly: false },
  { date: "Sat", cashIn: 8000, cashOut: 7000, anomaly: false },
  { date: "Sun", cashIn: 6000, cashOut: 5000, anomaly: false },
];

const weeklyData = [
  { date: "Week 1", cashIn: 85000, cashOut: 62000, anomaly: false },
  { date: "Week 2", cashIn: 92000, cashOut: 68000, anomaly: false },
  { date: "Week 3", cashIn: 78000, cashOut: 85000, anomaly: true },
  { date: "Week 4", cashIn: 105000, cashOut: 72000, anomaly: false },
];

const monthlyData = [
  { date: "Jan", cashIn: 340000, cashOut: 280000, anomaly: false },
  { date: "Feb", cashIn: 360000, cashOut: 295000, anomaly: false },
  { date: "Mar", cashIn: 320000, cashOut: 310000, anomaly: true },
  { date: "Apr", cashIn: 395000, cashOut: 285000, anomaly: false },
];

type TimeFrame = "daily" | "weekly" | "monthly";

export const CashflowChart = () => {
  const [timeFrame, setTimeFrame] = useState<TimeFrame>("daily");

  const dataMap = {
    daily: dailyData,
    weekly: weeklyData,
    monthly: monthlyData,
  };

  const data = dataMap[timeFrame];

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
