import { useEffect } from 'react';
import Icon from './Icon.jsx';

const WIDTH = { md: 'max-w-lg', lg: 'max-w-3xl', xl: 'max-w-5xl' };

/** Centered dialog. Closes with the X button or the Esc key. */
export default function Modal({ title, onClose, children, footer, size = 'lg' }) {
  useEffect(() => {
    const onKey = (e) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-slate-900/50 p-4 sm:p-8" role="dialog" aria-modal="true" aria-label={title}>
      <div className={`card w-full ${WIDTH[size] || WIDTH.lg}`}>
        <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
          <button type="button" onClick={onClose} className="rounded-lg p-1 text-slate-500 hover:bg-slate-100" aria-label="Close">
            <Icon name="close" />
          </button>
        </div>
        <div className="px-5 py-4">{children}</div>
        {footer && <div className="flex justify-end gap-2 border-t border-slate-200 bg-slate-50 px-5 py-3">{footer}</div>}
      </div>
    </div>
  );
}
