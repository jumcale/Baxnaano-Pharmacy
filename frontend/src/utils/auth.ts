import axios from "axios";
import jwtDecode from "jwt-decode";

import { API_BASE_URL } from "./apiClient";
import { useAuthStore } from "../store/useAuthStore";

type TokenPayload = {
  exp: number;
  email: string;
  role: string;
  user_id: number;
};

export const decodeToken = (token: string): TokenPayload => jwtDecode<TokenPayload>(token);

export const isTokenExpired = (token: string | null): boolean => {
  if (!token) return true;
  const payload = decodeToken(token);
  const now = Date.now() / 1000;
  return payload.exp < now;
};

export const refreshToken = async () => {
  const { refreshToken } = useAuthStore.getState();
  if (!refreshToken) {
    return null;
  }
  const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, { refresh: refreshToken });
  return response.data;
};
