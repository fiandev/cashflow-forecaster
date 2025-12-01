import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AuthStore, Business } from './auth-types';
import { API_ENDPOINTS, apiRequest, authenticatedRequest } from '@/lib/api';
import { setCookie, eraseCookie, getCookie } from '@/lib/cookies';

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, password: string, rememberMe: boolean = false) => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiRequest(API_ENDPOINTS.login, {
            method: 'POST',
            body: JSON.stringify({ email, password }),
          });

          if (response.status !== 200) {
            throw new Error('Login failed');
          }

          const data = await response.json();

          // The API returns both token and user data
          const userData = data.user;

          // Store the token in localStorage for API calls
          localStorage.setItem('auth_token', data.token);

          // If rememberMe is true, also store the token in a cookie
          if (rememberMe) {
            setCookie('auth_token', data.token, 30); // 30 days
          } else {
            eraseCookie('auth_token');
          }

          set({
            user: userData,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Login failed',
            isLoading: false,
          });
        }
      },

      logout: () => {
        // Remove the auth token from localStorage and cookies
        localStorage.removeItem('auth_token');
        eraseCookie('auth_token');
        set({
          user: null,
          isAuthenticated: false,
          error: null,
        });
      },

      register: async (userData) => {
        set({ isLoading: true, error: null });
        try {
          // Register the user first
          const registerResponse = await apiRequest(API_ENDPOINTS.register, {
            method: 'POST',
            body: JSON.stringify(userData),
          });

          // After successful registration, there might be a brief delay before the user
          // can log in, so we'll try logging in with some error handling
          // Wait a bit for the registration to be processed by the backend
          await new Promise(resolve => setTimeout(resolve, 500));

          if (registerResponse.status !== 201) {
            throw new Error('Registration failed');
          }

          // Attempt to log the user in to get the authentication token
          const loginResponse = await apiRequest(API_ENDPOINTS.login, {
            method: 'POST',
            body: JSON.stringify({
              email: userData.email,
              password: userData.password
            }),
          });

          if (loginResponse.status !== 200) {
            throw new Error('Login failed');
          }

          const loginData = await loginResponse.json();

          // Store the token in localStorage for API calls
          localStorage.setItem('auth_token', loginData.token);

          set({
            user: loginData.user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Registration failed',
            isLoading: false,
          });
          // Re-throw to allow calling component to handle appropriately
          throw error;
        }
      },

      registerBusiness: async (businessData: any) => {
        const { user } = get();
        if (!user) {
          throw new Error('User not authenticated');
        }

        set({ isLoading: true, error: null });
        try {
          const response = await authenticatedRequest(API_ENDPOINTS.registerBusiness, {
            method: 'POST',
            body: JSON.stringify({
              ...businessData,
              owner_id: user.id
            }),
          });

          if (!response.ok) {
            throw new Error('Business registration failed');
          }

          const newBusiness = await response.json();

          // Update the user with the new business
          if (get().user) {
            const updatedUser = {
              ...get().user!,
              // Add business to user's businesses - we need to fetch the updated profile
              // For now, just update the state with the business data
            };
            set({
              user: updatedUser,
              isLoading: false,
              error: null,
            });
          }
          return newBusiness;
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Business registration failed',
            isLoading: false,
          });
          throw error;
        }
      },

      updateProfile: async (userData) => {
        const { user } = get();
        if (!user) return;

        set({ isLoading: true, error: null });
        try {
          const response = await authenticatedRequest(API_ENDPOINTS.profile, {
            method: 'PUT',
            body: JSON.stringify(userData),
          });

          if (!response.ok) {
            throw new Error('Update failed');
          }

          const updatedUser = await response.json();

          set({
            user: updatedUser,
            isLoading: false,
            error: null,
          });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Update failed',
            isLoading: false,
          });
        }
      },

      checkAuth: async () => {
        let token = localStorage.getItem('auth_token');

        // If no token in localStorage, check for cookie token
        if (!token) {
          token = getCookie('auth_token');
          if (token) {
            // If found in cookies, also store it in localStorage for API calls
            localStorage.setItem('auth_token', token);
          }
        }

        if (!token) {
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
          });
          return;
        }

        set({ isLoading: true, error: null });
        try {
          // Use the 'Get Current User' endpoint from Postman: /api/auth/me
          const response = await authenticatedRequest(API_ENDPOINTS.me);

          if (!response.ok) {
            throw new Error('Auth check failed');
          }

          const userData = await response.json();

          set({
            user: userData,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error) {
          localStorage.removeItem('auth_token');
          eraseCookie('auth_token');
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