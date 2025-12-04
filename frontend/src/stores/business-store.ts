import { create } from "zustand";
import { BusinessStore } from "./business-types";
import { API_ENDPOINTS, apiRequest, authenticatedRequest } from "@/lib/api";

export const useBusinessStore = create<BusinessStore>((set) => ({
  businesses: [],
  currentBusiness: null,
  categories: [],
  isLoading: false,
  error: null,

  fetchBusinesses: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await authenticatedRequest(API_ENDPOINTS.getAllBusinesses, {});
      if (response.ok) {
        const businessesData = await response.json();
        set({
          businesses: businessesData,
          isLoading: false,
          error: null,
        });
      } else {
        throw new Error("Failed to fetch businesses");
      }
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to fetch businesses",
        isLoading: false,
      });
    }
  },

  createBusiness: async (businessData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authenticatedRequest(API_ENDPOINTS.createBusiness, {
        method: "POST",
        body: JSON.stringify(businessData),
      });

      if (response.ok) {
        const newBusiness = await response.json();
        set((state) => ({
          businesses: [...state.businesses, newBusiness],
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to create business");
      }
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to create business",
        isLoading: false,
      });
    }
  },

  updateBusiness: async (id, businessData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authenticatedRequest(
        `${API_ENDPOINTS.getAllBusinesses}/${id}`,
        {
          method: "PUT",
          body: JSON.stringify(businessData),
        },
      );

      if (response.ok) {
        const updatedBusiness = await response.json();
        set((state) => ({
          businesses: state.businesses.map((b) =>
            b.id === id ? updatedBusiness : b,
          ),
          currentBusiness:
            state.currentBusiness?.id === id
              ? updatedBusiness
              : state.currentBusiness,
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to update business");
      }
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to update business",
        isLoading: false,
      });
    }
  },

  deleteBusiness: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authenticatedRequest(
        `${API_ENDPOINTS.getAllBusinesses}/${id}`,
        {
          method: "DELETE",
        },
      );

      if (response.ok) {
        set((state) => ({
          businesses: state.businesses.filter((b) => b.id !== id),
          currentBusiness:
            state.currentBusiness?.id === id ? null : state.currentBusiness,
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to delete business");
      }
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to delete business",
        isLoading: false,
      });
    }
  },

  setCurrentBusiness: (business) => {
    set({ currentBusiness: business });
  },

  fetchCategories: async (businessId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authenticatedRequest(
        `${API_ENDPOINTS.categories}/${businessId}/categories`,
        {
          method: "GET",
        },
      );
      if (response.ok) {
        const categoriesData = await response.json();
        set({
          categories: categoriesData,
          isLoading: false,
          error: null,
        });
      } else {
        throw new Error("Failed to fetch categories");
      }
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to fetch categories",
        isLoading: false,
      });
    }
  },

  createCategory: async (categoryData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authenticatedRequest(`${API_ENDPOINTS.categories}`, {
        method: "POST",
        body: JSON.stringify(categoryData),
      });

      if (response.ok) {
        const newCategory = await response.json();
        set((state) => ({
          categories: [...state.categories, newCategory],
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to create category");
      }
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to create category",
        isLoading: false,
      });
    }
  },

  updateCategory: async (id, categoryData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authenticatedRequest(`${API_ENDPOINTS.categories}/${id}`, {
        method: "PUT",
        body: JSON.stringify(categoryData),
      });

      if (response.ok) {
        const updatedCategory = await response.json();
        set((state) => ({
          categories: state.categories.map((c) =>
            c.id === id ? updatedCategory : c,
          ),
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to update category");
      }
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to update category",
        isLoading: false,
      });
    }
  },

  deleteCategory: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authenticatedRequest(`${API_ENDPOINTS.categories}/${id}`, {
        method: "DELETE",
      });

      if (response.ok) {
        set((state) => ({
          categories: state.categories.filter((c) => c.id !== id),
          isLoading: false,
          error: null,
        }));
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to delete category");
      }
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to delete category",
        isLoading: false,
      });
    }
  },

  clearError: () => {
    set({ error: null });
  },
}));
