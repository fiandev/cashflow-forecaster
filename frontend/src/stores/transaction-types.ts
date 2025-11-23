export interface Transaction {
  id: number;
  business_id: number;
  date: string;
  datetime?: string;
  description?: string;
  amount: number;
  direction: 'in' | 'out';
  category_id?: number;
  source?: string;
  ocr_document_id?: number;
  tags?: Record<string, any>;
  is_anomalous?: boolean;
  ai_tag?: string;
  created_at?: string;
  updated_at?: string;
}

export interface TransactionFilters {
  business_id?: number;
  category_id?: number;
  direction?: 'in' | 'out';
  date_from?: string;
  date_to?: string;
  search?: string;
  is_anomalous?: boolean;
}

export interface TransactionState {
  transactions: Transaction[];
  filteredTransactions: Transaction[];
  isLoading: boolean;
  error: string | null;
  filters: TransactionFilters;
  pagination: {
    page: number;
    limit: number;
    total: number;
  };
}

export interface TransactionActions {
  fetchTransactions: (businessId: number, filters?: TransactionFilters) => Promise<void>;
  createTransaction: (transactionData: Omit<Transaction, 'id' | 'created_at' | 'updated_at'>) => Promise<void>;
  updateTransaction: (id: number, transactionData: Partial<Transaction>) => Promise<void>;
  deleteTransaction: (id: number) => Promise<void>;
  setFilters: (filters: Partial<TransactionFilters>) => void;
  clearFilters: () => void;
  setPage: (page: number) => void;
  setLimit: (limit: number) => void;
  clearError: () => void;
}

export type TransactionStore = TransactionState & TransactionActions;