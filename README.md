# FinLedger Pro

Accounting + ERP software for Indian businesses (Tally-style): **Finance & GST ledgers, vouchers, trial balance, P&L,
balance sheet - plus Inventory, CRM, HR & payroll, Gate/visitors, POS, Production and Maintenance.**

| Part | Technology |
|---|---|
| Frontend | **React 19** + **Tailwind CSS 3** (built with Vite) |
| Backend | **Django 5.2** + Django REST Framework + JWT login |
| Database | **MySQL 8 / MariaDB 10.5+** - database and tables are created **automatically** |
| Settings | `backend/.env` (MySQL user `root` + password live here) |

You run **two programs in two terminals**: the backend (port 8000) and the frontend (port 5173).

```
finledger-pro/
├── backend/        Django API  (one folder per module in backend/apps/)
├── frontend/       React + Tailwind app  (one folder per module in frontend/src/modules/)
├── docs/           ARCHITECTURE.md (how the code is organised), DATABASE.md (setup + all tables)
├── .vscode/        tasks to start both servers from VS Code
└── README.md
```

---

## 1. What you need installed

| Program | Version | Check with |
|---|---|---|
| Python | 3.11 or newer | `python --version` |
| Node.js (includes npm) | 18 or newer | `node --version` |
| MySQL **or** MariaDB | MySQL 8.0+ / MariaDB 10.5+ | the service must be **running** |

> Old XAMPP versions ship MariaDB 10.4, which Django 5.2 refuses ("MariaDB 10.5 or later is required").
> Install a newer XAMPP, or MySQL Installer / `docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=secret mysql:8`.

## 2. Tell the backend your MySQL password

Open **`backend/.env`** and set the password of your MySQL `root` user (XAMPP's default root password is empty):

```ini
DB_USER=root
DB_PASSWORD=your_mysql_root_password
```

That is the only thing to configure. You do **not** create a database or tables - the backend does it.
(`backend/.env.example` is a clean copy of the file.)

## 3. Terminal 1 - backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

```

* PowerShell says *"running scripts is disabled"*? Run `Set-ExecutionPolicy -Scope Process Bypass` once, then activate again (or use Command Prompt).
* Linux / macOS: `source .venv/bin/activate` instead of `.venv\Scripts\activate`.

On the **first** start you will see:

```
Preparing database ...
Created database 'finledger_pro'.
Creating / updating tables ...
Adding starting data (roles, account groups, voucher types, admin user) ...
Database is ready.
Starting development server at http://127.0.0.1:8000/
```

Leave this terminal open.

## 4. Terminal 2 - frontend

```powershell
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** and sign in:

| Username | Password |
|---|---|
| `admin` | `admin` |

(Change them in `backend/.env` *before the first start*: `ADMIN_USERNAME`, `ADMIN_PASSWORD`; later use *My profile -> Change password*.)

## 5. Running it from VS Code

1. **File -> Open Folder** -> the `finledger-pro` folder. Accept the "install recommended extensions" prompt (Python, Tailwind CSS IntelliSense).
2. Open a terminal (menu *Terminal -> New Terminal*) and do steps 3 and 4 above - use the **`+`** button for the second terminal.
3. Pick the interpreter: `Ctrl+Shift+P` -> *Python: Select Interpreter* -> `backend\.venv\Scripts\python.exe`.
4. Shortcut once everything is installed: `Ctrl+Shift+P` -> *Tasks: Run Task* -> **Start backend + frontend** (opens both terminals for you).
5. Debugging Django: Run and Debug panel -> **Debug Django backend** (stop the normal backend terminal first, port 8000 must be free).

## 6. What you get

* **Dashboard** - sales, purchases, net profit, cash & bank, receivable / payable, 6-month chart, low stock, today's attendance (all from real data).
* **Finance** - ledgers (wipython manage.py runserverth GSTIN, bank, credit details), account groups, voucher entry with debit = credit check, ledger statement,
  **Trial Balance, Profit & Loss, Balance Sheet** for any date range, financial-year switcher in the top bar.
* **Inventory** - stock items (GST/HSN, min stock), groups, godowns, batches, stock journal, material receipts, stock movement history.
* **CRM** - customers, leads, inquiries, quotations, purchase orders.
* **HR** - employees, one-click **bulk attendance**, **payroll summary** (absent-day deduction), departments, designations, documents (file upload).
* **Gate** - visitors, gate entries, transporters.  **POS**, **Production** (BOM, orders, output, quality), **Maintenance** (assets, work orders, breakdowns).
* **Administration** - users, roles, financial years, company profile, branches, settings, audit logs and the system tables.
* Login with automatic token refresh, sign-out that really invalidates the token, role-based menu (an *HR* user sees only HR), mobile-friendly layout.

Sample data (customers, items, employees, 7 months of vouchers ...) is inserted on first start so every screen has content.
For an empty system set `SEED_DEMO_DATA=false` in `backend/.env` **before the first start** (or run `python manage.py setup_db --reset --yes --no-demo`).

## 7. Handy commands (run inside `backend/` with the virtual environment active)

| Command | Does |
|---|---|
| `python manage.py runserver` | start API (creates database/tables first if needed) |
| `python manage.py setup_db` | create database + tables + starting data without starting the server |
| `python manage.py setup_db --reset --yes` | **delete** the database and rebuild it |
| `python manage.py createsuperuser` | add another administrator |
| `python manage.py makemigrations` then `migrate` | after you change a model |
| `python manage.py test` | run the automatic tests (they use a temporary database, your data is safe) |
| `npm run build` (in `frontend/`) | production build into `frontend/dist` |

## 8. Troubleshooting

| Message / problem | Fix |
|---|---|
| `MySQL refused the login for user 'root'` | wrong `DB_PASSWORD` in `backend/.env` |
| `Could not connect to MySQL at 127.0.0.1:3306` | start the MySQL service (XAMPP: **Start** next to MySQL) |
| `MariaDB 10.5 or later is required` | install a newer MariaDB/MySQL (see section 1) |
| Login page says *Cannot reach the server at http://localhost:8000/api* | backend terminal is not running, or another program uses port 8000 |
| Browser console shows a **CORS** error | the page is not opened on `http://localhost:5173` - add its address to `CORS_ALLOWED_ORIGINS` in `backend/.env` |
| `npm install` fails | check `node --version` (needs 18+), delete `frontend/node_modules`, run again |
| Port 5173 / 8000 busy | close the old terminal; or change `server.port` in `frontend/vite.config.js` / run `python manage.py runserver 8001` and set `VITE_API_URL=http://localhost:8001/api` in `frontend/.env` |
| `pip install` cannot build a package | use Python 3.11-3.13 (very new Python versions may lack ready-made packages) |
| Forgot admin password | `python manage.py changepassword admin` |

## 9. API in one minute

Base address `http://localhost:8000/api`. Everything except login needs the header `Authorization: Bearer <access token>`.

| Address | Purpose |
|---|---|
| `POST /auth/login/`, `/auth/refresh/`, `/auth/logout/`, `GET /auth/profile/`, `POST /auth/change-password/` | sign in / out |
| `GET /core/dashboard/?from=&to=` | numbers for the dashboard |
| `/core/users/ roles/ financial-years/ company-profiles/ branches/ settings/ audit-logs/ notifications/` | administration tables |
| `/finance/ledgers/ account-groups/ voucher-types/ vouchers/ accounting-entries/` | finance tables (`vouchers` accept a nested `items` list) |
| `GET /finance/reports/trial-balance/ profit-loss/ balance-sheet/?from=&to=` | reports |
| `GET /finance/ledgers/<id>/transactions/` | ledger statement |
| `/inventory/...  /crm/...  /hr/...  /gate/...  /pos/...  /production/...  /maintenance/...  /admin/...` | module tables |
| `POST /hr/attendance/bulk/`, `GET /hr/payroll/?month=YYYY-MM`, `GET /inventory/items/<id>/movements/` | special actions |

Every table supports `GET list`, `POST`, `GET/PATCH/DELETE <id>`, plus `?search=`, `?page=`, `?page_size=` and field filters.
The Django admin screen (`http://localhost:8000/admin/`, same login) lets you look at the raw data.

## 10. Known limitations - please read

* **Roles only hide menu items.** The API itself still lets any logged-in user call any endpoint. Enforce per-role permissions in the
  viewsets (`permission_classes`) before putting real, multi-user data on the system.
* `DEBUG=true` and the sample `SECRET_KEY` are for development. For a real server set a long random `SECRET_KEY`, `DEBUG=false`,
  correct `ALLOWED_HOSTS`, serve the built frontend (`npm run build`) behind a real web server and use HTTPS.
* **Profit & Loss does not value closing stock** automatically (enter it as a ledger if needed). Balance sheet shows the difference
  if opening balances do not balance.
* Voucher *lines* store the ledger by name, so a ledger cannot be renamed without updating its old vouchers.
* Payroll is a simple summary (basic salary minus absent days); there is no payslip / statutory deduction module yet.
* POS sales, production orders and similar documents are plain forms; they do not yet post accounting entries or stock movements by themselves.
* The password in `backend/.env` is stored as plain text - that is normal for local development; never commit this file (`.gitignore` already excludes it).
