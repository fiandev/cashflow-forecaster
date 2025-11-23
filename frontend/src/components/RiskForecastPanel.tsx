import { Card } from "@/components/ui/card";
import { AlertCircle } from "lucide-react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface RiskItem {
  category: string;
  level: number;
  description: string;
}

const riskData: RiskItem[] = [
  { category: "Cashflow Risk", level: 35, description: "Moderate risk of negative cashflow in next 2 weeks" },
  { category: "Debt Risk", level: 15, description: "Low debt exposure relative to revenue" },
  { category: "Burn Rate Risk", level: 65, description: "Current spending rate may exceed income" },
  { category: "Drawdown Probability", level: 45, description: "Medium probability of needing emergency funds" },
];

export const RiskForecastPanel = () => {
  const getRiskColor = (level: number) => {
    if (level < 30) return "bg-success";
    if (level < 60) return "bg-warning";
    return "bg-destructive";
  };

  const getRiskBgColor = (level: number) => {
    if (level < 30) return "bg-success/10";
    if (level < 60) return "bg-warning/10";
    return "bg-destructive/10";
  };

  return (
    <Card className="p-6 animate-slide-up">
      <h3 className="text-lg font-semibold mb-6">AI Risk Forecast</h3>
      <div className="space-y-4">
        {riskData.map((risk, index) => (
          <div key={index} className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium">{risk.category}</span>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger>
                      <AlertCircle className="w-4 h-4 text-muted-foreground" />
                    </TooltipTrigger>
                    <TooltipContent>
                      <p className="max-w-xs">{risk.description}</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>
              <span className="text-sm font-semibold">{risk.level}%</span>
            </div>
            <div className={`h-2 rounded-full ${getRiskBgColor(risk.level)}`}>
              <div
                className={`h-full rounded-full transition-all duration-500 ${getRiskColor(risk.level)}`}
                style={{ width: `${risk.level}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
