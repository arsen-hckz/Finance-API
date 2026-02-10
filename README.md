# 💰 Finance Management API

A production-ready RESTful API for personal finance tracking, built with **Django**, **MySQL**, and **Docker**. This project demonstrates advanced backend architecture, including automated data integrity through **Django Signals** and a fully containerized development environment.



## 🌟 Key Features
* **Automated Accounting:** Custom Django Signals listen for transactions and update the corresponding Account balance in real-time.
* **Containerized Infrastructure:** Orchestrated with Docker Compose, separating the application logic from the database layer for portability and scalability.
* **Relational Integrity:** Implements strict foreign key relationships between Users, Accounts, and Transactions.
* **Persistent Storage:** Docker volumes ensure financial data remains intact even if containers are destroyed or rebuilt.

---

## 🛠️ Tech Stack
* **Backend:** Python 3.12, Django
* **API:** Django REST Framework (DRF)
* **Database:** MySQL 8.0
* **Containerization:** Docker, Docker Compose

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is installed and running.

### 2. Configure Environment
Create a `.env` file in the root directory:
```ini
MYSQL_DB=finance
MYSQL_ROOT_PASSWORD=your_secure_password
MYSQL_HOST=db
MYSQL_PORT=3306
SECRET_KEY=your_django_secret_key


### 3. Build, Launch, and Initialize
Run the following commands to build the containers, apply the database schema, and set up your administrative access:

```bash
# Build and start containers in the background
docker-compose up --build -d

# Wait 10-15 seconds for MySQL to initialize, then run migrations and create admin
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser


Method	Endpoint	Description
POST	/auth/users/	Register a new user
POST	/auth/jwt/create/	Login & receive JWT tokens
GET	/api/accounts/	List all user accounts & balances
POST	/api/transactions/	Create transaction (triggers balance update)
GET	/api/categories/	List expense/income categories