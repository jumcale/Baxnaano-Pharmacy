import { useEffect, useMemo } from "react";
import { ArrowTrendingUpIcon, BanknotesIcon, BellAlertIcon, CubeIcon } from "@heroicons/react/24/outline";
import { useQuery } from "@tanstack/react-query";
import { ResponsiveContainer, AreaChart, Area, Tooltip, XAxis, YAxis, CartesianGrid } from "recharts";

import AlertList from "../components/AlertList";
import StatCard from "../components/StatCard";
import { useAuthGuard } from "../hooks/useAuthGuard";
import { useAlertsStore } from "../store/useAlertsStore";
import { useInventoryStore } from "../store/useInventoryStore";
import { useSalesStore } from "../store/useSalesStore";
import { apiClient } from "../utils/apiClient";

type DashboardMetrics = {
  total_sales: number;
  total_revenue: number;
  weekly_sales: number;
  monthly_sales: number;
  low_stock_count: number;
  recent_alerts: any[];
  top_medicines: { medicine__name: string; total_quantity: number }[];
};

const Dashboard = () => {
  useAuthGuard();
  const { fetchAlerts } = useAlertsStore();
  const { fetchInventory } = useInventoryStore();
  const { fetchSummary } = useSalesStore();

  useEffect(() => {
    fetchAlerts();
    fetchInventory();
    fetchSummary();
  }, [fetchAlerts, fetchInventory, fetchSummary]);

  const { data: metrics } = useQuery<DashboardMetrics>({
    queryKey: ["dashboard-metrics"],
    queryFn: async () => {
      const response = await apiClient.get("/reports/dashboard/");
      return response.data;
    },
  });

  const chartData = useMemo(() => {
    if (!metrics) return [];
    return metrics.top_medicines.map((item, index) => ({
      name: item.medicine__name,
      value: item.total_quantity,
    }));
  }, [metrics]);

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Sales Invoices"
          value={metrics?.total_sales ?? "-"}
          icon={<CubeIcon className="h-6 w-6" />}
          trend="All-time invoices recorded in the system."
        />
        <StatCard
          title="Total Revenue"
          value={`$${metrics?.total_revenue?.toLocaleString() ?? "0"}`}
          icon={<BanknotesIcon className="h-6 w-6" />}
          trend={`Monthly: $${metrics?.monthly_sales ?? "0"}`}
          variant="success"
        />
        <StatCard
          title="Weekly Sales"
          value={`$${metrics?.weekly_sales ?? "0"}`}
          icon={<ArrowTrendingUpIcon className="h-6 w-6" />}
          trend="Revenue generated in the past 7 days."
        />
        <StatCard
          title="Low Stock Items"
          value={metrics?.low_stock_count ?? 0}
          icon={<BellAlertIcon className="h-6 w-6" />}
          trend="Products below reorder level."
          variant="danger"
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-950 lg:col-span-2">
          <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Top Selling Medicines</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">Based on sales quantities.</p>
          <div className="mt-6 h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2BB7B3" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#2BB7B3" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#33415522" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip />
                <Area type="monotone" dataKey="value" stroke="#0f766e" fillOpacity={1} fill="url(#colorValue)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-950">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Alerts</h2>
            <span className="rounded-full bg-rose-100 px-3 py-1 text-xs font-semibold text-rose-600 dark:bg-rose-900/30 dark:text-rose-100">
              Live
            </span>
          </div>
          <AlertList />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
