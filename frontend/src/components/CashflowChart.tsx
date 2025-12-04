import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceDot } from "recharts";
import { Card } from "@/components/ui/card";
import { authenticatedRequest, API_ENDPOINTS } from "@/lib/api";
import { Loader2 } from "lucide-react";
import { format, parseISO } from "date-fns";
import { useBusinessStore } from "@/stores/business-store";

interface Transaction {
  date: string;
  amount: number;
  direction: "inflow" | "outflow";
  is_anomalous: boolean;
}

interface ChartData {
  date: string;
  cashIn: number;
  cashOut: number;
  anomaly: boolean;
}

export const CashflowChart = () => {
  const [data, setData] = useState<ChartData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const { currentBusiness } = useBusinessStore();

  useEffect(() => {
    if (!currentBusiness) {
      // No business selected, clear data and show message
      setData([]);
      setIsLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        setIsLoading(true);
        // Include the business ID in the API call when a business is selected
        const response = await authenticatedRequest(`${API_ENDPOINTS.transactions}?business_id=${currentBusiness.id}`);
        const transactions: Transaction[] = await response.json();

        // Process transactions into daily chart data
        const groupedData: Record<string, ChartData> = {};

        transactions.forEach((t) => {
          // Normalize date string just in case
          const dateStr = t.date.split('T')[0];

          if (!groupedData[dateStr]) {
            groupedData[dateStr] = {
              date: dateStr,
              cashIn: 0,
              cashOut: 0,
              anomaly: false,
            };
          }

          if (t.direction === "inflow") {
            groupedData[dateStr].cashIn += t.amount;
          } else {
            groupedData[dateStr].cashOut += t.amount;
          }

          if (t.is_anomalous) {
            groupedData[dateStr].anomaly = true;
          }
        });

        // Convert to array and sort by date
        const chartData = Object.values(groupedData).sort((a, b) =>
          new Date(a.date).getTime() - new Date(b.date).getTime()
        );

        // Format dates for display (e.g., "Jan 20")
        const formattedData = chartData.map(item => ({
          ...item,
          date: format(parseISO(item.date), "MMM d"),
          rawDate: item.date // Keep raw for sorting validation if needed
        }));

        setData(formattedData);
      } catch (error) {
        console.error("Failed to load cashflow data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [currentBusiness]);

  if (!currentBusiness) {
    return (
      <Card className="p-6 animate-slide-up min-h-[300px] flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Please select a business first or create one</p>
        </div>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card className="p-6 animate-slide-up min-h-[300px] flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
      </Card>
    );
  }

  return (
    <Card className="p-4 sm:p-6 animate-slide-up">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-4 sm:mb-6 gap-2">
        <h3 className="text-lg font-semibold">Cashflow Timeline (Daily)</h3>
      </div>
      <div className="h-60 xs:h-64 sm:h-72 md:h-80">
        <ResponsiveContainer className="w-full overflow-x-auto">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" tick={{ fontSize: 8, textAnchor: 'end', dy: 5 }} />
            <YAxis stroke="hsl(var(--muted-foreground))" tick={{ fontSize: 8 }} />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
              formatter={(value: number) => [`$${value.toLocaleString()}`, ""]}
              wrapperStyle={{ zIndex: 100 }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="cashIn"
              stroke="hsl(var(--chart-2))"
              strokeWidth={2}
              dot={{ fill: "hsl(var(--chart-2))", r: 2, strokeWidth: 0 }}
              activeDot={{ r: 4 }}
              name="Cash In"
            />
            <Line
              type="monotone"
              dataKey="cashOut"
              stroke="hsl(var(--chart-1))"
              strokeWidth={2}
              dot={{ fill: "hsl(var(--chart-1))", r: 2, strokeWidth: 0 }}
              activeDot={{ r: 4 }}
              name="Cash Out"
            />
            {data.map((entry, index) =>
              entry.anomaly ? (
                <ReferenceDot
                  key={index}
                  x={entry.date}
                  y={entry.cashOut > entry.cashIn ? entry.cashOut : entry.cashIn}
                  r={4}
                  fill="hsl(var(--destructive))"
                  stroke="none"
                  ifOverflow="extendDomain"
                />
              ) : null
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>
      {data.length === 0 && (
        <div className="text-center text-muted-foreground mt-4">
          No transaction data available to display for this business.
        </div>
      )}
    </Card>
  );
};
