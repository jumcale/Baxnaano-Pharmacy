import { create } from "zustand";
import { persist } from "zustand/middleware";

import { decodeToken } from "../utils/auth";
import { login as loginService } from "../services/authService";

type Role = "admin" | "pharmacist" | "staff";

export type AuthUser = {
  id: number;
  email: string;
  role: Role;
  fullName: string;
};

type AuthState = {
  accessToken: string | null;
  refreshToken: string | null;
  user: AuthUser | null;
  isAuthenticated: boolean;
  login: (payload: { email: string; password: string }) => Promise<void>;
  logout: () => void;
  setTokens: (tokens: { access: string; refresh: string }) => void;
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      accessToken: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
      login: async ({ email, password }) => {
        const response = await loginService({ email, password });
        const { access, refresh, user } = response.data;
        set({
          accessToken: access,
          refreshToken: refresh,
          user: {
            id: user.id,
            email: user.email,
            role: user.role,
            fullName: `${user.first_name ?? ""} ${user.last_name ?? ""}`.trim() || user.email,
          },
          isAuthenticated: true,
        });
      },
      logout: () => {
        set({
          accessToken: null,
          refreshToken: null,
          user: null,
          isAuthenticated: false,
        });
      },
      setTokens: ({ access, refresh }) => {
        const payload = decodeToken(access);
        set({
          accessToken: access,
          refreshToken: refresh,
          isAuthenticated: true,
          user: {
            id: payload.user_id,
            email: payload.email,
            role: payload.role,
            fullName: payload.email,
          },
        });
      },
    }),
    {
      name: "baxnaano-auth",
      partialize: (state) => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    },
  ),
);
