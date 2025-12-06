import { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { Card } from "@/components/ui/card";
import { authenticatedRequest, API_ENDPOINTS } from "@/lib/api";
import { Loader2 } from "lucide-react";
import { useBusinessStore } from "@/stores/business-store";
import { formatCurrency } from "@/lib/utils";

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

export const IncomeChart = () => {
  const [data, setData] = useState<{ source: string; amount: number }[]>([]);
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

        const incomeMap: Record<string, number> = {};

        transactions
          .filter((t) => t.direction === "inflow")
          .forEach((t) => {
            const catName = categoryMap[t.category_id] || "Unknown";
            incomeMap[catName] = (incomeMap[catName] || 0) + t.amount;
          });

        const chartData = Object.entries(incomeMap).map(([source, amount]) => ({
          source,
          amount,
        }));

        setData(chartData);
      } catch (error) {
        console.error("Failed to load income data:", error);
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
      <h3 className="text-lg font-semibold mb-4">Income Stream Breakdown</h3>
      {data.length > 0 ? (
        <div className="h-96 lg:h-60">
          <ResponsiveContainer width="100%" height="100%" className="w-full overflow-x-auto">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis dataKey="source" stroke="hsl(var(--muted-foreground))" tick={{ fontSize: 8, textAnchor: 'end', dy: 5 }} />
              <YAxis stroke="hsl(var(--muted-foreground))" className="text-xs md:text-sm lg:text-base" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "var(--radius)",
                }}
                formatter={(value: number) => [formatCurrency(value, currentBusiness?.currency || 'USD'), ""]}
              />
              <Bar dataKey="amount" fill="hsl(var(--chart-2))" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="h-96 lg:h-60 flex items-center justify-center text-muted-foreground">
          No income data recorded for this business.
        </div>
      )}
    </Card>
  );
};
