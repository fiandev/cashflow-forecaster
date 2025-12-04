import { useEffect, useState } from "react";
import { MetricCard } from "@/components/MetricCard";
import { CashflowChart } from "@/components/CashflowChart";
import { RiskForecastPanel } from "@/components/RiskForecastPanel";
import { ExpenseChart } from "@/components/ExpenseChart";
import { IncomeChart } from "@/components/IncomeChart";
import { AIAlertsPanel } from "@/components/AIAlertsPanel";
import { TransactionsTable } from "@/components/TransactionsTable";
import { authenticatedRequest, API_ENDPOINTS } from "@/lib/api";
import { Loader2, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useBusinessStore } from "@/stores/business-store";

interface DashboardMetrics {
  net_cashflow: number;
  net_cashflow_trend: "up" | "down" | "neutral";
  net_cashflow_percentage_change: number;
  liquidity_score: number;
  liquidity_score_trend: "up" | "down" | "neutral";
  liquidity_score_percentage_change: number;
  cashflow_volatility: number;
  cashflow_volatility_trend: "up" | "down" | "neutral";
  cashflow_volatility_percentage_change: number;
  projected_risk: string;
  projected_risk_trend: "up" | "down" | "neutral";
  projected_risk_status: string[];
  risk_breakdown: Array<{ category: string; level: number; description: string }>;
}

const Index = () => {
  const [dashboardMetrics, setDashboardMetrics] = useState<DashboardMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { currentBusiness } = useBusinessStore();

  const fetchMetrics = async () => {
    if (!currentBusiness) {
      setDashboardMetrics(null);
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const response = await authenticatedRequest(`${API_ENDPOINTS.dashboardMetrics}?business_id=${currentBusiness.id}`);
      if (!response.ok) {
        throw new Error(`Status: ${response.status}`);
      }
      const data: DashboardMetrics = await response.json();
      console.log("Dashboard Data Received:", data); // DEBUG LOG
      setDashboardMetrics(data);
    } catch (error) {
      console.error("Failed to fetch dashboard metrics:", error);
      setError("Failed to load dashboard metrics.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, [currentBusiness]);

  if (!currentBusiness) {
    return (
      <div className="flex-1 space-y-4 p-4 pt-6 flex items-center justify-center min-h-[calc(100vh-64px)]">
        <div className="text-center">
          <p className="text-muted-foreground">Please select a business first or create one</p>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex-1 space-y-4 p-4 pt-6 flex items-center justify-center min-h-[calc(100vh-64px)]">
        <Loader2 className="w-10 h-10 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 space-y-4 p-4 pt-6 flex flex-col items-center justify-center min-h-[calc(100vh-64px)] text-center">
        <AlertTriangle className="w-12 h-12 text-destructive mb-4" />
        <h3 className="text-lg font-semibold mb-2">Error Loading Dashboard</h3>
        <p className="text-muted-foreground mb-4">{error}</p>
        <Button onClick={fetchMetrics}>Try Again</Button>
      </div>
    );
  }

  // Safe access helpers with strict defaults
  const metrics = {
    net_cashflow: Number(dashboardMetrics?.net_cashflow) || 0,
    net_cashflow_trend: dashboardMetrics?.net_cashflow_trend || "neutral",
    net_cashflow_percentage_change: Number(dashboardMetrics?.net_cashflow_percentage_change) || 0,
    liquidity_score: Number(dashboardMetrics?.liquidity_score) || 0,
    liquidity_score_trend: dashboardMetrics?.liquidity_score_trend || "neutral",
    liquidity_score_percentage_change: Number(dashboardMetrics?.liquidity_score_percentage_change) || 0,
    cashflow_volatility: Number(dashboardMetrics?.cashflow_volatility) || 0,
    cashflow_volatility_trend: dashboardMetrics?.cashflow_volatility_trend || "neutral",
    cashflow_volatility_percentage_change: Number(dashboardMetrics?.cashflow_volatility_percentage_change) || 0,
    projected_risk: dashboardMetrics?.projected_risk || "Unknown",
    projected_risk_trend: dashboardMetrics?.projected_risk_trend || "neutral",
    projected_risk_status: Array.isArray(dashboardMetrics?.projected_risk_status) ? dashboardMetrics.projected_risk_status : [],
    risk_breakdown: Array.isArray(dashboardMetrics?.risk_breakdown) ? dashboardMetrics.risk_breakdown : [],
  };

  return (
    <div className="flex-1 space-y-4 p-4 pt-6">
      {/* Top Metric Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          title="Net Cashflow"
          value={`$${metrics.net_cashflow.toLocaleString(undefined, { maximumFractionDigits: 0 })}`}
          trend={metrics.net_cashflow_trend}
          trendValue={`${metrics.net_cashflow_percentage_change.toFixed(1)}%`}
          risk={
            metrics.net_cashflow_trend === "down" && metrics.net_cashflow_percentage_change < -10
              ? "critical"
              : metrics.net_cashflow_trend === "down"
              ? "high"
              : "low"
          }
        />
        <MetricCard
          title="Liquidity Score"
          value={`${metrics.liquidity_score.toFixed(0)}/100`}
          trend={metrics.liquidity_score_trend}
          trendValue={
            metrics.liquidity_score_percentage_change
              ? `${metrics.liquidity_score_percentage_change.toFixed(1)}%`
              : undefined
          }
          risk={
            metrics.liquidity_score < 50
              ? "critical"
              : metrics.liquidity_score < 75
              ? "medium"
              : "low"
          }
        />
        <MetricCard
          title="Cashflow Volatility"
          value={`${metrics.cashflow_volatility.toFixed(1)}%`}
          trend={metrics.cashflow_volatility_trend}
          trendValue={
            metrics.cashflow_volatility_percentage_change
              ? `${metrics.cashflow_volatility_percentage_change.toFixed(1)}%`
              : undefined
          }
          risk={
            metrics.cashflow_volatility > 20
              ? "high"
              : metrics.cashflow_volatility > 10
              ? "medium"
              : "low"
          }
        />
        <MetricCard
          title="Projected Risk"
          value={metrics.projected_risk}
          trend={metrics.projected_risk_trend}
          trendValue={
            metrics.projected_risk_status.length > 0
              ? metrics.projected_risk_status[0]
              : undefined
          }
          risk={(metrics.projected_risk.toLowerCase() || "medium") as "low" | "medium" | "high" | "critical"}
        />
      </div>

      {/* Main Panels Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <div className="md:col-span-2">
          <CashflowChart />
        </div>
        <div>
          <RiskForecastPanel riskData={metrics.risk_breakdown} />
        </div>
      </div>

      {/* Secondary Panels */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <ExpenseChart />
        <IncomeChart />
        <AIAlertsPanel />
      </div>

      {/* Transactions Table */}
      <TransactionsTable />
    </div>
  );
};

export default Index;
