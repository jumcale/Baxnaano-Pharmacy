import { create } from "zustand";
import { devtools } from "zustand/middleware";

import { apiClient } from "../utils/apiClient";

export type SalesSummary = {
  total_sales: number;
  total_revenue: string;
  days: number;
};

type SalesState = {
  summary: SalesSummary | null;
  loading: boolean;
  fetchSummary: (days?: number) => Promise<void>;
};

export const useSalesStore = create<SalesState>()(
  devtools((set) => ({
    summary: null,
    loading: false,
    fetchSummary: async (days = 7) => {
      set({ loading: true });
      try {
        const response = await apiClient.get(`/sales/summary/?days=${days}`);
        set({ summary: response.data, loading: false });
      } catch (error) {
        console.error("Failed to load sales summary", error);
        set({ loading: false });
      }
    },
  })),
);
