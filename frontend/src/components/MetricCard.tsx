import { Card } from "@/components/ui/card";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string;
  trend?: "up" | "down" | "neutral";
  trendValue?: string;
  risk?: "low" | "medium" | "high" | "critical";
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  trend = "neutral",
  trendValue,
  risk,
}) => {
  const trendColor = trend === "up" ? "text-success" : trend === "down" ? "text-destructive" : "text-muted-foreground";
  const trendIcon =
    trend === "up" ? (
      <TrendingUp className="w-4 h-4" />
    ) : trend === "down" ? (
      <TrendingDown className="w-4 h-4" />
    ) : (
      <Minus className="w-4 h-4" />
    );

  return (
    <Card className="p-4 animate-slide-up">
      <div className="text-sm text-muted-foreground mb-1">{title}</div>
      <div className="text-2xl font-bold text-foreground">{value}</div>
      <div className="flex items-center gap-1 mt-2">
        {trendValue && (
          <span className={`flex items-center gap-1 text-sm ${trendColor}`}>
            {trendIcon}
            {trendValue}
          </span>
        )}
        {risk && (
          <span
            className={`text-xs capitalize px-2 py-1 rounded-full ${
              risk === "low"
                ? "bg-success/20 text-success"
                : risk === "medium"
                ? "bg-warning/20 text-warning"
                : risk === "high" || risk === "critical"
                ? "bg-destructive/20 text-destructive"
                : "bg-muted text-muted-foreground"
            }`}
          >
            {risk}
          </span>
        )}
      </div>
    </Card>
  );
};
