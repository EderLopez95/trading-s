const API = process.env.REACT_APP_API_URL;
const BASE = `${API}/api`;

const request = async (endpoint, options = {}) => {
  const res = await fetch(`${BASE}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });
  const data = await res.json();
  if (!res.ok) {
    throw {
      message: data.message || "Unknown error",
      status: res.status
    };
  }
  return data;
};

export const getStatus = () => request("/status");

export const startBot = () =>
  request("/start", {
    method: "POST"
  });

export const stopBot = () =>
  request("/stop", {
    method: "POST"
  });

export const getConfig = () => request("/config");

export const saveConfig = (config) =>
  request("/config", {
    method: "POST",
    body: JSON.stringify(config)
  });

export const getSymbols = async (query = "") => {
  if (!query) return [];
  return request(`/symbols/search?query=${query}`);
};
