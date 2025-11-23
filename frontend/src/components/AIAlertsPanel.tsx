import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, TrendingDown, AlertCircle, Info } from "lucide-react";

interface Alert {
  id: number;
  type: "warning" | "critical" | "info";
  message: string;
  timestamp: string;
}

const alerts: Alert[] = [
  {
    id: 1,
    type: "warning",
    message: "Potential negative cashflow next week",
    timestamp: "2 hours ago",
  },
  {
    id: 2,
    type: "critical",
    message: "Unusual spike in operational expenses",
    timestamp: "5 hours ago",
  },
  {
    id: 3,
    type: "warning",
    message: "Low liquidity window expected in 14 days",
    timestamp: "1 day ago",
  },
  {
    id: 4,
    type: "info",
    message: "Income pattern aligned with seasonal trends",
    timestamp: "2 days ago",
  },
];

export const AIAlertsPanel = () => {
  const getIcon = (type: string) => {
    switch (type) {
      case "critical":
        return <AlertTriangle className="w-4 h-4" />;
      case "warning":
        return <TrendingDown className="w-4 h-4" />;
      default:
        return <Info className="w-4 h-4" />;
    }
  };

  const getBadgeVariant = (type: string) => {
    switch (type) {
      case "critical":
        return "destructive";
      case "warning":
        return "secondary";
      default:
        return "outline";
    }
  };

  return (
    <Card className="p-6 animate-slide-up">
      <h3 className="text-lg font-semibold mb-4">AI Insights & Alerts</h3>
      <div className="space-y-3">
        {alerts.map((alert) => (
          <div
            key={alert.id}
            className="flex gap-3 p-3 rounded-lg border border-border hover:bg-accent/50 transition-colors"
          >
            <div className={alert.type === "critical" ? "text-destructive" : alert.type === "warning" ? "text-warning" : "text-primary"}>
              {getIcon(alert.type)}
            </div>
            <div className="flex-1 space-y-1">
              <p className="text-sm font-medium">{alert.message}</p>
              <p className="text-xs text-muted-foreground">{alert.timestamp}</p>
            </div>
            <Badge variant={getBadgeVariant(alert.type)} className="h-fit">
              {alert.type}
            </Badge>
          </div>
        ))}
      </div>
    </Card>
  );
};
