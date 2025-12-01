import { useEffect, useState } from "react";
import { MetricCard } from "@/components/MetricCard";
import { CashflowChart } from "@/components/CashflowChart";
import { RiskForecastPanel } from "@/components/RiskForecastPanel";
import { ExpenseChart } from "@/components/ExpenseChart";
import { IncomeChart } from "@/components/IncomeChart";
import { AIAlertsPanel } from "@/components/AIAlertsPanel";
import { TransactionsTable } from "@/components/TransactionsTable";
import { useBusiness } from "@/contexts/BusinessContext";
import { authenticatedRequest } from "@/lib/api";

interface MetricCardData {
  net_cashflow: string;
  net_cashflow_trend: "up" | "down" | "neutral";
  net_cashflow_trend_value: string;
  net_cashflow_risk: "low" | "medium" | "high";
  liquidity_score: string;
  liquidity_score_trend: "up" | "down" | "neutral";
  liquidity_score_trend_value: string;
  liquidity_score_risk: "low" | "medium" | "high";
  cashflow_volatility: string;
  cashflow_volatility_trend: "up" | "down" | "neutral";
  cashflow_volatility_trend_value: string;
  cashflow_volatility_risk: "low" | "medium" | "high";
  projected_risk: string;
  projected_risk_trend: "up" | "down" | "neutral";
  projected_risk_trend_value: string;
  projected_risk_risk: "low" | "medium" | "high";
}

interface DashboardData {
  metrics: MetricCardData;
  cashflow_chart: {
    daily: Array<{ date: string; cashIn: number; cashOut: number; anomaly: boolean }>;
    weekly: Array<{ date: string; cashIn: number; cashOut: number; anomaly: boolean }>;
    monthly: Array<{ date: string; cashIn: number; cashOut: number; anomaly: boolean }>;
  };
  risk_forecast: Array<{
    category: string;
    level: number;
    description: string;
  }>;
  expense_chart: Array<{
    name: string;
    value: number;
  }>;
  income_chart: Array<{
    source: string;
    amount: number;
  }>;
  ai_alerts: Array<{
    id: number;
    message: string;
    timestamp: string;
    type: "warning" | "critical" | "info";
  }>;
  transactions: Array<{
    id: number;
    date: string;
    description: string;
    inflow: number;
    outflow: number;
    category: string;
    aiTag: "Normal" | "Unusual";
  }>;
}

const Index = () => {
  const { currentBusiness } = useBusiness();
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [generatingAlerts, setGeneratingAlerts] = useState(false);

  useEffect(() => {
    const fetchDashboardData = async () => {
      if (!currentBusiness) return;

      try {
        setLoading(true);
        const response = await authenticatedRequest(`/api/dashboard/stats/${currentBusiness.id}`);
        const data = await response.json();
        setDashboardData(data);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [currentBusiness]);

  const handleGenerateAIAlerts = async () => {
    if (!currentBusiness) return;

    try {
      setGeneratingAlerts(true);
      const response = await authenticatedRequest(`/api/dashboard/generate-ai-alerts/${currentBusiness.id}`, {
        method: "POST",
      });
      const data = await response.json();

      if (response.ok) {
        // Refresh dashboard data to show new alerts
        const refreshResponse = await authenticatedRequest(`/api/dashboard/stats/${currentBusiness.id}`);
        const refreshData = await refreshResponse.json();
        setDashboardData(refreshData);
        console.log("AI alerts generated successfully:", data);
      } else {
        console.error("Error generating AI alerts:", data.error);
      }
    } catch (error) {
      console.error("Error generating AI alerts:", error);
    } finally {
      setGeneratingAlerts(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 space-y-4 p-4 pt-6">
        <div className="text-center py-10">
          Loading dashboard data...
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 space-y-4 p-4 pt-6">
      {/* Top Metric Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          title="Net Cashflow"
          value={dashboardData?.metrics?.net_cashflow || "$0.00"}
          trend={dashboardData?.metrics?.net_cashflow_trend || "neutral"}
          trendValue={dashboardData?.metrics?.net_cashflow_trend_value || "0%"}
          risk={dashboardData?.metrics?.net_cashflow_risk || "low"}
        />
        <MetricCard
          title="Liquidity Score"
          value={dashboardData?.metrics?.liquidity_score || "0/100"}
          trend={dashboardData?.metrics?.liquidity_score_trend || "neutral"}
          trendValue={dashboardData?.metrics?.liquidity_score_trend_value || "0%"}
          risk={dashboardData?.metrics?.liquidity_score_risk || "low"}
        />
        <MetricCard
          title="Cashflow Volatility"
          value={dashboardData?.metrics?.cashflow_volatility || "0%"}
          trend={dashboardData?.metrics?.cashflow_volatility_trend || "neutral"}
          trendValue={dashboardData?.metrics?.cashflow_volatility_trend_value || "0%"}
          risk={dashboardData?.metrics?.cashflow_volatility_risk || "low"}
        />
        <MetricCard
          title="Projected Risk"
          value={dashboardData?.metrics?.projected_risk || "Low"}
          trend={dashboardData?.metrics?.projected_risk_trend || "neutral"}
          trendValue={dashboardData?.metrics?.projected_risk_trend_value || "Stable"}
          risk={dashboardData?.metrics?.projected_risk_risk || "low"}
        />
      </div>

      {/* Main Panels Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <div className="md:col-span-2">
          <CashflowChart chartData={dashboardData?.cashflow_chart || { daily: [], weekly: [], monthly: [] }} />
        </div>
        <div>
          <RiskForecastPanel riskData={dashboardData?.risk_forecast || []} />
        </div>
      </div>

      {/* Secondary Panels */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <ExpenseChart expenseData={dashboardData?.expense_chart || []} />
        <IncomeChart incomeData={dashboardData?.income_chart || []} />
        <div>
          <div className="flex justify-between items-center mb-2">
            <h3 className="text-lg font-semibold">AI Alerts</h3>
            <button
              onClick={handleGenerateAIAlerts}
              disabled={generatingAlerts}
              className="p-2 rounded-md hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              title="Refresh AI Alerts"
            >
              {generatingAlerts ? (
                <svg className="w-5 h-5 text-blue-500 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              ) : (
                <svg className="w-5 h-5 text-gray-600 hover:text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              )}
            </button>
          </div>
          <AIAlertsPanel alerts={dashboardData?.ai_alerts || []} />
        </div>
      </div>

      {/* Transactions Table */}
      <TransactionsTable transactions={dashboardData?.transactions || []} />
    </div>
  );
};

export default Index;
