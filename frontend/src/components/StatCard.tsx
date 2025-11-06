import clsx from "clsx";
import { ReactNode } from "react";

type StatCardProps = {
  title: string;
  value: string | number;
  icon: ReactNode;
  trend?: string;
  variant?: "default" | "success" | "danger";
};

const variants = {
  default: "bg-white text-slate-800 dark:bg-slate-900 dark:text-slate-100",
  success: "bg-green-50 text-green-800 dark:bg-green-900/30 dark:text-green-100",
  danger: "bg-rose-50 text-rose-800 dark:bg-rose-900/30 dark:text-rose-100",
};

const StatCard = ({ title, value, icon, trend, variant = "default" }: StatCardProps) => (
  <div className={clsx("rounded-xl border border-slate-200 p-5 shadow-sm dark:border-slate-800", variants[variant])}>
    <div className="flex items-start justify-between">
      <div>
        <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</p>
        <p className="mt-2 text-2xl font-semibold">{value}</p>
      </div>
      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary-dark">
        {icon}
      </div>
    </div>
    {trend && <p className="mt-3 text-xs text-slate-500 dark:text-slate-400">{trend}</p>}
  </div>
);

export default StatCard;
