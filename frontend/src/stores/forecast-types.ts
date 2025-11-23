export interface Forecast {
  id: number;
  business_id: number;
  model_run_id?: number;
  model_id?: number;
  created_at: string;
  granularity: 'daily' | 'weekly' | 'monthly';
  period_start: string;
  period_end: string;
  predicted_value?: number;
  lower_bound?: number;
  upper_bound?: number;
  forecast_metadata?: Record<string, any>;
}

export interface Model {
  id: number;
  business_id?: number;
  name: string;
  model_type: string;
  params?: Record<string, any>;
  version?: string;
  last_trained_at?: string;
  created_at: string;
}

export interface ModelRun {
  id: number;
  model_id: number;
  run_at: string;
  input_summary?: Record<string, any>;
  output_summary?: Record<string, any>;
  run_status: 'completed' | 'running' | 'failed';
  notes?: string;
}

export interface ForecastState {
  forecasts: Forecast[];
  models: Model[];
  modelRuns: ModelRun[];
  currentForecast: Forecast | null;
  isLoading: boolean;
  error: string | null;
}

export interface ForecastActions {
  fetchForecasts: (businessId: number) => Promise<void>;
  createForecast: (forecastData: Omit<Forecast, 'id' | 'created_at'>) => Promise<void>;
  updateForecast: (id: number, forecastData: Partial<Forecast>) => Promise<void>;
  deleteForecast: (id: number) => Promise<void>;
  fetchModels: (businessId?: number) => Promise<void>;
  createModel: (modelData: Omit<Model, 'id' | 'created_at'>) => Promise<void>;
  updateModel: (id: number, modelData: Partial<Model>) => Promise<void>;
  deleteModel: (id: number) => Promise<void>;
  fetchModelRuns: (modelId?: number) => Promise<void>;
  runModel: (modelId: number, params?: Record<string, any>) => Promise<void>;
  setCurrentForecast: (forecast: Forecast | null) => void;
  clearError: () => void;
}

export type ForecastStore = ForecastState & ForecastActions;