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
  login: buildEndpoint('/auth/login'),
  register: buildEndpoint('/auth/register'),
  me: buildEndpoint('/auth/me'),

  // Business endpoints
  registerBusiness: buildEndpoint('/auth/business/register'),
  getBusinesses: buildEndpoint('/businesses/'),
  getBusinessById: (id: number) => buildEndpoint(`/businesses/${id}`),
  updateBusiness: (id: number) => buildEndpoint(`/businesses/${id}`),

  // Profile endpoints
  profile: buildEndpoint('/profile/'),
  changePassword: buildEndpoint('/profile/change-password'),
};

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
}

export interface ApiError {
  error?: string;
  message?: string;
  status: number;
}

export const apiRequest = async (
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> => {
  // Build headers explicitly to ensure Content-Type is always set correctly
  const headers: HeadersInit = {
    ...options.headers,  // User headers first
    'Content-Type': 'application/json', // This will ensure it's always set to application/json
  };

  const response = await fetch(endpoint, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const apiError: ApiError = {
      error: errorData.error || errorData.message,
      status: response.status,
    };
    throw apiError;
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

// Business API functions
export interface RegisterBusinessData {
  name: string;
  currency: string;
  owner_id: number;
}

export interface Business {
  id: number;
  name: string;
  currency: string;
  owner_id: number;
  timezone: string;
  city?: string | null;
  country?: string | null;
  settings?: Record<string, any> | null;
  created_at: string;
}

export interface UpdateBusinessData {
  name?: string;
  description?: string;
  settings?: Record<string, any>;
}

export const registerBusiness = async (data: RegisterBusinessData): Promise<Business> => {
  const response = await authenticatedRequest(API_ENDPOINTS.registerBusiness, {
    method: 'POST',
    body: JSON.stringify(data),
  });
  return response.json();
};

export const getBusinesses = async (): Promise<Business[]> => {
  const response = await authenticatedRequest(API_ENDPOINTS.getBusinesses);
  return response.json();
};

export const getBusinessById = async (id: number): Promise<Business> => {
  const response = await authenticatedRequest(API_ENDPOINTS.getBusinessById(id));
  return response.json();
};

export const updateBusiness = async (id: number, data: UpdateBusinessData): Promise<Business> => {
  const response = await authenticatedRequest(API_ENDPOINTS.updateBusiness(id), {
    method: 'PUT',
    body: JSON.stringify(data),
  });
  return response.json();
};