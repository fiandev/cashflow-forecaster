// Utility functions for business-related data persistence
const BUSINESS_STORAGE_KEY = 'selected_business_id';

// Get the selected business ID from localStorage
export const getSelectedBusinessId = (): number | null => {
  const businessId = localStorage.getItem(BUSINESS_STORAGE_KEY);
  return businessId ? parseInt(businessId, 10) : null;
};

// Set the selected business ID in localStorage
export const setSelectedBusinessId = (businessId: number | null): void => {
  if (businessId !== null) {
    localStorage.setItem(BUSINESS_STORAGE_KEY, businessId.toString());
  } else {
    localStorage.removeItem(BUSINESS_STORAGE_KEY);
  }
};

// Clear the selected business ID from localStorage
export const clearSelectedBusinessId = (): void => {
  localStorage.removeItem(BUSINESS_STORAGE_KEY);
};