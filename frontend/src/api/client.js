const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

function extractErrorMessage(payload, fallback = "API request failed") {
  if (!payload) return fallback;
  if (typeof payload === "string") return payload;
  if (payload.detail) return payload.detail;

  const firstKey = Object.keys(payload)[0];
  if (!firstKey) return fallback;
  const firstValue = payload[firstKey];
  if (Array.isArray(firstValue) && firstValue.length) return String(firstValue[0]);
  if (typeof firstValue === "string") return firstValue;
  return fallback;
}

export async function apiRequest(path, options = {}) {
  const token = localStorage.getItem("access_token");
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  const contentType = response.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const payload = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    throw new Error(extractErrorMessage(payload));
  }

  return payload;
}

export async function login(username, password) {
  return apiRequest("/auth/login/", {
    method: "POST",
    body: JSON.stringify({ username: username.trim(), password }),
  });
}

export async function signup(payload) {
  return apiRequest("/auth/signup/", {
    method: "POST",
    body: JSON.stringify({
      ...payload,
      username: payload.username.trim(),
      email: payload.email.trim().toLowerCase(),
    }),
  });
}
