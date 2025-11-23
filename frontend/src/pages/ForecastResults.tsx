import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  Area,
  ComposedChart,
} from "recharts";
import {
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  Info,
  ArrowLeft,
} from "lucide-react";

// Simulated forecast data
const generateForecastData = (period: string) => {
  const days = parseInt(period);
  const data = [];
  let balance = 45000;

  for (let i = 0; i <= days; i++) {
    const isHistorical = i <= 7;
    const variance = Math.random() * 5000 - 2500;
    const trend = i * 50;
    
    balance = balance + variance + trend;
    
    data.push({
      day: `Day ${i}`,
      actual: isHistorical ? balance : null,
      forecast: !isHistorical ? balance : null,
      upperBound: !isHistorical ? balance + 8000 : null,
      lowerBound: !isHistorical ? balance - 8000 : null,
      cashIn: 15000 + Math.random() * 5000,
      cashOut: 12000 + Math.random() * 4000,
    });
  }

  return data;
};

const riskMetrics = [
  { name: "Liquidity Risk", level: 35, status: "low", color: "success" },
  { name: "Volatility Risk", level: 58, status: "medium", color: "warning" },
  { name: "Burn Rate Risk", level: 42, status: "medium", color: "warning" },
  { name: "Cash Shortage Risk", level: 28, status: "low", color: "success" },
];

const aiInsights = [
  {
    type: "positive",
    title: "Strong Projected Growth",
    message: "Your forecasted cashflow shows a positive trend with 12% growth over the selected period.",
  },
  {
    type: "warning",
    title: "Volatility Detected",
    message: "Week 3-4 may experience higher than usual cashflow fluctuations. Consider maintaining a buffer.",
  },
  {
    type: "info",
    title: "Optimization Opportunity",
    message: "Consolidating expenses in weeks 2 and 5 could reduce volatility by 8%.",
  },
];

const scenarioData = [
  { scenario: "Best Case", projection: 68500, probability: 25 },
  { scenario: "Expected", projection: 52300, probability: 50 },
  { scenario: "Worst Case", projection: 38200, probability: 25 },
];

const ForecastResults = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const forecastPeriod = location.state?.forecastPeriod || "30";
  const [activeView, setActiveView] = useState<"cashflow" | "scenarios">("cashflow");

  const forecastData = generateForecastData(forecastPeriod);

  const getIconByType = (type: string) => {
    switch (type) {
      case "positive":
        return <CheckCircle className="w-5 h-5 text-success" />;
      case "warning":
        return <AlertTriangle className="w-5 h-5 text-warning" />;
      default:
        return <Info className="w-5 h-5 text-primary" />;
    }
  };

  const getRiskColor = (level: number) => {
    if (level < 40) return "hsl(var(--success))";
    if (level < 70) return "hsl(var(--warning))";
    return "hsl(var(--destructive))";
  };

  return (
    <div className="flex-1 space-y-4 p-4 pt-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center gap-4 mb-8">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate("/forecast")}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Input
          </Button>
          <div className="flex-1">
            <h2 className="text-3xl font-bold mb-2">AI Forecast Simulation</h2>
            <p className="text-muted-foreground">
              {forecastPeriod}-day cashflow projection with risk analysis
            </p>
          </div>
          <Badge variant="secondary" className="text-sm">
            Simulated Data
          </Badge>
        </div>

        {/* Key Metrics Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card className="p-4">
            <div className="text-sm text-muted-foreground mb-1">
              Projected Balance
            </div>
            <div className="text-2xl font-bold text-foreground">
              ${forecastData[forecastData.length - 1].forecast?.toFixed(0)}
            </div>
            <div className="flex items-center gap-1 mt-2 text-success text-sm">
              <TrendingUp className="w-4 h-4" />
              <span>+12.4%</span>
            </div>
          </Card>

          <Card className="p-4">
            <div className="text-sm text-muted-foreground mb-1">
              Confidence Level
            </div>
            <div className="text-2xl font-bold text-foreground">78%</div>
            <Progress value={78} className="mt-2 h-2" />
          </Card>

          <Card className="p-4">
            <div className="text-sm text-muted-foreground mb-1">
              Risk Score
            </div>
            <div className="text-2xl font-bold text-warning">Medium</div>
            <div className="text-xs text-muted-foreground mt-2">
              Overall: 42/100
            </div>
          </Card>

          <Card className="p-4">
            <div className="text-sm text-muted-foreground mb-1">
              Buffer Days
            </div>
            <div className="text-2xl font-bold text-foreground">18</div>
            <div className="text-xs text-muted-foreground mt-2">
              Days of runway
            </div>
          </Card>
        </div>

        {/* Main Chart */}
        <Card className="p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold">Cashflow Forecast</h3>
            <div className="flex gap-2">
              <Button
                variant={activeView === "cashflow" ? "default" : "outline"}
                size="sm"
                onClick={() => setActiveView("cashflow")}
              >
                Cashflow View
              </Button>
              <Button
                variant={activeView === "scenarios" ? "default" : "outline"}
                size="sm"
                onClick={() => setActiveView("scenarios")}
              >
                Scenarios
              </Button>
            </div>
          </div>

          {activeView === "cashflow" ? (
            <ResponsiveContainer width="100%" height={400}>
              <ComposedChart data={forecastData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis
                  dataKey="day"
                  stroke="hsl(var(--muted-foreground))"
                  tick={{ fontSize: 12 }}
                  interval={Math.floor(forecastData.length / 8)}
                />
                <YAxis stroke="hsl(var(--muted-foreground))" tick={{ fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                  }}
                />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="upperBound"
                  fill="hsl(var(--primary) / 0.1)"
                  stroke="none"
                />
                <Area
                  type="monotone"
                  dataKey="lowerBound"
                  fill="hsl(var(--background))"
                  stroke="none"
                />
                <Line
                  type="monotone"
                  dataKey="actual"
                  stroke="hsl(var(--primary))"
                  strokeWidth={2}
                  dot={false}
                  name="Historical"
                />
                <Line
                  type="monotone"
                  dataKey="forecast"
                  stroke="hsl(var(--success))"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={false}
                  name="Forecast"
                />
                <ReferenceLine
                  x="Day 7"
                  stroke="hsl(var(--muted-foreground))"
                  strokeDasharray="3 3"
                  label="Today"
                />
              </ComposedChart>
            </ResponsiveContainer>
          ) : (
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={scenarioData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="scenario" stroke="hsl(var(--muted-foreground))" />
                <YAxis stroke="hsl(var(--muted-foreground))" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                  }}
                />
                <Bar dataKey="projection" fill="hsl(var(--primary))" radius={[8, 8, 0, 0]} />
                <Bar dataKey="probability" fill="hsl(var(--success))" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Risk Analysis */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Risk Analysis</h3>
            <div className="space-y-4">
              {riskMetrics.map((risk) => (
                <div key={risk.name} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">{risk.name}</span>
                    <Badge
                      variant={
                        risk.color === "success"
                          ? "default"
                          : risk.color === "warning"
                          ? "secondary"
                          : "destructive"
                      }
                    >
                      {risk.status}
                    </Badge>
                  </div>
                  <div className="relative h-2 bg-muted rounded-full overflow-hidden">
                    <div
                      className="absolute left-0 top-0 h-full rounded-full transition-all"
                      style={{
                        width: `${risk.level}%`,
                        backgroundColor: getRiskColor(risk.level),
                      }}
                    />
                  </div>
                  <div className="text-xs text-muted-foreground text-right">
                    {risk.level}% risk level
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* AI Insights */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">AI Insights</h3>
            <div className="space-y-4">
              {aiInsights.map((insight, index) => (
                <div key={index} className="flex gap-3 p-3 rounded-lg bg-muted/50">
                  <div className="flex-shrink-0 mt-1">
                    {getIconByType(insight.type)}
                  </div>
                  <div className="flex-1">
                    <h4 className="text-sm font-semibold mb-1">
                      {insight.title}
                    </h4>
                    <p className="text-sm text-muted-foreground">
                      {insight.message}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ForecastResults;
