import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Business, getBusinesses } from '@/lib/api';
import { useAuthStore } from '@/stores/auth-store';
import { getSelectedBusinessId, setSelectedBusinessId } from '@/utils/businessUtils';

interface BusinessContextType {
  businesses: Business[];
  currentBusiness: Business | null;
  setCurrentBusiness: (business: Business) => void;
  loading: boolean;
  refreshBusinesses: () => Promise<void>;
  addBusiness: (business: Business) => void;
  updateBusinessInContext: (business: Business) => void;
}

const BusinessContext = createContext<BusinessContextType | undefined>(undefined);

export const BusinessProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [currentBusiness, setCurrentBusiness] = useState<Business | null>(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuthStore();

  // Refresh businesses from API
  const refreshBusinesses = async () => {
    if (!user) {
      setBusinesses([]);
      setCurrentBusiness(null);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      const fetchedBusinesses = await getBusinesses();
      setBusinesses(fetchedBusinesses);

      // Try to restore the previously selected business
      const selectedBusinessId = getSelectedBusinessId();
      if (selectedBusinessId) {
        const savedBusiness = fetchedBusinesses.find(b => b.id === selectedBusinessId);
        if (savedBusiness) {
          setCurrentBusiness(savedBusiness);
          return;
        }
      }

      // If no saved business or it doesn't exist, set first business if available
      if (fetchedBusinesses.length > 0 && !currentBusiness) {
        setCurrentBusiness(fetchedBusinesses[0]);
      }
    } catch (error) {
      console.error('Error fetching businesses:', error);
      setBusinesses([]);
      setCurrentBusiness(null);
    } finally {
      setLoading(false);
    }
  };

  // Handle business change and persist to localStorage
  const handleSetCurrentBusiness = (business: Business) => {
    setCurrentBusiness(business);
    setSelectedBusinessId(business.id);
  };

  // Add a business to the context
  const addBusiness = (business: Business) => {
    setBusinesses(prev => {
      // Check if business already exists to avoid duplicates
      const exists = prev.some(b => b.id === business.id);
      if (!exists) {
        return [...prev, business];
      }
      return prev;
    });
    // Set the new business as current
    setCurrentBusiness(business);
    setSelectedBusinessId(business.id);
  };

  // Update a business in the context
  const updateBusinessInContext = (updatedBusiness: Business) => {
    setBusinesses(prev =>
      prev.map(b => b.id === updatedBusiness.id ? updatedBusiness : b)
    );

    // If this is the current business, update it too
    if (currentBusiness && currentBusiness.id === updatedBusiness.id) {
      setCurrentBusiness(updatedBusiness);
      setSelectedBusinessId(updatedBusiness.id);
    }
  };

  // Fetch businesses when user changes
  useEffect(() => {
    refreshBusinesses();
  }, [user?.id]);

  // Update context value to use the new handler
  const value = {
    businesses,
    currentBusiness,
    setCurrentBusiness: handleSetCurrentBusiness,
    loading,
    refreshBusinesses,
    addBusiness,
    updateBusinessInContext,
  };

  return (
    <BusinessContext.Provider value={value}>
      {children}
    </BusinessContext.Provider>
  );
};

export const useBusiness = () => {
  const context = useContext(BusinessContext);
  if (context === undefined) {
    throw new Error('useBusiness must be used within a BusinessProvider');
  }
  return context;
};