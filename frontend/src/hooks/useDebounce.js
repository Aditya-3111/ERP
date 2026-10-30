import { useEffect, useState } from 'react';

/** Waits until the user stops typing for `delay` ms (so we do not call the API on every key). */
export default function useDebounce(value, delay = 350) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return debounced;
}
