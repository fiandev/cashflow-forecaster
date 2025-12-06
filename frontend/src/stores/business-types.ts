export interface Business {
  id: number;
  owner_id: number;
  name: string;
  country?: string;
  city?: string;
  currency: string;
  timezone: string;
  created_at?: string;
  settings?: Record<string, any>;
}

export interface Category {
  id: number;
  business_id: number;
  name: string;
  type: 'income' | 'expense';
  parent_id?: number;
  created_at?: string;
  children?: Category[];
}

export interface BusinessState {
  businesses: Business[];
  currentBusiness: Business | null;
  categories: Category[];
  isLoading: boolean;
  error: string | null;
}

export interface BusinessActions {
  fetchBusinesses: () => Promise<void>;
  createBusiness: (businessData: Omit<Business, 'id' | 'owner_id' | 'created_at'>) => Promise<void>;
  updateBusiness: (id: number, businessData: Partial<Business>) => Promise<void>;
  deleteBusiness: (id: number) => Promise<void>;
  setCurrentBusiness: (business: Business | null) => void;
  fetchCategories: (businessId: number) => Promise<void>;
  createCategory: (categoryData: Omit<Category, 'id' | 'created_at'>) => Promise<void>;
  updateCategory: (id: number, categoryData: Partial<Category>) => Promise<void>;
  deleteCategory: (id: number) => Promise<void>;
  clearError: () => void;
}

export type BusinessStore = BusinessState & BusinessActions;