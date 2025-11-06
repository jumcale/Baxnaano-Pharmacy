import { create } from "zustand";
import { devtools } from "zustand/middleware";

import { apiClient } from "../utils/apiClient";

export type Alert = {
  id: number;
  title: string;
  message: string;
  alert_type: string;
  status: string;
};

type AlertsState = {
  alerts: Alert[];
  loading: boolean;
  fetchAlerts: () => Promise<void>;
};

export const useAlertsStore = create<AlertsState>()(
  devtools((set) => ({
    alerts: [],
    loading: false,
    fetchAlerts: async () => {
      set({ loading: true });
      try {
        const response = await apiClient.get("/alerts/");
        const alerts = response.data.results ?? response.data;
        set({ alerts, loading: false });
      } catch (error) {
        console.error("Failed to load alerts", error);
        set({ loading: false });
      }
    },
  })),
);
