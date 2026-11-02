# Finance Management API

REST API for personal finance tracking. Users keep several accounts (bank,
cash, ...), record income and expense transactions against them, and a Django
signal keeps each account's balance up to date.

## Features
* **Automatic balances:** a `post_save` signal on `Transaction` adds income and subtracts expenses from the account balance. The update runs in the database (`balance = balance + change`) inside the same DB transaction as the insert, so concurrent transactions can't lose an update.
* **Per-user data:** users only see their own accounts and transactions, and can only post transactions to their own accounts.
* **Validation:** amounts must be positive (the category decides the direction); bad filter values get a 400, not a 500.
* **JWT auth** via Djoser and Simple JWT.
* **Seed data:** `python manage.py seed_categories` adds a set of Greek income/expense categories.

## Tech Stack
* Python 3.12, Django, Django REST Framework
* Djoser + Simple JWT
* MySQL 8.0
* Docker, Docker Compose

## Getting Started

### 1. Prerequisites
[Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### 2. Configure Environment
Create a `.env` file in the root directory (never commit it):
```ini
MYSQL_DB=finance
MYSQL_PASSWORD=your_secure_password
MYSQL_HOST=db
MYSQL_PORT=3306
DJANGO_SECRET_KEY=your_django_secret_key
```
The app connects as MySQL `root`; `MYSQL_PASSWORD` is used as the root password of the `db` container.

### 3. Build, Launch, and Initialize
```bash
# Build and start containers in the background
docker-compose up --build -d

# Wait 10-15 seconds for MySQL to initialize, then:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py seed_categories
docker-compose exec web python manage.py createsuperuser
```

The API is at http://localhost:8000. MySQL is published on host port 3307.

## Endpoints

All `/api/` endpoints need `Authorization: Bearer <access token>`.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/users/` | Register (`username`, `password`, `re_password`) |
| POST | `/auth/jwt/create/` | Login & receive JWT tokens |
| POST | `/auth/jwt/refresh/` | Get a new access token |
| GET, POST | `/api/accounts/` | List / create your accounts and balances |
| GET, POST | `/api/transactions/` | List / create transactions (`?category=<id>` to filter) |
| GET | `/api/categories/` | List expense/income categories |

## Tests

```bash
docker-compose exec web python manage.py test API
```

13 tests in `API/tests.py`: registration and JWT login, balance updates for
income and expenses, amount validation, per-user access (including posting to
another user's account), category listing and filtering.
