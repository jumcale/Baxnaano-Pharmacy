import { useNavigate } from "react-router-dom";
import { Bars3Icon, MoonIcon, SunIcon } from "@heroicons/react/24/outline";

import { useAuthStore } from "../store/useAuthStore";
import { useTheme } from "../hooks/useTheme";

const Topbar = () => {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4 dark:border-slate-800 dark:bg-slate-950">
      <div className="flex items-center gap-3">
        <button className="rounded-lg p-2 hover:bg-slate-100 dark:hover:bg-slate-900 md:hidden">
          <Bars3Icon className="h-5 w-5 text-slate-700 dark:text-slate-200" />
        </button>
        <div>
          <h1 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Baxnaano Pharmacy</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">Arabsiyo, Somaliland</p>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <button
          onClick={toggleTheme}
          className="rounded-full border border-slate-200 p-2 text-slate-700 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-900"
          aria-label="Toggle dark mode"
        >
          {theme === "dark" ? <SunIcon className="h-5 w-5" /> : <MoonIcon className="h-5 w-5" />}
        </button>
        <div className="hidden flex-col text-right text-sm md:flex">
          <span className="font-medium text-slate-700 dark:text-slate-200">{user?.fullName ?? "Guest"}</span>
          <span className="text-xs uppercase tracking-wide text-primary-dark dark:text-primary-light">
            {user?.role ?? "Staff"}
          </span>
        </div>
        <button
          onClick={handleLogout}
          className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-primary-dark dark:bg-primary-light dark:text-slate-900"
        >
          Logout
        </button>
      </div>
    </header>
  );
};

export default Topbar;
