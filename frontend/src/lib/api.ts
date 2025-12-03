// Extract API base URL from environment variable or use relative paths to avoid CORS
// Using environment variable if provided, otherwise relative paths to same origin
const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

// Helper function to construct API endpoints
const buildEndpoint = (path: string): string => {
  if (API_BASE && !API_BASE.startsWith('/')) {
    // If API_BASE is an absolute URL (e.g., http://localhost:5000)
    return `${API_BASE}${path}`;
  } else if (API_BASE) {
    // If API_BASE is a relative path or root
    return `${API_BASE}${path}`;
  }
  // Default to relative paths to avoid CORS issues
  return path;
};

// Define API endpoints
export const API_ENDPOINTS = {
  // Auth endpoints
  login: buildEndpoint('/api/auth/login'),
  register: buildEndpoint('/api/auth/register'),
  me: buildEndpoint('/api/auth/me'),

  // Business endpoints
  registerBusiness: buildEndpoint('/api/auth/business/register'),

  // Profile endpoints
  profile: buildEndpoint('/api/profile/'),
  changePassword: buildEndpoint('/api/profile/change-password'),

  // Forecast endpoints
  forecasts: buildEndpoint('/api/forecasts/'),

  // Alert endpoints
  alerts: buildEndpoint('/api/alerts/'),

  // Transaction endpoints
  transactions: buildEndpoint('/api/transactions/'),

  // Category endpoints
  categories: buildEndpoint('/api/categories/'),

  // Dashboard endpoints
  dashboardMetrics: buildEndpoint('/api/dashboard/metrics'),
};

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
}

export const apiRequest = async (
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> => {
  // Build headers explicitly to ensure Content-Type is always set correctly
  const headers: HeadersInit = {
    ...options.headers,  // User headers first
    'Content-Type': 'application/json', // This will ensure it's always set to application/json
    'ngrok-skip-browser-warning': 'true', // Bypass ngrok browser warning for free accounts
  };

  const response = await fetch(endpoint, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
  }

  return response
};

export const authenticatedRequest = async <T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> => {
  const token = localStorage.getItem('auth_token');

  if (!token) {
    throw new Error('Authentication token not found');
  }

  // Merge headers properly, ensuring Content-Type is preserved
  const mergedHeaders = {
    ...options.headers,
    'Authorization': `Bearer ${token}`,
  };

  return apiRequest(endpoint, {
    ...options,
    headers: mergedHeaders,
  });
};