import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { api, rowsOf } from '../api/client.js';
import { useAuth } from './AuthContext.jsx';
import { todayISO } from '../utils/format.js';

const PeriodContext = createContext(null);
const KEY = 'fl_financial_year';

/**
 * The financial year chosen in the top bar. Dashboard, vouchers and reports
 * use  period.from / period.to  as their default date range.
 */
export function PeriodProvider({ children }) {
  const { user } = useAuth();
  const [years, setYears] = useState([]);
  const [selected, setSelected] = useState(localStorage.getItem(KEY));

  useEffect(() => {
    if (!user) return;
    api.get('/core/financial-years/', { page_size: 50, ordering: '-start_date' })
      .then((data) => setYears(rowsOf(data)))
      .catch(() => setYears([]));
  }, [user]);

  const current = useMemo(() => {
    const year = years.find((y) => y.guid === selected) || years.find((y) => y.is_active) || years[0];
    if (!year) {   // no financial year defined yet: use April-March around today
      const t = todayISO();
      const startYear = Number(t.slice(5, 7)) >= 4 ? Number(t.slice(0, 4)) : Number(t.slice(0, 4)) - 1;
      return { guid: null, name: `FY ${startYear}-${String(startYear + 1).slice(2)}`, from: `${startYear}-04-01`, to: `${startYear + 1}-03-31` };
    }
    return { guid: year.guid, name: year.name, from: year.start_date, to: year.end_date };
  }, [years, selected]);

  const value = useMemo(() => ({
    years, period: current,
    selectYear: (guid) => { localStorage.setItem(KEY, guid); setSelected(guid); },
  }), [years, current]);

  return <PeriodContext.Provider value={value}>{children}</PeriodContext.Provider>;
}

export const usePeriod = () => useContext(PeriodContext);
