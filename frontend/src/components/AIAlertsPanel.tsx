import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, TrendingDown, AlertCircle, Info, Loader2 } from "lucide-react";
import { authenticatedRequest, API_ENDPOINTS } from "@/lib/api";
import { useBusinessStore } from "@/stores/business-store";

interface Alert {
  id: number;
  level: "warning" | "critical" | "info" | "error";
  message: string;
  created_at: string;
  business_id: number;
}

export const AIAlertsPanel = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { currentBusiness } = useBusinessStore();

  useEffect(() => {
    if (!currentBusiness) {
      setAlerts([]);
      setIsLoading(false);
      return;
    }

    const fetchAlerts = async () => {
      try {
        const response = await authenticatedRequest(`${API_ENDPOINTS.alerts}?business_id=${currentBusiness.id}`);
        const data = await response.json();
        // Sort by newest first and take top 5
        const sortedAlerts = data.sort((a: Alert, b: Alert) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        ).slice(0, 5);

        setAlerts(sortedAlerts);
      } catch (err) {
        console.error("Failed to fetch alerts:", err);
        setError("Could not load alerts.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchAlerts();
  }, [currentBusiness]);

  const getIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case "critical":
      case "error":
        return <AlertTriangle className="w-4 h-4" />;
      case "warning":
        return <TrendingDown className="w-4 h-4" />;
      default:
        return <Info className="w-4 h-4" />;
    }
  };

  const getBadgeVariant = (type: string) => {
    switch (type.toLowerCase()) {
      case "critical":
      case "error":
        return "destructive";
      case "warning":
        return "secondary";
      default:
        return "outline";
    }
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return "Just now";
    if (diffInHours < 24) return `${diffInHours} hours ago`;
    return `${Math.floor(diffInHours / 24)} days ago`;
  };

  if (!currentBusiness) {
    return (
      <Card className="p-6 animate-slide-up min-h-[200px] flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Please select a business first or create one</p>
        </div>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card className="p-6 animate-slide-up min-h-[200px] flex items-center justify-center">
        <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
      </Card>
    );
  }

  return (
    <Card className="p-4 sm:p-6 animate-slide-up">
      <h3 className="text-lg font-semibold mb-4">AI Insights & Alerts</h3>
      <div className="space-y-3">
        {alerts.length === 0 ? (
          <div className="text-center text-muted-foreground py-4">
            <Info className="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">No new alerts detected.</p>
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className="flex flex-col sm:flex-row gap-3 p-3 rounded-lg border border-border hover:bg-accent/50 transition-colors"
            >
              <div className={
                alert.level === "critical" ? "text-destructive" :
                alert.level === "warning" ? "text-warning" : "text-primary"
              }>
                {getIcon(alert.level)}
              </div>
              <div className="flex-1 space-y-1 sm:space-y-0">
                <p className="text-sm font-medium">{alert.message}</p>
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 sm:gap-0">
                  <p className="text-xs text-muted-foreground">{formatTime(alert.created_at)}</p>
                  <Badge
                    variant={getBadgeVariant(alert.level)}
                    className="h-fit capitalize self-start sm:self-auto w-fit"
                  >
                    {alert.level}
                  </Badge>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </Card>
  );
};
