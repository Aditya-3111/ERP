// ----------------------------------------------------------------------------
// The ONE place that talks to the Django API.
//   * adds the login token to every request
//   * when the token has expired it silently gets a new one (refresh token)
//   * turns Django's error replies into readable messages
// Every page uses:  api.get(url, params)  api.post(url, body)  api.patch  api.put  api.delete
// ----------------------------------------------------------------------------
import { API_URL } from '../config/env.js';

const ACCESS_KEY = 'fl_access';
const REFRESH_KEY = 'fl_refresh';

export const tokens = {
  get access() { return localStorage.getItem(ACCESS_KEY); },
  get refresh() { return localStorage.getItem(REFRESH_KEY); },
  set(access, refresh) {
    if (access) localStorage.setItem(ACCESS_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
  },
  clear() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
  },
};

/** Turn a Django error body into one readable line. */
export function messageFrom(data, status) {
  if (!data) return status ? `Request failed (HTTP ${status})` : 'Request failed';
  if (typeof data === 'string') return data.length > 200 ? `Server error (HTTP ${status})` : data;
  if (data.detail) return String(data.detail);
  if (data.error) return String(data.error);
  const parts = Object.entries(data).map(([field, msg]) => {
    const text = Array.isArray(msg) ? msg.join(' ') : typeof msg === 'object' ? JSON.stringify(msg) : String(msg);
    return field === 'non_field_errors' ? text : `${field}: ${text}`;
  });
  return parts.join(' | ') || `Request failed (HTTP ${status})`;
}

export class ApiError extends Error {
  constructor(status, data) {
    super(messageFrom(data, status));
    this.name = 'ApiError';
    this.status = status;
    this.data = data;          // for forms: { field_name: ['message'] }
  }
  /** Field-level errors only (used to show red text under each input). */
  get fieldErrors() {
    if (!this.data || typeof this.data !== 'object') return {};
    const out = {};
    for (const [k, v] of Object.entries(this.data)) {
      if (k !== 'detail' && k !== 'error') out[k] = Array.isArray(v) ? v.join(' ') : String(v);
    }
    return out;
  }
}

// ---- token refresh: several requests may fail together, but the refresh token can
// ---- be used only once (the server rotates it) -> everybody waits for ONE refresh call.
let refreshing = null;
function refreshAccess() {
  if (!refreshing) {
    refreshing = (async () => {
      const refresh = tokens.refresh;
      if (!refresh) return false;
      try {
        const res = await fetch(`${API_URL}/auth/refresh/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh }),
        });
        if (!res.ok) return false;
        const data = await res.json();
        tokens.set(data.access, data.refresh);
        return true;
      } catch {
        return false;
      }
    })().finally(() => { refreshing = null; });
  }
  return refreshing;
}

function buildUrl(path, params) {
  const url = new URL(API_URL + path);
  Object.entries(params || {}).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') url.searchParams.set(k, v);
  });
  return url.toString();
}

async function request(method, path, { params, body, auth = true, retry = true } = {}) {
  const headers = {};
  let payload;
  if (body instanceof FormData) payload = body;                  // file upload: browser sets the headers
  else if (body !== undefined) { headers['Content-Type'] = 'application/json'; payload = JSON.stringify(body); }
  if (auth && tokens.access) headers.Authorization = `Bearer ${tokens.access}`;

  let res;
  try {
    res = await fetch(buildUrl(path, params), { method, headers, body: payload });
  } catch {
    throw new ApiError(0, { detail: `Cannot reach the server at ${API_URL}. Is the backend running?` });
  }

  if (res.status === 401 && auth && retry && tokens.refresh && (await refreshAccess())) {
    return request(method, path, { params, body, auth, retry: false });
  }
  if (res.status === 401 && auth) {
    tokens.clear();
    window.dispatchEvent(new Event('fl:logout'));               // AuthContext sends the user to /login
  }

  let data = null;
  if (res.status !== 204) {
    const text = await res.text();
    try { data = text ? JSON.parse(text) : null; } catch { data = text; }
  }
  if (!res.ok) throw new ApiError(res.status, data);
  return data;
}

export const api = {
  get: (path, params) => request('GET', path, { params }),
  post: (path, body, opts) => request('POST', path, { body, ...opts }),
  put: (path, body) => request('PUT', path, { body }),
  patch: (path, body) => request('PATCH', path, { body }),
  delete: (path) => request('DELETE', path),
};

/** List endpoints return {count, results}; some small ones may return a plain array. */
export const rowsOf = (data) => (Array.isArray(data) ? data : data?.results || []);
