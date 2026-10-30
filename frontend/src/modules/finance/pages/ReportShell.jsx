import { useState } from 'react';
import { api } from '../../../api/client.js';
import Alert from '../../../components/ui/Alert.jsx';
import Button from '../../../components/ui/Button.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import PageHeader from '../../../components/ui/PageHeader.jsx';
import Spinner from '../../../components/ui/Spinner.jsx';
import { usePeriod } from '../../../context/PeriodContext.jsx';
import useFetch from '../../../hooks/useFetch.js';

/**
 * Common frame of the three reports: date range on top, report below.
 *   <ReportShell title="Trial Balance" endpoint="/finance/reports/trial-balance/">{(data) => <table/>}</ReportShell>
 * The dates start with the selected financial year.
 */
export default function ReportShell({ title, subtitle, endpoint, children }) {
  const { period } = usePeriod();
  const [range, setRange] = useState({ from: period.from, to: period.to });
  const [applied, setApplied] = useState(range);
  const { data, loading, error, reload } = useFetch(() => api.get(endpoint, applied), [endpoint, applied.from, applied.to]);

  return (
    <>
      <PageHeader title={title} subtitle={subtitle}>
        <Button variant="secondary" onClick={() => window.print()}>Print</Button>
      </PageHeader>
      <Card className="mb-5 print:hidden">
        <form className="flex flex-wrap items-end gap-3" onSubmit={(e) => { e.preventDefault(); setApplied(range); }}>
          <div><label className="label" htmlFor="rep-from">From</label>
            <input id="rep-from" type="date" className="input" value={range.from} onChange={(e) => setRange({ ...range, from: e.target.value })} /></div>
          <div><label className="label" htmlFor="rep-to">To</label>
            <input id="rep-to" type="date" className="input" value={range.to} onChange={(e) => setRange({ ...range, to: e.target.value })} /></div>
          <Button type="submit" icon="refresh">Show report</Button>
        </form>
      </Card>
      {loading && <Spinner />}
      {error && <Alert onRetry={reload}>{error.message}</Alert>}
      {!loading && !error && data && children(data)}
    </>
  );
}
