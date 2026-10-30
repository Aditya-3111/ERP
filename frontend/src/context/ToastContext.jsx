import { createContext, useCallback, useContext, useMemo, useRef, useState } from 'react';

const ToastContext = createContext(null);
const TONE = { success: 'bg-emerald-600', error: 'bg-red-600', info: 'bg-slate-800' };

/** Small pop-up messages.  const toast = useToast();  toast.success('Saved');  toast.error(err.message) */
export function ToastProvider({ children }) {
  const [items, setItems] = useState([]);
  const nextId = useRef(1);

  const push = useCallback((tone, message) => {
    const id = nextId.current++;
    setItems((list) => [...list, { id, tone, message }]);
    setTimeout(() => setItems((list) => list.filter((t) => t.id !== id)), 4000);
  }, []);

  const api = useMemo(() => ({
    success: (m) => push('success', m),
    error: (m) => push('error', m),
    info: (m) => push('info', m),
  }), [push]);

  return (
    <ToastContext.Provider value={api}>
      {children}
      <div className="fixed right-4 top-4 z-[60] flex w-80 flex-col gap-2" aria-live="polite">
        {items.map((t) => (
          <div key={t.id} role="status" className={`rounded-lg px-4 py-3 text-sm text-white shadow-lg ${TONE[t.tone]}`}>{t.message}</div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export const useToast = () => useContext(ToastContext);
