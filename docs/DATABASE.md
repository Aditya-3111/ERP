# Database

FinLedger Pro uses **MySQL 8.0+ or MariaDB 10.5+** (any of: MySQL Installer, XAMPP with a recent MariaDB, Docker `mysql:8`).

## You do not create anything by hand

On the first `python manage.py runserver` the backend

1. connects to MySQL with the login in `backend/.env` (`DB_USER` / `DB_PASSWORD` - normally `root`),
2. runs `CREATE DATABASE IF NOT EXISTS finledger_pro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`,
3. creates all tables (`migrate`),
4. inserts the starting data: roles, Tally-style account groups, voucher types, units, financial years, company, the admin login,
5. if `SEED_DEMO_DATA=true`: inserts sample customers, items, employees, vouchers ...

The code for this is `backend/apps/core/db_bootstrap.py` and the commands in `backend/apps/core/management/commands/`.

Turn it off with `AUTO_SETUP_DB=false` in `.env` and run the same steps yourself:

```
python manage.py setup_db                 # create database + tables + starting data (+ demo data if enabled)
python manage.py setup_db --no-demo       # same, without sample records
python manage.py setup_db --reset --yes   # DROP the database and build it again  (deletes everything!)
python manage.py migrate                  # only create / update tables
```

## Backup and restore

```
mysqldump -u root -p finledger_pro > backup.sql
mysql -u root -p finledger_pro < backup.sql
```

## Changing the database layout

Edit a model in `backend/apps/<module>/models.py`, then

```
python manage.py makemigrations
python manage.py migrate
```

Never edit tables by hand in MySQL - the migration files are the history that keeps every computer in sync.

## Tables

### Core (users, roles, company)  (8 tables)

| Table | Django model | Columns |
|---|---|---|
| `core_audit_logs` | AuditLog | 8 |
| `core_branches` | Branch | 10 |
| `core_company_profile` | CompanyProfile | 19 |
| `core_financial_years` | FinancialYear | 7 |
| `core_roles` | Role | 6 |
| `core_system_settings` | SystemSetting | 6 |
| `core_user_sessions` | UserSession | 7 |
| `core_users` | User | 18 |

### Finance  (6 tables)

| Table | Django model | Columns |
|---|---|---|
| `fin_accounting_entries` | AccountingEntry | 8 |
| `fin_groups` | AccountGroup | 9 |
| `fin_inventory_entries` | InventoryEntry | 15 |
| `fin_ledgers` | Ledger | 42 |
| `fin_voucher_types` | VoucherType | 6 |
| `fin_vouchers` | Voucher | 18 |

### Inventory  (9 tables)

| Table | Django model | Columns |
|---|---|---|
| `inv_godowns` | Godown | 10 |
| `inv_mrn_entries` | MaterialReceiptNote | 12 |
| `inv_mrn_items` | MRNItem | 10 |
| `inv_stock_batches` | StockBatch | 8 |
| `inv_stock_categories` | StockCategory | 3 |
| `inv_stock_groups` | StockGroup | 3 |
| `inv_stock_items` | StockItem | 30 |
| `inv_stock_journals` | StockJournal | 11 |
| `inv_uom` | UnitOfMeasure | 7 |

### CRM  (8 tables)

| Table | Django model | Columns |
|---|---|---|
| `crm_activities` | Activity | 9 |
| `crm_customers` | Customer | 34 |
| `crm_leads` | Lead | 14 |
| `crm_po_items` | PurchaseOrderItem | 10 |
| `crm_purchase_inquiries` | PurchaseInquiry | 17 |
| `crm_purchase_orders` | PurchaseOrder | 21 |
| `crm_quotation_items` | QuotationItem | 10 |
| `crm_quotations` | Quotation | 28 |

### HR  (6 tables)

| Table | Django model | Columns |
|---|---|---|
| `hr_attendance` | Attendance | 8 |
| `hr_departments` | Department | 4 |
| `hr_designations` | Designation | 4 |
| `hr_employee_documents` | EmployeeDocument | 6 |
| `hr_employees` | Employee | 30 |
| `hr_pay_heads` | PayHead | 9 |

### Gate  (4 tables)

| Table | Django model | Columns |
|---|---|---|
| `gate_entries` | GateEntry | 20 |
| `gate_transporters` | Transporter | 5 |
| `gate_visitor_logs` | VisitorLog | 6 |
| `gate_visitors` | Visitor | 32 |

### POS  (9 tables)

| Table | Django model | Columns |
|---|---|---|
| `pos_counters` | POSCounter | 10 |
| `pos_customers` | POSCustomer | 8 |
| `pos_item_prices` | ItemPrice | 8 |
| `pos_payment_methods` | PaymentMethod | 5 |
| `pos_payments` | POSPayment | 7 |
| `pos_price_lists` | PriceList | 6 |
| `pos_sale_items` | POSSaleItem | 18 |
| `pos_sales` | POSSale | 23 |
| `pos_sessions` | POSSession | 17 |

### Production  (8 tables)

| Table | Django model | Columns |
|---|---|---|
| `prd_bom_header` | BOMHeader | 17 |
| `prd_bom_items` | BOMItem | 11 |
| `prd_machines` | Machine | 10 |
| `prd_operations` | Operation | 10 |
| `prd_orders` | ProductionOrder | 23 |
| `prd_output` | ProductionOutput | 17 |
| `prd_quality_inspection` | QualityInspection | 15 |
| `prd_work_centers` | WorkCenter | 11 |

### Maintenance  (7 tables)

| Table | Django model | Columns |
|---|---|---|
| `mnt_asset_categories` | AssetCategory | 8 |
| `mnt_assets` | Asset | 25 |
| `mnt_breakdowns` | Breakdown | 19 |
| `mnt_schedules` | MaintenanceSchedule | 16 |
| `mnt_spare_parts` | SparePart | 16 |
| `mnt_wo_tasks` | WorkOrderTask | 11 |
| `mnt_work_orders` | WorkOrder | 25 |

### Administration  (27 tables)

| Table | Django model | Columns |
|---|---|---|
| `admin_activity_feed` | ActivityFeed | 10 |
| `admin_api_tokens` | APIToken | 10 |
| `admin_backups` | DataBackup | 11 |
| `admin_config_presets` | ConfigurationPreset | 9 |
| `admin_db_statistics` | DatabaseStatistic | 6 |
| `admin_email_queue` | EmailQueue | 16 |
| `admin_email_templates` | EmailTemplate | 10 |
| `admin_ip_whitelist` | IPWhitelist | 6 |
| `admin_license` | License | 13 |
| `admin_login_attempts` | LoginAttempt | 7 |
| `admin_maintenance_mode` | MaintenanceMode | 9 |
| `admin_menu_groups` | MenuGroup | 9 |
| `admin_menu_items` | MenuItem | 15 |
| `admin_module_settings` | ModuleSetting | 7 |
| `admin_modules` | RegisteredModule | 13 |
| `admin_notifications` | Notification | 9 |
| `admin_permission_groups` | PermissionGroup | 5 |
| `admin_permissions` | Permission | 7 |
| `admin_restores` | DataRestore | 7 |
| `admin_role_permissions` | RolePermission | 6 |
| `admin_scheduled_tasks` | ScheduledTask | 11 |
| `admin_system_logs` | SystemLog | 7 |
| `admin_task_history` | TaskExecutionHistory | 9 |
| `admin_theme_settings` | ThemeSettings | 9 |
| `admin_user_permissions` | UserPermission | 8 |
| `admin_webhook_logs` | WebhookLog | 10 |
| `admin_webhooks` | Webhook | 12 |


Besides these, Django creates its own tables (`auth_*`, `django_*`, `token_blacklist_*`, sessions) for permissions, migration history and logout tokens.

Notes
* Every table has a UUID primary key called `guid`.
* A voucher's lines (`fin_accounting_entries`) refer to ledgers by **ledger name**, so ledger names are unique.
* Money columns are `DECIMAL`, never floating point.
