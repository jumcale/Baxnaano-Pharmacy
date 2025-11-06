import { useEffect, useState } from "react";
import { ArrowDownTrayIcon, DocumentChartBarIcon } from "@heroicons/react/24/outline";

import { useAuthGuard } from "../hooks/useAuthGuard";
import { apiClient } from "../utils/apiClient";

type DashboardMetrics = {
  total_sales: number;
  total_revenue: number;
  weekly_sales: number;
  monthly_sales: number;
  low_stock_count: number;
};

const Reports = () => {
  useAuthGuard();
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const response = await apiClient.get("/reports/dashboard/");
        setMetrics(response.data);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-800 dark:text-slate-100">Reports & Analytics</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Gain insights with sales, inventory, and alerts dashboards.
          </p>
        </div>
        <div className="flex gap-3">
          <button className="flex items-center gap-2 rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-900">
            <ArrowDownTrayIcon className="h-4 w-4" />
            Export PDF
          </button>
          <button className="flex items-center gap-2 rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-900">
            <ArrowDownTrayIcon className="h-4 w-4" />
            Export Excel
          </button>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-950">
        <div className="flex items-center gap-3">
          <DocumentChartBarIcon className="h-6 w-6 text-primary-dark" />
          <div>
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Executive Summary</h2>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              Automatically generated recap of sales and inventory performance.
            </p>
          </div>
        </div>
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {loading ? (
            <p className="text-sm text-slate-500 dark:text-slate-400">Loading metrics...</p>
          ) : metrics ? (
            <>
              <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
                <p className="text-xs uppercase text-slate-500 dark:text-slate-400">Total Sales</p>
                <p className="text-2xl font-semibold text-slate-800 dark:text-slate-100">{metrics.total_sales}</p>
              </div>
              <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
                <p className="text-xs uppercase text-slate-500 dark:text-slate-400">Total Revenue</p>
                <p className="text-2xl font-semibold text-slate-800 dark:text-slate-100">
                  ${metrics.total_revenue?.toLocaleString()}
                </p>
              </div>
              <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
                <p className="text-xs uppercase text-slate-500 dark:text-slate-400">Weekly Sales</p>
                <p className="text-2xl font-semibold text-slate-800 dark:text-slate-100">${metrics.weekly_sales}</p>
              </div>
              <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
                <p className="text-xs uppercase text-slate-500 dark:text-slate-400">Monthly Sales</p>
                <p className="text-2xl font-semibold text-slate-800 dark:text-slate-100">${metrics.monthly_sales}</p>
              </div>
              <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
                <p className="text-xs uppercase text-slate-500 dark:text-slate-400">Low Stock Items</p>
                <p className="text-2xl font-semibold text-slate-800 dark:text-slate-100">{metrics.low_stock_count}</p>
              </div>
            </>
          ) : (
            <p className="text-sm text-slate-500 dark:text-slate-400">No report data yet.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Reports;
