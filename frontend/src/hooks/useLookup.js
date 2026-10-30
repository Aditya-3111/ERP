import { useEffect, useState } from 'react';
import { loadLookup } from '../api/lookups.js';

/** Options for a drop-down:  const { options, loading } = useLookup('employees');  -> [{value,label}] */
export default function useLookup(name) {
  const [state, setState] = useState({ options: [], loading: Boolean(name), error: null });
  useEffect(() => {
    if (!name) return undefined;
    let alive = true;
    loadLookup(name)
      .then((options) => alive && setState({ options, loading: false, error: null }))
      .catch((error) => alive && setState({ options: [], loading: false, error }));
    return () => { alive = false; };
  }, [name]);
  return state;
}
