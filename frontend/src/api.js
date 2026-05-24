const API_BASE = '/api/v1';

async function request(path, options = {}) {
  const token = localStorage.getItem('token');
  const headers = { ...options.headers };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 204) return null;

  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error(text || `HTTP ${res.status}: response is not JSON`);
  }

  if (!res.ok) {
    const detail = data.detail || data.message || `HTTP ${res.status}`;
    const msg = typeof detail === 'string' ? detail : detail[0]?.msg || `HTTP ${res.status}`;
    throw new Error(msg);
  }
  return data;
}

export async function login(username, password) {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  return request('/jwt/login', {
    method: 'POST',
    body: formData,
  });
}

export async function register(username, email, password) {
  return request('/jwt/register', {
    method: 'POST',
    body: JSON.stringify({ username, email, password }),
  });
}

export async function getMe() {
  return request('/jwt/users/me/');
}
