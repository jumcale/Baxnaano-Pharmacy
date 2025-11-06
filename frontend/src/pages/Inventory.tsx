import { useEffect } from "react";

import { useAuthGuard } from "../hooks/useAuthGuard";
import { useInventoryStore } from "../store/useInventoryStore";

const Inventory = () => {
  useAuthGuard();
  const { medicines, nearExpiryBatches, fetchInventory, loading } = useInventoryStore();

  useEffect(() => {
    fetchInventory();
  }, [fetchInventory]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-800 dark:text-slate-100">Inventory</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Manage medicines, batches, and supplier information.
          </p>
        </div>
        <button className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white shadow hover:bg-primary-dark dark:bg-primary-light dark:text-slate-900">
          Add Medicine
        </button>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-950">
            <div className="border-b border-slate-200 p-4 dark:border-slate-800">
              <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Medicine Catalogue</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200 text-sm dark:divide-slate-800">
                <thead className="bg-slate-50 dark:bg-slate-900/40">
                  <tr>
                    <th className="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">Name</th>
                    <th className="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">SKU</th>
                    <th className="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">Category</th>
                    <th className="px-4 py-3 text-right font-semibold text-slate-600 dark:text-slate-300">
                      Stock / Reorder
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
                  {loading ? (
                    <tr>
                      <td colSpan={4} className="px-4 py-6 text-center text-slate-500 dark:text-slate-400">
                        Loading inventory...
                      </td>
                    </tr>
                  ) : medicines.length === 0 ? (
                    <tr>
                      <td colSpan={4} className="px-4 py-6 text-center text-slate-500 dark:text-slate-400">
                        No medicines found.
                      </td>
                    </tr>
                  ) : (
                    medicines.map((medicine) => (
                      <tr key={medicine.id} className="hover:bg-slate-50 dark:hover:bg-slate-900/40">
                        <td className="px-4 py-3 text-slate-800 dark:text-slate-100">{medicine.name}</td>
                        <td className="px-4 py-3 text-slate-600 dark:text-slate-300">{medicine.sku}</td>
                        <td className="px-4 py-3 capitalize text-slate-600 dark:text-slate-300">
                          {medicine.category}
                        </td>
                        <td className="px-4 py-3 text-right text-slate-600 dark:text-slate-300">
                          {medicine.total_stock} / {medicine.reorder_level}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-950">
          <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Near Expiry Batches</h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">Batches expiring within the next 30 days.</p>
          <div className="mt-4 space-y-3">
            {nearExpiryBatches.length === 0 ? (
              <p className="text-sm text-slate-500 dark:text-slate-400">No batches near expiry.</p>
            ) : (
              nearExpiryBatches.map((batch) => (
                <div
                  key={batch.id}
                  className="rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800 dark:border-amber-900/30 dark:bg-amber-900/20 dark:text-amber-100"
                >
                  <p className="font-semibold">{batch.batch_number}</p>
                  <p className="text-xs">
                    Qty: {batch.quantity} • Expiry: {batch.expiry_date}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Inventory;
