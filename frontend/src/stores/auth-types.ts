export interface User {
  id: number;
  email: string;
  password_hash?: string;
  name?: string;
  role?: string;
  created_at?: string;
  last_login?: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface AuthActions {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (userData: Omit<User, 'id' | 'created_at' | 'last_login'>) => Promise<void>;
  updateProfile: (userData: Partial<User>) => Promise<void>;
  checkAuth: () => Promise<void>;
  clearError: () => void;
}

export type AuthStore = AuthState & AuthActions;