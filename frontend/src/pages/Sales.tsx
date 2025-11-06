import { useEffect } from "react";

import { useAuthGuard } from "../hooks/useAuthGuard";
import { useSalesStore } from "../store/useSalesStore";

const Sales = () => {
  useAuthGuard();
  const { summary, fetchSummary, loading } = useSalesStore();

  useEffect(() => {
    fetchSummary();
  }, [fetchSummary]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-800 dark:text-slate-100">Point of Sale</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Create invoices, process payments, and manage transactions.
          </p>
        </div>
        <button className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white shadow hover:bg-primary-dark dark:bg-primary-light dark:text-slate-900">
          New Sale
        </button>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-950">
          <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Invoice Builder</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Scan medicines via barcode, adjust quantity, and apply discounts.
          </p>
          <div className="mt-4 rounded-xl border border-dashed border-slate-300 p-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
            POS interface placeholder. Integrate barcode reader and AI-powered demand predictions here.
          </div>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-950">
          <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Recent Performance</h2>
          {loading ? (
            <p className="mt-3 text-sm text-slate-500 dark:text-slate-400">Loading summary...</p>
          ) : summary ? (
            <ul className="mt-3 space-y-2 text-sm text-slate-600 dark:text-slate-300">
              <li>Total invoices (last {summary.days} days): {summary.total_sales}</li>
              <li>Total revenue: ${summary.total_revenue}</li>
            </ul>
          ) : (
            <p className="mt-3 text-sm text-slate-500 dark:text-slate-400">No sales data available.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Sales;
