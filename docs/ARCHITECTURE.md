# How the project is organised

```
Browser (React, port 5173)  --JSON over HTTP-->  Django REST API (port 8000)  --SQL-->  MySQL (port 3306)
```

Two programs, started in two terminals. The React app never touches the database; it only calls the API.

## Backend  (`backend/`)

```
backend/
  manage.py                  start / manage the server
  .env                       private settings: MySQL login, secret key ...   (copy of .env.example)
  requirements.txt           python packages
  config/                    project settings (not a business module)
    settings.py              reads .env, database, REST + JWT + CORS settings
    env.py                   tiny .env reader
    urls.py                  /api/auth, /api/core, /api/finance ... routes
  apps/                      ONE FOLDER PER BUSINESS MODULE
    core/                    users, roles, company, financial years, dashboard API, database auto-setup
    finance/                 account groups, ledgers, vouchers, trial balance / P&L / balance sheet
    inventory/               stock items, godowns, batches, MRN
    crm/                     customers, leads, quotations, purchase orders
    hr/                      employees, attendance (bulk), payroll
    gate/                    visitors, gate entries
    pos/                     counters, sales, payments
    production/              BOM, production orders, quality
    maintenance/             assets, work orders, breakdowns
    admin_panel/             menus, permissions, themes, settings tables
  tests/                     automatic tests  (python manage.py test)
```

Inside every module folder:

| File | What it holds |
|---|---|
| `models.py` | the database tables (Python classes) |
| `migrations/` | generated history of table changes |
| `api/serializers.py` | what fields the API accepts / returns for each table |
| `api/views.py` | the API actions: list, create, edit, delete (+ special ones) |
| `api/urls.py` | the web addresses, e.g. `/api/hr/employees/` |
| `admin.py` | Django's built-in admin screen (http://localhost:8000/admin/) |

`apps/core/` additionally has `management/commands/` (setup_db, seed_masters, seed_demo, runserver) and `db_bootstrap.py`.

## Frontend  (`frontend/`)

```
frontend/
  index.html, vite.config.js, tailwind.config.js, postcss.config.js, package.json
  .env                       VITE_API_URL = address of the backend
  src/
    main.jsx                 starts React
    App.jsx                  providers (toast, login)
    index.css                Tailwind + a few shared classes (.btn .input .card ...)
    api/
      client.js              ALL calls to the backend (token, auto-refresh, error messages)
      lookups.js             drop-down lists filled from other tables
    context/                 AuthContext (who is logged in), PeriodContext (financial year), ToastContext
    hooks/                   useFetch, useDebounce, useLookup
    utils/format.js          money / date formatting
    components/
      ui/                    Button, Modal, Badge, Card, Spinner ... (no business logic)
      layout/                Sidebar, Topbar, AppLayout
      crud/                  ResourcePage + ResourceForm + DataTable  (the generic list/add/edit/delete screen)
    routes/                  AppRoutes (all URLs), ProtectedRoute (login required)
    pages/                   Login, Dashboard, Profile, NotFound
    modules/                 ONE FOLDER PER BUSINESS MODULE (same names as the backend)
      registry.js            list of modules (sidebar + routes are built from it)
      access.js              which role may open which module
      finance/ inventory/ crm/ hr/ gate/ pos/ production/ maintenance/ admin/
        resources.js         tables described as data: columns + form fields
        index.jsx            module definition: title, icon, menu, extra pages
        pages/               hand-written screens (only where a plain table is not enough)
```

### The idea that keeps the code small

Most screens are "a table + an add/edit form". Those are **not written as separate pages**. Each is a few lines in
`modules/<name>/resources.js`:

```js
export const departments = {
  key: 'departments', title: 'Departments', singular: 'Department', endpoint: '/hr/departments/',
  search: true,
  columns: [ { key: 'name', label: 'Name' }, ... ],
  fields:  [ { name: 'name', label: 'Name', type: 'text', required: true }, ... ],
};
```

and one shared component (`components/crud/ResourcePage.jsx`) turns it into a page with search, paging, add, edit and delete.
Screens that need real logic are written by hand in `modules/<name>/pages/`: voucher entry (debit = credit),
ledger statement, trial balance, profit & loss, balance sheet, bulk attendance, payroll, stock movements, dashboard.

A test (`backend/tests/test_frontend_contract.py`) compares every `resources.js` with the API, so a wrong field name
fails the tests instead of failing silently in the browser.

## Add a new module

1. Backend: `cd backend && python manage.py startapp ...` is not needed - copy the layout of a small app (e.g. `apps/gate`):
   `models.py`, `api/serializers.py`, `api/views.py`, `api/urls.py`; add it to `INSTALLED_APPS` in `config/settings.py`
   and to `config/urls.py`; run `makemigrations` and `migrate`.
2. Frontend: create `src/modules/<name>/resources.js` and `index.jsx` (copy `gate`), add the module to `modules/registry.js`
   and a role rule in `modules/access.js`. The menu and routes appear automatically.

## Add a column or a form field

Edit the `columns` / `fields` list in the module's `resources.js`. If the field is new in the database, add it to the
model first and run `makemigrations` + `migrate`, and to the serializer if it lists fields explicitly.

## Change the colours

`frontend/tailwind.config.js` -> `brand` colours.

## Login and security

* `POST /api/auth/login/` returns a short-lived *access* token (8 h) and a *refresh* token (30 days). Both are kept in the browser's localStorage.
* Every request sends `Authorization: Bearer <access>`. When it has expired the client silently gets a new one; when the refresh token is
  also dead the user is sent to the login page.
* Sign out blacklists the refresh token on the server.
