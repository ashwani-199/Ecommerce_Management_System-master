# Ecommerce Management System - Project Documentation

## 📌 Project Overview
This repository implements a full stack **Ecommerce Management System** built with **Django** and a custom admin panel. It supports:

- Catalog management (products, categories, images)
- Shopping cart, checkout, and order processing
- Customer accounts and authentication
- Admin dashboard for managing users, products, orders, and more

The project is organized as a Django multi-app project with a modular app structure.

---

## 🗂️ Repository Structure (High Level)

- **manage.py** – Django command-line utility.
- **db.sqlite3** – Default development database.
- **mysite_management/** – Django project settings (settings.py, urls.py, wsgi/asgi).
- **apps/** – Django apps grouped by feature domain (customers, orders, products, etc.).
- **fronts/** – Frontend-facing apps (home, contact, etc.).
- **static/** – Static assets (CSS, JS, images, vendor libs).
- **templates/** – Global templates and shared layouts.
- **media/** – Uploaded media (product images, user uploads).

---

## 🧩 Key Apps (What They Do)

### ✅ Core Business Apps
- **product/** – Product models, admin, API serializers, views, and product-related forms.
- **orders/** – Order models, checkout flow, order tracking, and related serializers.
- **customers/** – Customer profiles, customer-facing pages, and management logic.
- **users/** – Authentication, registration, user forms, and user-related serializers.
- **shipping_cart/** – Shopping cart management, cart models, and cart views.
- **payment/** – Payment-related models and views (integration points).

### ✅ Admin / Dashboard
- **dashboard/** – Admin dashboard views and data aggregation for sales, orders, and users.
- **login/** – Custom login flow and access control (likely used by the admin panel).

### ✅ Public Frontend
- **fronts/home/** – Homepage and public landing pages.
- **fronts/contact/** – Contact form and related pages.

---

## 🛠️ Getting Started (Local Development)

1. **Create and activate a virtual environment**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

3. **Run migrations**

   ```powershell
   python manage.py migrate
   ```

4. **Create a superuser**

   ```powershell
   python manage.py createsuperuser
   ```

5. **Run the development server**

   ```powershell
   python manage.py runserver
   ```

6. **Open in browser**
   - Website: `http://127.0.0.1:8000/`
   - Admin (if present): `http://127.0.0.1:8000/admin/` or custom dashboard URL.

---

## 🔧 Configuration Notes

- Database: default uses SQLite (`db.sqlite3`). To switch to MySQL/PostgreSQL, update `mysite_management/settings.py` with the proper `DATABASES` settings.
- Media files are served from `media/` and static assets from `static/`.
- Templates are rendered from `templates/` and per-app `templates/` folders.

---

## 🧪 Testing

Run unit tests for all apps:

```powershell
python manage.py test
```

---

## ✅ Adding New Features

1. Create a new Django app with `python manage.py startapp <app_name>`.
2. Register the app in `mysite_management/settings.py` under `INSTALLED_APPS`.
3. Add URL configuration in the app, and include it in the project `urls.py`.

---

## 📍 Where to Look for Common Code

- **URL routing:** `mysite_management/urls.py` + each app’s `urls.py`
- **Views:** `apps/*/views.py` and `fronts/*/views.py`
- **Models:** `apps/*/models.py`, `fronts/*/models.py`
- **Forms:** `apps/*/forms.py` and `fronts/*/forms.py`

---

## 📝 Notes
- This document is intended to provide a general orientation to the repository and help contributors get started quickly.
- Update this file as the project evolves (new apps, migrations, settings changes, etc.).
