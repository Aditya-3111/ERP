// Address of the Django API.  Change it in frontend/.env (VITE_API_URL), then restart `npm run dev`.
export const API_URL =
  (import.meta.env && import.meta.env.VITE_API_URL) || 'http://localhost:8000/api';
