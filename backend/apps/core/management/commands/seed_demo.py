"""python manage.py seed_demo

Sample records so every screen has something to show: ledgers, vouchers,
stock items, customers, leads, employees, attendance, visitors, assets ...
Safe to run again - it never creates the same record twice.
Switch it off with SEED_DEMO_DATA=false in .env (or `setup_db --no-demo`).
"""
from datetime import date, datetime, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.core.models import FinancialYear
from apps.crm.models import Customer, Lead
from apps.finance.models import AccountingEntry, Ledger, Voucher
from apps.gate.models import Visitor
from apps.hr.models import Attendance, Department, Designation, Employee
from apps.inventory.models import Godown, StockGroup, StockItem
from apps.maintenance.models import Asset, AssetCategory, WorkOrder

D = Decimal


class Command(BaseCommand):
    help = 'Create sample records for every module (idempotent).'

    @transaction.atomic
    def handle(self, *args, **opts):
        today = timezone.localdate()
        self.finance(today)
        self.inventory()
        self.crm(today)
        self.hr(today)
        self.gate(today)
        self.maintenance(today)
        if opts.get('verbosity', 1) > 0:
            self.stdout.write(self.style.SUCCESS('Demo data ready.'))

    # ------------------------------------------------------------- finance
    def finance(self, today):
        ledgers = [
            # name, group, opening, dr/cr
            ('HDFC Bank', 'Bank Accounts', 300000, 'dr'),
            ('Capital Account - Owner', 'Capital Account', 300000, 'cr'),
            ('Sharma Traders', 'Sundry Debtors', 0, 'dr'),
            ('Verma Enterprises', 'Sundry Debtors', 0, 'dr'),
            ('Gupta Suppliers', 'Sundry Creditors', 0, 'cr'),
            ('Mehta Industries', 'Sundry Creditors', 0, 'cr'),
            ('Office Rent', 'Indirect Expenses', 0, 'dr'),
            ('Salaries', 'Indirect Expenses', 0, 'dr'),
        ]
        contact = {
            'Sharma Traders': ('Pune', 'Maharashtra', '27AAAPS1234A1Z5'),
            'Verma Enterprises': ('Indore', 'Madhya Pradesh', '23AAAPV5678B1Z2'),
            'Gupta Suppliers': ('Delhi', 'Delhi', '07AAAPG4321C1Z9'),
            'Mehta Industries': ('Surat', 'Gujarat', '24AAAPM8765D1Z1'),
        }
        for name, group, opening, typ in ledgers:
            city, state, gstin = contact.get(name, ('', '', ''))
            Ledger.objects.get_or_create(name=name, defaults={
                'parent': group, 'opening_balance': opening, 'opening_balance_type': typ,
                'is_deemed_positive': typ == 'dr', 'city': city, 'state': state, 'gstin': gstin})

        if Voucher.objects.filter(narration__startswith='Demo:').exists():
            return
        fy = FinancialYear.objects.filter(is_active=True).first()
        start = fy.start_date if fy else date(today.year if today.month >= 4 else today.year - 1, 4, 1)
        counters = {}

        def voucher(vtype, day, party, narration, lines):
            if day > today:
                return
            counters[vtype] = counters.get(vtype, 0) + 1
            prefix = ''.join(w[0] for w in vtype.split()).upper()
            prefix = prefix if len(prefix) > 1 else vtype[:3].upper()
            v = Voucher.objects.create(
                date=day, voucher_type=vtype, voucher_number=f'{prefix}/{counters[vtype]:04d}',
                party_name=party, narration='Demo: ' + narration, financial_year=fy,
                is_invoice=vtype in ('Sales', 'Purchase'))
            for ledger, amount, is_dr in lines:
                AccountingEntry.objects.create(voucher=v, ledger=ledger, amount=D(str(amount)), is_dr=is_dr)

        month = start
        i = 0
        while month <= today:
            def d(day):
                return month.replace(day=day)
            customer = 'Sharma Traders' if i % 2 == 0 else 'Verma Enterprises'
            supplier = 'Gupta Suppliers' if i % 2 == 0 else 'Mehta Industries'
            sale = D(220000 + i * 25000)
            sale_gst = (sale * D('0.18')).quantize(D('0.01'))
            buy = D(110000 + i * 10000)
            buy_gst = (buy * D('0.18')).quantize(D('0.01'))
            voucher('Sales', d(5), customer, f'Sale invoice {i + 1}',
                    [(customer, sale + sale_gst, True), ('Sales Account', sale, False), ('Output GST', sale_gst, False)])
            voucher('Purchase', d(9), supplier, f'Purchase bill {i + 1}',
                    [('Purchase Account', buy, True), ('Input GST', buy_gst, True), (supplier, buy + buy_gst, False)])
            voucher('Receipt', d(18), customer, 'Payment received',
                    [('HDFC Bank', (sale * D('0.6')).quantize(D('0.01')), True),
                     (customer, (sale * D('0.6')).quantize(D('0.01')), False)])
            voucher('Payment', d(21), supplier, 'Supplier payment',
                    [(supplier, (buy * D('0.5')).quantize(D('0.01')), True),
                     ('HDFC Bank', (buy * D('0.5')).quantize(D('0.01')), False)])
            voucher('Payment', d(25), 'Landlord', 'Monthly rent',
                    [('Office Rent', 25000, True), ('HDFC Bank', 25000, False)])
            voucher('Payment', d(28), 'Staff', 'Salary',
                    [('Salaries', 60000, True), ('HDFC Bank', 60000, False)])
            i += 1
            month = (month.replace(day=28) + timedelta(days=4)).replace(day=1)

    # ----------------------------------------------------------- inventory
    def inventory(self):
        for name in ('Raw Material', 'Finished Goods', 'Consumables'):
            StockGroup.objects.get_or_create(name=name)
        for name, city in (('Main Warehouse', 'Mumbai'), ('Retail Store', 'Pune'), ('Scrap Yard', 'Mumbai')):
            Godown.objects.get_or_create(name=name, defaults={'city': city, 'incharge': 'Store Keeper'})
        items = [
            # name, group, uom, qty, rate, min, hsn
            ('Steel Rod 12mm', 'Raw Material', 'Kg', 850, 72, 200, '7214'),
            ('Copper Wire 2.5mm', 'Raw Material', 'Mtr', 1200, 18, 300, '7408'),
            ('Industrial Bearing 6204', 'Raw Material', 'Nos', 140, 210, 50, '8482'),
            ('Hydraulic Oil 20L', 'Consumables', 'Ltr', 60, 145, 100, '2710'),
            ('Packing Box Large', 'Consumables', 'Box', 420, 28, 150, '4819'),
            ('Safety Gloves', 'Consumables', 'Pcs', 35, 55, 80, '4015'),
            ('Electric Motor 5HP', 'Finished Goods', 'Nos', 18, 9800, 5, '8501'),
            ('Welding Rod 3.15mm', 'Consumables', 'Kg', 300, 95, 100, '8311'),
        ]
        for name, group, uom, qty, rate, minimum, hsn in items:
            StockItem.objects.get_or_create(name=name, defaults={
                'parent': group, 'category': group, 'uom': uom, 'opening_balance': qty,
                'opening_rate': rate, 'opening_value': D(qty) * D(rate), 'closing_balance': qty,
                'closing_rate': rate, 'closing_value': D(qty) * D(rate), 'min_stock': minimum,
                'max_stock': minimum * 6, 'gst_rate': 18, 'gst_hsn_code': hsn,
                'costing_method': 'Average', 'default_godown': 'Main Warehouse'})

    # ----------------------------------------------------------------- crm
    def crm(self, today):
        customers = [
            ('Sharma Traders', 'customer', 'Rajesh Sharma', '9820011111', 'Pune'),
            ('Verma Enterprises', 'customer', 'Anil Verma', '9820022222', 'Indore'),
            ('Gupta Suppliers', 'supplier', 'Sunil Gupta', '9820033333', 'Delhi'),
            ('Mehta Industries', 'supplier', 'Kiran Mehta', '9820044444', 'Surat'),
            ('Singh & Sons', 'both', 'Harpreet Singh', '9820055555', 'Ludhiana'),
            ('Patel Engineering', 'customer', 'Mehul Patel', '9820066666', 'Ahmedabad'),
        ]
        for name, kind, person, mobile, city in customers:
            Customer.objects.get_or_create(name=name, defaults={
                'company': name, 'customer_type': kind, 'contact_person': person, 'mobile': mobile,
                'email': person.split()[0].lower() + '@example.com', 'city': city, 'status': 'active',
                'country': 'India', 'credit_limit': 100000, 'credit_period': 30})
        leads = [
            ('Bhatia Motors', 'Ravi Bhatia', 'new', 'high'), ('Kapoor Textiles', 'Neha Kapoor', 'contacted', 'medium'),
            ('Rao Foods', 'Suresh Rao', 'qualified', 'high'), ('Nair Plastics', 'Anita Nair', 'new', 'low'),
            ('Joshi Pumps', 'Vikas Joshi', 'converted', 'medium'), ('Khan Traders', 'Imran Khan', 'lost', 'low'),
        ]
        for n, (company, person, status, priority) in enumerate(leads):
            Lead.objects.get_or_create(company=company, defaults={
                'contact_person': person, 'mobile': f'98100{n:05d}', 'email': person.split()[0].lower() + '@example.com',
                'source': 'Website' if n % 2 else 'Referral', 'status': status, 'priority': priority,
                'assigned_to': 'Sales Team', 'follow_up_date': today + timedelta(days=n + 1)})

    # ------------------------------------------------------------------ hr
    def hr(self, today):
        depts = ['Accounts', 'Sales', 'Store', 'HR', 'Production', 'Security']
        dept_obj = {n: Department.objects.get_or_create(name=n)[0] for n in depts}
        for name, dept in (('Manager', 'Accounts'), ('Executive', 'Sales'), ('Store Keeper', 'Store'),
                           ('HR Officer', 'HR'), ('Supervisor', 'Production'), ('Guard', 'Security')):
            Designation.objects.get_or_create(name=name, department=dept_obj[dept])
        staff = [
            ('EMP001', 'Amit Kulkarni', 'Accounts', 'Manager', 'Male', 62000),
            ('EMP002', 'Priya Deshmukh', 'Sales', 'Executive', 'Female', 38000),
            ('EMP003', 'Rohit Jadhav', 'Store', 'Store Keeper', 'Male', 28000),
            ('EMP004', 'Sneha Patil', 'HR', 'HR Officer', 'Female', 42000),
            ('EMP005', 'Vijay More', 'Production', 'Supervisor', 'Male', 35000),
            ('EMP006', 'Kavita Shinde', 'Sales', 'Executive', 'Female', 36000),
            ('EMP007', 'Ganesh Pawar', 'Security', 'Guard', 'Male', 21000),
            ('EMP008', 'Meera Iyer', 'Accounts', 'Executive', 'Female', 40000),
        ]
        employees = []
        for code, name, dept, desig, gender, salary in staff:
            emp, _ = Employee.objects.get_or_create(emp_code=code, defaults={
                'name': name, 'department': dept, 'designation': desig, 'gender': gender, 'salary': salary,
                'status': 'active', 'date_of_joining': date(2023, 4, 1) + timedelta(days=30 * len(employees)),
                'mobile': f'97000{len(employees):05d}', 'city': 'Mumbai', 'state': 'Maharashtra'})
            employees.append(emp)
        # attendance for the last 10 days (skip Sundays)
        for back in range(10):
            day = today - timedelta(days=back)
            if day.weekday() == 6:
                continue
            for n, emp in enumerate(employees):
                status = 'Absent' if (n + back) % 11 == 0 else ('Half Day' if (n + back) % 13 == 0 else 'Present')
                Attendance.objects.get_or_create(employee=emp, date=day, defaults={
                    'status': status,
                    'in_time': time(9, 0 + (n * 3) % 40) if status != 'Absent' else None,
                    'out_time': time(18, 0) if status == 'Present' else None})

    # ---------------------------------------------------------------- gate
    def gate(self, today):
        visitors = [
            ('Deepak Rane', 'ABC Logistics', 'Delivery', 'Rohit Jadhav', 'checked_in'),
            ('Pooja Salvi', 'Tech Suppliers', 'Meeting', 'Amit Kulkarni', 'checked_in'),
            ('Sanjay Dixit', 'Audit Partners', 'Audit', 'Meera Iyer', 'checked_out'),
            ('Farida Shaikh', 'Job Applicant', 'Interview', 'Sneha Patil', 'checked_out'),
            ('Manoj Tiwari', 'City Couriers', 'Delivery', 'Rohit Jadhav', 'checked_out'),
        ]
        for n, (name, company, purpose, host, status) in enumerate(visitors, start=1):
            Visitor.objects.get_or_create(visitor_id=f'VIS-{today:%y%m%d}-{n:03d}', defaults={
                'name': name, 'company': company, 'mobile': f'96000{n:05d}', 'purpose': purpose,
                'host_employee': host, 'entry_date': today, 'entry_time': time(9 + n, 15),
                'exit_time': time(10 + n, 45) if status == 'checked_out' else None, 'status': status,
                'no_of_persons': 1})

    # --------------------------------------------------------- maintenance
    def maintenance(self, today):
        cat = {}
        for name, code in (('Machinery', 'MCH'), ('Vehicles', 'VEH'), ('IT Equipment', 'ITE')):
            cat[name], _ = AssetCategory.objects.get_or_create(
                category_code=code, defaults={'category_name': name, 'depreciation_rate': 10})
        assets = [
            ('AST-001', 'CNC Lathe Machine', 'Machinery', 'critical', 'active'),
            ('AST-002', 'Delivery Van MH-12', 'Vehicles', 'high', 'active'),
            ('AST-003', 'Server Rack', 'IT Equipment', 'medium', 'active'),
            ('AST-004', 'Hydraulic Press', 'Machinery', 'high', 'under_maintenance'),
        ]
        made = {}
        for code, name, category, crit, status in assets:
            made[code], _ = Asset.objects.get_or_create(asset_code=code, defaults={
                'asset_name': name, 'category': cat[category], 'criticality': crit, 'status': status,
                'purchase_date': today - timedelta(days=700), 'purchase_price': 450000,
                'location': 'Plant 1', 'department': 'Production'})
        orders = [
            ('WO-0001', 'AST-004', 'Pressure drop in hydraulic line', 'high', 'in_progress'),
            ('WO-0002', 'AST-001', 'Routine lubrication and calibration', 'medium', 'open'),
            ('WO-0003', 'AST-002', 'Brake pad replacement', 'low', 'completed'),
        ]
        for wo_no, asset, problem, priority, status in orders:
            WorkOrder.objects.get_or_create(wo_no=wo_no, defaults={
                'wo_date': today - timedelta(days=3), 'asset': made[asset], 'problem_description': problem,
                'priority': priority, 'status': status, 'assigned_technician': 'Maintenance Team'})
