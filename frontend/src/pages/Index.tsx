import { MetricCard } from "@/components/MetricCard";
import { CashflowChart } from "@/components/CashflowChart";
import { RiskForecastPanel } from "@/components/RiskForecastPanel";
import { ExpenseChart } from "@/components/ExpenseChart";
import { IncomeChart } from "@/components/IncomeChart";
import { AIAlertsPanel } from "@/components/AIAlertsPanel";
import { TransactionsTable } from "@/components/TransactionsTable";

const Index = () => {
  return (
    <div className="flex-1 space-y-4 p-4 pt-6">
      {/* Top Metric Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          title="Net Cashflow"
          value="$23,450"
          trend="up"
          trendValue="+12.5%"
          risk="low"
        />
        <MetricCard
          title="Liquidity Score"
          value="72/100"
          trend="down"
          trendValue="-5.2%"
          risk="medium"
        />
        <MetricCard
          title="Cashflow Volatility"
          value="18.3%"
          trend="up"
          trendValue="+3.1%"
          risk="medium"
        />
        <MetricCard
          title="Projected Risk"
          value="High"
          trend="up"
          trendValue="Critical"
          risk="high"
        />
      </div>

      {/* Main Panels Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <div className="md:col-span-2">
          <CashflowChart />
        </div>
        <div>
          <RiskForecastPanel />
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
