export interface Alert {
  id: number;
  business_id: number;
  created_at: string;
  level: 'info' | 'warning' | 'error' | 'critical';
  message: string;
  linked_transaction_id?: number;
  linked_forecast_id?: number;
  resolved: boolean;
  resolved_at?: string;
  forecast_metadata?: Record<string, any>;
}

export interface RiskScore {
  id: number;
  business_id: number;
  assessed_at: string;
  liquidity_score?: number;
  cashflow_risk_score?: number;
  volatility_index?: number;
  drawdown_prob?: number;
  source_forecast_id?: number;
  details?: Record<string, any>;
}

export interface AlertState {
  alerts: Alert[];
  riskScores: RiskScore[];
  unreadCount: number;
  isLoading: boolean;
  error: string | null;
  filters: {
    level?: string;
    resolved?: boolean;
    business_id?: number;
  };
}

export interface AlertActions {
  fetchAlerts: (businessId?: number) => Promise<void>;
  createAlert: (alertData: Omit<Alert, 'id' | 'created_at'>) => Promise<void>;
  updateAlert: (id: number, alertData: Partial<Alert>) => Promise<void>;
  resolveAlert: (id: number) => Promise<void>;
  deleteAlert: (id: number) => Promise<void>;
  fetchRiskScores: (businessId?: number) => Promise<void>;
  createRiskScore: (riskData: Omit<RiskScore, 'id' | 'assessed_at'>) => Promise<void>;
  setFilters: (filters: Partial<AlertState['filters']>) => void;
  clearFilters: () => void;
  clearError: () => void;
}

export type AlertStore = AlertState & AlertActions;