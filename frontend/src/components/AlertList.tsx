import { BellAlertIcon } from "@heroicons/react/24/outline";

import { useAlertsStore } from "../store/useAlertsStore";

const AlertList = () => {
  const { alerts } = useAlertsStore();

  if (!alerts.length) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 bg-white p-6 text-center dark:border-slate-700 dark:bg-slate-900">
        <p className="text-sm text-slate-500 dark:text-slate-400">No active alerts. Inventory looks healthy!</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {alerts.map((alert) => (
        <div
          key={alert.id}
          className="flex items-start gap-3 rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800 dark:border-rose-900/40 dark:bg-rose-900/20 dark:text-rose-100"
        >
          <BellAlertIcon className="mt-1 h-5 w-5 shrink-0" />
          <div>
            <p className="font-semibold">{alert.title}</p>
            <p className="text-xs opacity-80">{alert.message}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default AlertList;
