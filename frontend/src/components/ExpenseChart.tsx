import { useState, useEffect } from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";
import { Card } from "@/components/ui/card";
import { authenticatedRequest, API_ENDPOINTS } from "@/lib/api";
import { Loader2 } from "lucide-react";
import { useBusinessStore } from "@/stores/business-store";

interface Transaction {
  amount: number;
  direction: "inflow" | "outflow";
  category_id: number;
  business_id: number;
}

interface Category {
  id: number;
  name: string;
  business_id: number;
}

const COLORS = [
  "hsl(var(--chart-1))",
  "hsl(var(--chart-2))",
  "hsl(var(--chart-3))",
  "hsl(var(--chart-4))",
  "hsl(var(--chart-5))",
];

export const ExpenseChart = () => {
  const [data, setData] = useState<{ name: string; value: number }[]>([]);
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

        const [transactionsRes, categoriesRes] = await Promise.all([
          authenticatedRequest(`${API_ENDPOINTS.transactions}?business_id=${currentBusiness.id}`),
          authenticatedRequest(`${API_ENDPOINTS.categories}?business_id=${currentBusiness.id}`),
        ]);

        const transactions: Transaction[] = await transactionsRes.json();
        const categories: Category[] = await categoriesRes.json();

        const categoryMap = categories.reduce((acc, cat) => {
          acc[cat.id] = cat.name;
          return acc;
        }, {} as Record<number, string>);

        const expenseMap: Record<string, number> = {};

        transactions
          .filter((t) => t.direction === "outflow")
          .forEach((t) => {
            const catName = categoryMap[t.category_id] || "Unknown";
            expenseMap[catName] = (expenseMap[catName] || 0) + t.amount;
          });

        const chartData = Object.entries(expenseMap).map(([name, value]) => ({
          name,
          value,
        }));

        setData(chartData);
      } catch (error) {
        console.error("Failed to load expense data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [currentBusiness]);

  if (!currentBusiness) {
    return (
      <Card className="p-6 animate-slide-up min-h-[250px] flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Please select a business first or create one</p>
        </div>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card className="p-6 animate-slide-up min-h-[250px] flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
      </Card>
    );
  }

  return (
    <Card className="p-4 sm:p-6 animate-slide-up">
      <h3 className="text-lg font-semibold mb-4">Expense Composition</h3>
      {data.length > 0 ? (
        <div className="h-60 xs:h-64 sm:h-72">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={30}
                outerRadius={60}
                fill="#8884d8"
                paddingAngle={2}
                dataKey="value"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "var(--radius)",
                }}
                formatter={(value: number) => [`$${value.toLocaleString()}`, ""]}
              />
              <Legend layout="vertical" verticalAlign="middle" align="right" className="hidden sm:block" />
              <Legend layout="horizontal" verticalAlign="bottom" align="center" className="sm:hidden" />
            </PieChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="h-60 xs:h-64 sm:h-72 flex items-center justify-center text-muted-foreground">
          No expense data recorded for this business.
        </div>
      )}
    </Card>
  );
};
