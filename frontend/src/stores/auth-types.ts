export interface User {
  id: number;
  email: string;
  password?: string;
  name?: string;
  role?: string;
  created_at?: string;
  last_login?: string;
}

export interface Business {
  id: number;
  name: string;
  currency: string;
  owner_id: number;
  created_at: string;
  city?: string | null;
  country?: string | null;
  settings?: string | null;
  timezone?: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface AuthActions {
  login: (email: string, password: string, rememberMe?: boolean) => Promise<void>;
  logout: () => void;
  register: (userData: Omit<User, 'id' | 'created_at' | 'last_login' | 'role'>) => Promise<void>;
  registerBusiness: (businessData: Omit<Business, 'id' | 'owner_id' | 'created_at'>) => Promise<Business | undefined>;
  updateProfile: (userData: Partial<User>) => Promise<void>;
  checkAuth: () => Promise<void>;
  clearError: () => void;
}

export type AuthStore = AuthState & AuthActions;