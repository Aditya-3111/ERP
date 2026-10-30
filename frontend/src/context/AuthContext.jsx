import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { api, tokens } from '../api/client.js';

const AuthContext = createContext(null);

/**
 * Knows who is logged in.
 *   const { user, login, logout, loading } = useAuth();
 * On page load it asks the server "who am I?" if a token is stored.
 */
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(tokens.access));

  useEffect(() => {
    if (!tokens.access) return;
    api.get('/auth/profile/')
      .then(setUser)
      .catch(() => tokens.clear())
      .finally(() => setLoading(false));
  }, []);

  // api/client.js fires this event when the token is dead and cannot be refreshed
  useEffect(() => {
    const onLogout = () => setUser(null);
    window.addEventListener('fl:logout', onLogout);
    return () => window.removeEventListener('fl:logout', onLogout);
  }, []);

  const login = useCallback(async (username, password) => {
    const data = await api.post('/auth/login/', { username, password }, { auth: false });
    tokens.set(data.access, data.refresh);
    setUser(data.user);
    return data.user;
  }, []);

  const logout = useCallback(async () => {
    try {
      if (tokens.refresh) await api.post('/auth/logout/', { refresh: tokens.refresh });
    } catch { /* the token is cleared below anyway */ }
    tokens.clear();
    setUser(null);
  }, []);

  const value = useMemo(() => ({ user, setUser, login, logout, loading }), [user, login, logout, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
