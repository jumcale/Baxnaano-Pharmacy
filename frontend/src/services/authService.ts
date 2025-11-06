import axios from "axios";

import { API_BASE_URL } from "../utils/apiClient";

export const login = async (payload: { email: string; password: string }) => {
  return axios.post(`${API_BASE_URL}/auth/login/`, payload);
};
