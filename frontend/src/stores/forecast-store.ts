import { create } from 'zustand';
import { ForecastStore } from './forecast-types';

const API_BASE = '/api';

export const useForecastStore = create<ForecastStore>((set) => ({
  forecasts: [],
  models: [],
  modelRuns: [],
  currentForecast: null,
  isLoading: false,
  error: null,

  fetchForecasts: async (businessId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/forecasts?business_id=${businessId}`);
      if (response.ok) {
        const forecastsData = await response.json();
        set({
          forecasts: forecastsData,
          isLoading: false,
          error: null,
        });
      } else {
        throw new Error('Failed to fetch forecasts');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch forecasts',
        isLoading: false,
      });
    }
  },

  createForecast: async (forecastData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/forecasts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(forecastData),
      });

      if (response.ok) {
        const newForecast = await response.json();
        set((state) => ({
          forecasts: [...state.forecasts, newForecast],
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create forecast');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to create forecast',
        isLoading: false,
      });
    }
  },

  updateForecast: async (id, forecastData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/forecasts/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(forecastData),
      });

      if (response.ok) {
        const updatedForecast = await response.json();
        set((state) => ({
          forecasts: state.forecasts.map((f) => (f.id === id ? updatedForecast : f)),
          currentForecast: state.currentForecast?.id === id ? updatedForecast : state.currentForecast,
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to update forecast');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to update forecast',
        isLoading: false,
      });
    }
  },

  deleteForecast: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/forecasts/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        set((state) => ({
          forecasts: state.forecasts.filter((f) => f.id !== id),
          currentForecast: state.currentForecast?.id === id ? null : state.currentForecast,
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete forecast');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to delete forecast',
        isLoading: false,
      });
    }
  },

  fetchModels: async (businessId) => {
    set({ isLoading: true, error: null });
    try {
      const url = businessId ? `${API_BASE}/models?business_id=${businessId}` : `${API_BASE}/models`;
      const response = await fetch(url);
      if (response.ok) {
        const modelsData = await response.json();
        set({
          models: modelsData,
          isLoading: false,
          error: null,
        });
      } else {
        throw new Error('Failed to fetch models');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch models',
        isLoading: false,
      });
    }
  },

  createModel: async (modelData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/models`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(modelData),
      });

      if (response.ok) {
        const newModel = await response.json();
        set((state) => ({
          models: [...state.models, newModel],
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create model');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to create model',
        isLoading: false,
      });
    }
  },

  updateModel: async (id, modelData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/models/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(modelData),
      });

      if (response.ok) {
        const updatedModel = await response.json();
        set((state) => ({
          models: state.models.map((m) => (m.id === id ? updatedModel : m)),
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to update model');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to update model',
        isLoading: false,
      });
    }
  },

  deleteModel: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/models/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        set((state) => ({
          models: state.models.filter((m) => m.id !== id),
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete model');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to delete model',
        isLoading: false,
      });
    }
  },

  fetchModelRuns: async (modelId) => {
    set({ isLoading: true, error: null });
    try {
      const url = modelId ? `${API_BASE}/model-runs?model_id=${modelId}` : `${API_BASE}/model-runs`;
      const response = await fetch(url);
      if (response.ok) {
        const modelRunsData = await response.json();
        set({
          modelRuns: modelRunsData,
          isLoading: false,
          error: null,
        });
      } else {
        throw new Error('Failed to fetch model runs');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch model runs',
        isLoading: false,
      });
    }
  },

  runModel: async (modelId, params = {}) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/models/${modelId}/run`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ params }),
      });

      if (response.ok) {
        const modelRun = await response.json();
        set((state) => ({
          modelRuns: [modelRun, ...state.modelRuns],
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to run model');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to run model',
        isLoading: false,
      });
    }
  },

  setCurrentForecast: (forecast) => {
    set({ currentForecast: forecast });
  },

  clearError: () => {
    set({ error: null });
  },
}));