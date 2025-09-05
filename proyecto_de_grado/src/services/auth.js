// src/services/auth.js
const API = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api";

export async function login(identifier, password) {
  const res = await fetch(`${API}/auth/token/`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    // SimpleJWT por defecto usa "username". Puedes escribir tu email en ese campo también
    body: JSON.stringify({ username: identifier, password })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Credenciales inválidas");
  }
  const data = await res.json();
  localStorage.setItem("access", data.access);
  localStorage.setItem("refresh", data.refresh);
  return data;
}

export function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
}

export const getAccess = () => localStorage.getItem("access");
export const getRefresh = () => localStorage.getItem("refresh");

export async function refreshToken() {
  const refresh = getRefresh();
  if (!refresh) throw new Error("No refresh token");
  const res = await fetch(`${API}/auth/token/refresh/`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ refresh })
  });
  if (!res.ok) throw new Error("Refresh inválido");
  const data = await res.json();
  localStorage.setItem("access", data.access);
  return data.access;
}

export async function apiFetch(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  const access = getAccess();
  if (access) headers["Authorization"] = `Bearer ${access}`;

  let res = await fetch(`${API}${path}`, { ...options, headers });

  // Si expira el access, intenta refrescar 1 vez
  if (res.status === 401 && getRefresh()) {
    try {
      const newAccess = await refreshToken();
      headers["Authorization"] = `Bearer ${newAccess}`;
      res = await fetch(`${API}${path}`, { ...options, headers });
    } catch (e) { /* ignore */ }
  }

  return res;
}
