import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { Card } from "@/components/ui/card";

interface MetricCardProps {
  title: string;
  value: string;
  trend: "up" | "down" | "neutral";
  trendValue: string;
  risk: "low" | "medium" | "high";
}

export const MetricCard = ({ title, value, trend, trendValue, risk }: MetricCardProps) => {
  const riskColors = {
    low: "text-success",
    medium: "text-warning",
    high: "text-destructive",
  };

  const TrendIcon = trend === "up" ? TrendingUp : trend === "down" ? TrendingDown : Minus;

  return (
    <Card className="p-6 hover:shadow-lg transition-shadow duration-300 animate-slide-up">
      <div className="space-y-3">
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        <div className="flex items-baseline justify-between">
          <h3 className="text-3xl font-bold tracking-tight">{value}</h3>
          <div className={`flex items-center gap-1 text-sm font-medium ${riskColors[risk]}`}>
            <TrendIcon className="w-4 h-4" />
            <span>{trendValue}</span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className={`h-1 flex-1 rounded-full ${risk === "low" ? "bg-success/20" : risk === "medium" ? "bg-warning/20" : "bg-destructive/20"}`}>
            <div 
              className={`h-full rounded-full transition-all duration-500 ${risk === "low" ? "bg-success w-3/4" : risk === "medium" ? "bg-warning w-1/2" : "bg-destructive w-1/4"}`}
            />
          </div>
        </div>
      </div>
    </Card>
  );
};
