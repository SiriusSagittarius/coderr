# Coderr Backend

A Django REST Framework backend for the Coderr platform, a marketplace where
business users publish service offers and customer users book them.

## Tech Stack

- Python, Django 5
- Django REST Framework
- Token authentication (`rest_framework.authtoken`)
- SQLite (development database)
- django-filter, django-cors-headers, Pillow

## Project Structure

The project root is the `core` app (settings, URL routing, WSGI/ASGI). All
business logic lives in dedicated apps, each with an `api/` sub-package
containing its serializers, views, urls and permissions:

```
core/            settings.py, urls.py, wsgi.py, asgi.py
auth_app/        custom User model, registration & login endpoints
profile_app/     Profile model, profile retrieve/update/list endpoints
offers_app/      Offer & OfferDetail models, offer CRUD + filtering
orders_app/      Order model, order CRUD + order-count endpoints
reviews_app/     Review model, review CRUD
platform_app/    cross-cutting endpoints (e.g. platform statistics)
```

Each app also has its own `tests/` package and `admin.py`.

## Getting Started

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

The API is then available at `http://127.0.0.1:8000/api/`. The Django admin
is available at `http://127.0.0.1:8000/admin/`.

## Authentication

Registration and login return a token:

```
POST /api/registration/
POST /api/login/
```

Authenticated requests must send the token in the `Authorization` header:

```
Authorization: Token <token>
```

## Running Tests & Coverage

```powershell
py manage.py test
coverage run manage.py test
coverage report -m
```

The test suite currently covers 99% of the codebase (excluding migrations
and settings boilerplate).

## Notable Details

- A `Profile` is created automatically for every new user via a Django
  signal in `profile_app` (decoupling `auth_app` from `profile_app`).
- Profile text fields (`first_name`, `last_name`, `location`, `tel`,
  `description`, `working_hours`) are guaranteed to never be `null` in API
  responses; they default to an empty string.
- Offers must be created with exactly one `basic`, one `standard` and one
  `premium` detail; `PATCH` updates target a detail by its `offer_type`.
- Orders are immutable snapshots of an `OfferDetail` at the time of booking;
  only their `status` field can later be changed by the business owner.
- `db.sqlite3` and `media/` are intentionally excluded from version control
  (see `.gitignore`); the database is regenerated locally via `migrate`.
- CORS is restricted to `http://127.0.0.1:5500` / `http://localhost:5500`
  for local frontend development — adjust `CORS_ALLOWED_ORIGINS` in
  `core/settings.py` for other setups..
