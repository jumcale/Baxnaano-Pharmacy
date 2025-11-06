import { Fragment } from "react";
import { NavLink } from "react-router-dom";
import {
  ChartBarIcon,
  ClipboardDocumentListIcon,
  CubeIcon,
  DocumentTextIcon,
  HomeIcon,
  ShoppingBagIcon,
} from "@heroicons/react/24/outline";
import clsx from "clsx";

import logo from "../assets/logo.svg";

const navigation = [
  { name: "Dashboard", to: "/dashboard", icon: HomeIcon },
  { name: "Inventory", to: "/inventory", icon: CubeIcon },
  { name: "Sales", to: "/sales", icon: ShoppingBagIcon },
  { name: "Reports", to: "/reports", icon: ChartBarIcon },
  { name: "Alerts", to: "/reports", icon: ClipboardDocumentListIcon, disabled: true },
  { name: "Documents", to: "/reports", icon: DocumentTextIcon, disabled: true },
];

const Sidebar = () => (
  <aside className="hidden w-64 flex-shrink-0 border-r border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950 md:flex md:flex-col">
    <div className="flex items-center gap-3 px-6 py-6">
      <img src={logo} alt="Baxnaano Pharmacy" className="h-10 w-10" />
      <span className="text-lg font-semibold text-slate-800 dark:text-slate-100">Baxnaano Pharmacy</span>
    </div>
    <nav className="flex-1 space-y-1 px-4">
      {navigation.map((item) => {
        const Icon = item.icon;
        if (item.disabled) {
          return (
            <div
              key={item.name}
              className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-400 dark:text-slate-600"
            >
              <Icon className="h-5 w-5" />
              <span>{item.name} (soon)</span>
            </div>
          );
        }
        return (
          <NavLink
            key={item.name}
            to={item.to}
            className={({ isActive }) =>
              clsx(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary/10 text-primary-dark dark:bg-primary/20 dark:text-primary-light"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-900",
              )
            }
          >
            <Icon className="h-5 w-5" aria-hidden="true" />
            <span>{item.name}</span>
          </NavLink>
        );
      })}
    </nav>
    <div className="px-6 pb-6">
      <div className="rounded-lg bg-primary/10 p-4 text-sm text-primary-dark dark:bg-primary/20 dark:text-primary-light">
        <p className="font-semibold">AI Forecast</p>
        <p className="text-xs text-primary-dark/80 dark:text-primary-light/80">
          Inventory predictions powered by the Baxnaano AI Engine.
        </p>
      </div>
    </div>
  </aside>
);

export default Sidebar;
