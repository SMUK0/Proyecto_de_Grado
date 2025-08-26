// src/services/api.js
export const API_BASE = "http://127.0.0.1:8000/api";

export async function fetchHomeInfo() {
  const res = await fetch(`${API_BASE}/home/`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
