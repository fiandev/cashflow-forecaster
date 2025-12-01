import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, TrendingDown, AlertCircle, Info } from "lucide-react";

interface Alert {
  id: number;
  type: "warning" | "critical" | "info";
  message: string;
  timestamp: string;
}

interface AIAlertsPanelProps {
  alerts: Alert[];
}

export const AIAlertsPanel = ({ alerts = [] }: AIAlertsPanelProps) => {
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
