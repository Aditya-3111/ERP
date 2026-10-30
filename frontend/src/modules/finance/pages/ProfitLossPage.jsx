import Alert from '../../../components/ui/Alert.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import ReportShell from './ReportShell.jsx';
import { GroupList, TotalRow } from './reportParts.jsx';

export default function ProfitLossPage() {
  return (
    <ReportShell title="Profit & Loss" subtitle="Trading account and profit & loss account" endpoint="/finance/reports/profit-loss/">
      {(r) => (
        <div className="space-y-5">
          <div className="grid gap-5 lg:grid-cols-2">
            <Card title="Trading account - Income (Sales)" bodyClassName="p-0">
              <GroupList groups={r.trading.income} />
              <TotalRow label="Total income" amount={r.trading.total_income} />
            </Card>
            <Card title="Trading account - Expenses (Purchases)" bodyClassName="p-0">
              <GroupList groups={r.trading.expense} />
              <TotalRow label="Total expenses" amount={r.trading.total_expense} />
            </Card>
          </div>
          <TotalRow label="Gross profit" amount={r.gross_profit} tone={r.gross_profit >= 0 ? 'green' : 'red'} />
          <div className="grid gap-5 lg:grid-cols-2">
            <Card title="Other income" bodyClassName="p-0">
              <GroupList groups={r.profit_loss.income} />
              <TotalRow label="Total other income" amount={r.profit_loss.total_income} />
            </Card>
            <Card title="Indirect expenses" bodyClassName="p-0">
              <GroupList groups={r.profit_loss.expense} />
              <TotalRow label="Total indirect expenses" amount={r.profit_loss.total_expense} />
            </Card>
          </div>
          <div data-testid="net-profit"><TotalRow label={r.net_profit >= 0 ? 'Net profit' : 'Net loss'} amount={r.net_profit} tone={r.net_profit >= 0 ? 'green' : 'red'} /></div>
          <Alert tone="info">{r.note}</Alert>
        </div>
      )}
    </ReportShell>
  );
}
