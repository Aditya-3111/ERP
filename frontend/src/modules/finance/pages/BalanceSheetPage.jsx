import Alert from '../../../components/ui/Alert.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import { formatMoney } from '../../../utils/format.js';
import ReportShell from './ReportShell.jsx';
import { GroupList, TotalRow } from './reportParts.jsx';

export default function BalanceSheetPage() {
  return (
    <ReportShell title="Balance Sheet" subtitle="Assets and liabilities as on the 'To' date" endpoint="/finance/reports/balance-sheet/">
      {(r) => (
        <div className="space-y-5">
          <div className="grid gap-5 lg:grid-cols-2">
            <Card title="Liabilities" bodyClassName="p-0">
              <GroupList groups={r.liabilities} />
              <TotalRow label="Total liabilities" amount={r.total_liabilities} />
            </Card>
            <Card title="Assets" bodyClassName="p-0">
              <GroupList groups={r.assets} />
              <TotalRow label="Total assets" amount={r.total_assets} />
            </Card>
          </div>
          {r.difference === 0
            ? <div data-testid="bs-state"><Alert tone="success">Balance sheet is balanced.</Alert></div>
            : <div data-testid="bs-state"><Alert tone="warning">Difference in opening balances: {formatMoney(Math.abs(r.difference))} (assets {r.difference > 0 ? 'exceed' : 'are less than'} liabilities).</Alert></div>}
        </div>
      )}
    </ReportShell>
  );
}
