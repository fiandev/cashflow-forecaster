import { useEffect } from 'react';
import { useAuthStore } from '@/stores/auth-store';

export const AuthInitializer: React.FC = () => {
  const { checkAuth, isAuthenticated } = useAuthStore();

  useEffect(() => {
    // Check authentication status on app load
    // In a real app, this would check for stored auth tokens
    checkAuth();
  }, [checkAuth]);

  // For demo purposes, you can uncomment this to auto-login
  // Remove this in production
  useEffect(() => {
    if (!isAuthenticated) {
      // Auto-login with demo user for development
      const demoUser = {
        id: 1,
        email: 'demo@example.com',
        name: 'Demo User',
        role: 'admin',
        created_at: new Date().toISOString(),
        last_login: new Date().toISOString(),
      };
      
      // Uncomment the next two lines for auto-login
      // useAuthStore.setState({ user: demoUser, isAuthenticated: true });
      // console.log('Demo user logged in for development');
    }
  }, [isAuthenticated]);

  return null;
};