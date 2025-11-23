import { create } from 'zustand';
import { AlertStore, Alert } from './alert-types';

const API_BASE = '/api';

export const useAlertStore = create<AlertStore>((set, get) => ({
  alerts: [],
  riskScores: [],
  unreadCount: 0,
  isLoading: false,
  error: null,
  filters: {},

  fetchAlerts: async (businessId) => {
    set({ isLoading: true, error: null });
    try {
      const params = new URLSearchParams();
      if (businessId) params.append('business_id', businessId.toString());
      Object.entries(get().filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });

      const response = await fetch(`${API_BASE}/alerts?${params}`);
      if (response.ok) {
        const alertsData = await response.json();
        const unreadCount = alertsData.filter((alert: Alert) => !alert.resolved).length;
        set({
          alerts: alertsData,
          unreadCount,
          isLoading: false,
          error: null,
        });
      } else {
        throw new Error('Failed to fetch alerts');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch alerts',
        isLoading: false,
      });
    }
  },

  createAlert: async (alertData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/alerts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(alertData),
      });

      if (response.ok) {
        const newAlert = await response.json();
        set((state) => ({
          alerts: [newAlert, ...state.alerts],
          unreadCount: !newAlert.resolved ? state.unreadCount + 1 : state.unreadCount,
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create alert');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to create alert',
        isLoading: false,
      });
    }
  },

  updateAlert: async (id, alertData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/alerts/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(alertData),
      });

      if (response.ok) {
        const updatedAlert = await response.json();
        set((state) => {
          const oldAlert = state.alerts.find(a => a.id === id);
          const unreadCountChange = oldAlert && !oldAlert.resolved && updatedAlert.resolved ? -1 : 
                                   oldAlert && oldAlert.resolved && !updatedAlert.resolved ? 1 : 0;
          
          return {
            alerts: state.alerts.map((a) => (a.id === id ? updatedAlert : a)),
            unreadCount: state.unreadCount + unreadCountChange,
            isLoading: false,
            error: null,
          };
        });
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to update alert');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to update alert',
        isLoading: false,
      });
    }
  },

  resolveAlert: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/alerts/${id}/resolve`, {
        method: 'POST',
      });

      if (response.ok) {
        set((state) => ({
          alerts: state.alerts.map((a) => 
            a.id === id ? { ...a, resolved: true, resolved_at: new Date().toISOString() } : a
          ),
          unreadCount: Math.max(0, state.unreadCount - 1),
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to resolve alert');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to resolve alert',
        isLoading: false,
      });
    }
  },

  deleteAlert: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/alerts/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        set((state) => {
          const alertToDelete = state.alerts.find(a => a.id === id);
          const unreadCountChange = alertToDelete && !alertToDelete.resolved ? -1 : 0;
          
          return {
            alerts: state.alerts.filter((a) => a.id !== id),
            unreadCount: Math.max(0, state.unreadCount + unreadCountChange),
            isLoading: false,
            error: null,
          };
        });
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete alert');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to delete alert',
        isLoading: false,
      });
    }
  },

  fetchRiskScores: async (businessId) => {
    set({ isLoading: true, error: null });
    try {
      const url = businessId ? `${API_BASE}/risk-scores?business_id=${businessId}` : `${API_BASE}/risk-scores`;
      const response = await fetch(url);
      if (response.ok) {
        const riskScoresData = await response.json();
        set({
          riskScores: riskScoresData,
          isLoading: false,
          error: null,
        });
      } else {
        throw new Error('Failed to fetch risk scores');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch risk scores',
        isLoading: false,
      });
    }
  },

  createRiskScore: async (riskData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/risk-scores`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(riskData),
      });

      if (response.ok) {
        const newRiskScore = await response.json();
        set((state) => ({
          riskScores: [newRiskScore, ...state.riskScores],
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create risk score');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to create risk score',
        isLoading: false,
      });
    }
  },

  setFilters: (newFilters) => {
    set((state) => ({
      filters: { ...state.filters, ...newFilters },
    }));
  },

  clearFilters: () => {
    set({ filters: {} });
  },

  clearError: () => {
    set({ error: null });
  },
}));