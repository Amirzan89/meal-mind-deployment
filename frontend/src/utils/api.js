// src/utils/api.js
import axios from "axios";

// Gunakan URL relatif karena kita menggunakan proxy Vite
const API_BASE_URL = "";

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.log("API Error:", {
      url: error.config?.url,
      status: error.response?.status,
      data: error.response?.data,
      headers: error.config?.headers,
    });

    // Handle 401 unauthorized errors
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  signup: (data) => api.post("/api/auth/signup", data),
  login: (data) => api.post("/api/auth/login", data),
  getCurrentUser: () => api.get("/api/auth/me"),
  testCors: () => api.get("/api/cors-test"),
};

// Profile API
export const profileAPI = {
  setup: (data) => api.post("/api/profile/setup", data),
  get: () => api.get("/api/profile/get"),
  update: (data) => api.put("/api/profile/update", data),
};

// Recommendations API
export const recommendationsAPI = {
  getToday: () => api.get("/api/recommendations/today"),
  regenerate: (type) => api.post(`/api/recommendations/regenerate/${type}`),
  checkin: (data) => api.post("/api/recommendations/checkin", data),
  getHistory: () => api.get("/api/recommendations/history"),
};

export default api;
