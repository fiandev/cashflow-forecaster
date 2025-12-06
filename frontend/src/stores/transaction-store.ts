import { create } from 'zustand';
import { TransactionStore } from './transaction-types';

const API_BASE = '/api/transactions';

export const useTransactionStore = create<TransactionStore>((set, get) => ({
  transactions: [],
  filteredTransactions: [],
  isLoading: false,
  error: null,
  filters: {},
  pagination: {
    page: 1,
    limit: 50,
    total: 0,
  },

  fetchTransactions: async (businessId, filters = {}) => {
    set({ isLoading: true, error: null });
    try {
      const params = new URLSearchParams();
      params.append('business_id', businessId.toString());
      params.append('page', get().pagination.page.toString());
      params.append('limit', get().pagination.limit.toString());
      
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });

      const response = await fetch(`${API_BASE}?${params}`);
      if (response.ok) {
        const data = await response.json();
        set({
          transactions: data.transactions || data,
          filteredTransactions: data.transactions || data,
          pagination: {
            ...get().pagination,
            total: data.total || data.length,
          },
          isLoading: false,
          error: null,
        });
      } else {
        throw new Error('Failed to fetch transactions');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch transactions',
        isLoading: false,
      });
    }
  },

  createTransaction: async (transactionData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(API_BASE, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(transactionData),
      });

      if (response.ok) {
        const newTransaction = await response.json();
        set((state) => ({
          transactions: [newTransaction, ...state.transactions],
          filteredTransactions: [newTransaction, ...state.filteredTransactions],
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create transaction');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to create transaction',
        isLoading: false,
      });
    }
  },

  updateTransaction: async (id, transactionData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(transactionData),
      });

      if (response.ok) {
        const updatedTransaction = await response.json();
        set((state) => ({
          transactions: state.transactions.map((t) => (t.id === id ? updatedTransaction : t)),
          filteredTransactions: state.filteredTransactions.map((t) => (t.id === id ? updatedTransaction : t)),
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to update transaction');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to update transaction',
        isLoading: false,
      });
    }
  },

  deleteTransaction: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        set((state) => ({
          transactions: state.transactions.filter((t) => t.id !== id),
          filteredTransactions: state.filteredTransactions.filter((t) => t.id !== id),
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete transaction');
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to delete transaction',
        isLoading: false,
      });
    }
  },

  setFilters: (newFilters) => {
    const updatedFilters = { ...get().filters, ...newFilters };
    set({ filters: updatedFilters });
    
    const { transactions } = get();
    let filtered = transactions;

    if (updatedFilters.category_id) {
      filtered = filtered.filter((t) => t.category_id === updatedFilters.category_id);
    }
    if (updatedFilters.direction) {
      filtered = filtered.filter((t) => t.direction === updatedFilters.direction);
    }
    if (updatedFilters.date_from) {
      filtered = filtered.filter((t) => t.date >= updatedFilters.date_from);
    }
    if (updatedFilters.date_to) {
      filtered = filtered.filter((t) => t.date <= updatedFilters.date_to);
    }
    if (updatedFilters.search) {
      const searchLower = updatedFilters.search.toLowerCase();
      filtered = filtered.filter((t) => 
        t.description?.toLowerCase().includes(searchLower) ||
        t.source?.toLowerCase().includes(searchLower)
      );
    }
    if (updatedFilters.is_anomalous !== undefined) {
      filtered = filtered.filter((t) => t.is_anomalous === updatedFilters.is_anomalous);
    }

    set({ filteredTransactions: filtered });
  },

  clearFilters: () => {
    set({ 
      filters: {},
      filteredTransactions: get().transactions,
    });
  },

  setPage: (page) => {
    set((state) => ({
      pagination: { ...state.pagination, page },
    }));
  },

  setLimit: (limit) => {
    set((state) => ({
      pagination: { ...state.pagination, limit, page: 1 },
    }));
  },

  clearError: () => {
    set({ error: null });
  },
}));