import { create } from "zustand";
import { devtools } from "zustand/middleware";

import { apiClient } from "../utils/apiClient";

export type Supplier = {
  id: number;
  name: string;
  contact_person?: string;
  email?: string;
  phone_number?: string;
};

export type Batch = {
  id: number;
  batch_number: string;
  expiry_date: string;
  quantity: number;
  is_expired: boolean;
};

export type Medicine = {
  id: number;
  name: string;
  sku: string;
  category: string;
  total_stock: number;
  reorder_level: number;
  supplier?: Supplier | number;
  batches: Batch[];
};

type InventoryState = {
  medicines: Medicine[];
  suppliers: Supplier[];
  nearExpiryBatches: Batch[];
  loading: boolean;
  fetchInventory: () => Promise<void>;
  fetchSuppliers: () => Promise<void>;
};

export const useInventoryStore = create<InventoryState>()(
  devtools((set) => ({
    medicines: [],
    suppliers: [],
    nearExpiryBatches: [],
    loading: false,
    fetchInventory: async () => {
      set({ loading: true });
      try {
        const [medicinesResponse, nearExpiryResponse] = await Promise.all([
          apiClient.get("/inventory/medicines/"),
          apiClient.get("/inventory/medicines/near_expiry/"),
        ]);
        const medicines = medicinesResponse.data.results ?? medicinesResponse.data;
        const nearExpiryBatches = nearExpiryResponse.data.results ?? nearExpiryResponse.data;
        set({ medicines, nearExpiryBatches, loading: false });
      } catch (error) {
        console.error("Failed to load inventory", error);
        set({ loading: false });
      }
    },
    fetchSuppliers: async () => {
      try {
        const response = await apiClient.get("/inventory/suppliers/");
        const suppliers = response.data.results ?? response.data;
        set({ suppliers });
      } catch (error) {
        console.error("Failed to load suppliers", error);
      }
    },
  })),
);
