import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AuthStore } from './auth-types';

const API_BASE = '/api/users';

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
          });

          if (response.ok) {
            const userData = await response.json();
            set({
              user: userData,
              isAuthenticated: true,
              isLoading: false,
              error: null,
            });
          } else {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Login failed');
          }
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Login failed',
            isLoading: false,
          });
        }
      },

      logout: () => {
        set({
          user: null,
          isAuthenticated: false,
          error: null,
        });
      },

      register: async (userData) => {
        set({ isLoading: true, error: null });
        try {
          const response = await fetch(API_BASE, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
          });

          if (response.ok) {
            const newUser = await response.json();
            set({
              user: newUser,
              isAuthenticated: true,
              isLoading: false,
              error: null,
            });
          } else {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Registration failed');
          }
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Registration failed',
            isLoading: false,
          });
        }
      },

      updateProfile: async (userData) => {
        const { user } = get();
        if (!user) return;

        set({ isLoading: true, error: null });
        try {
          const response = await fetch(`${API_BASE}/${user.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
          });

          if (response.ok) {
            const updatedUser = await response.json();
            set({
              user: updatedUser,
              isLoading: false,
              error: null,
            });
          } else {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Update failed');
          }
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Update failed',
            isLoading: false,
          });
        }
      },

      checkAuth: async () => {
        const { user } = get();
        if (!user) return;

        set({ isLoading: true, error: null });
        try {
          const response = await fetch(`${API_BASE}/${user.id}`);
          
          if (response.ok) {
            const userData = await response.json();
            set({
              user: userData,
              isAuthenticated: true,
              isLoading: false,
              error: null,
            });
          } else {
            set({
              user: null,
              isAuthenticated: false,
              isLoading: false,
            });
          }
        } catch (error) {
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: error instanceof Error ? error.message : 'Auth check failed',
          });
        }
      },

      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);