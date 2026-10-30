import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * Load data when the page opens (and again when `deps` change).
 *   const { data, loading, error, reload } = useFetch(() => api.get('/hr/employees/'), []);
 */
export default function useFetch(loader, deps = []) {
  const [state, setState] = useState({ data: null, loading: true, error: null });
  const loaderRef = useRef(loader);
  loaderRef.current = loader;
  const counter = useRef(0);

  const run = useCallback(() => {
    const id = ++counter.current;                       // ignore answers of outdated requests
    setState((s) => ({ ...s, loading: true, error: null }));
    loaderRef.current()
      .then((data) => id === counter.current && setState({ data, loading: false, error: null }))
      .catch((error) => id === counter.current && setState({ data: null, loading: false, error }));
  }, []);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { run(); }, deps);
  return { ...state, reload: run };
}
