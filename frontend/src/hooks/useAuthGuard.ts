import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { useAuthStore } from "../store/useAuthStore";
import { isTokenExpired } from "../utils/auth";

export const useAuthGuard = () => {
  const { accessToken, logout, isAuthenticated } = useAuthStore((state) => ({
    accessToken: state.accessToken,
    logout: state.logout,
    isAuthenticated: state.isAuthenticated,
  }));
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (!isAuthenticated || isTokenExpired(accessToken)) {
      logout();
      if (location.pathname !== "/login") {
        navigate("/login", { replace: true });
      }
    }
  }, [accessToken, isAuthenticated, location.pathname, logout, navigate]);
};
