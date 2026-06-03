# Consult Edge Consultancy Platform

## Project Status

Current Phase: **Backend Foundation + Authentication Complete**

Completion Date: 2026-05-28

---

# Tech Stack

## Backend

* FastAPI
* PostgreSQL
* SQLAlchemy Async ORM
* Alembic
* Pydantic v2
* JWT Authentication
* Passlib + Bcrypt

## Frontend

* Next.js 15
* TypeScript
* TailwindCSS

---

# Backend Architecture

Repository Pattern + Service Layer Architecture

```text
Router
  ↓
Service
  ↓
Repository
  ↓
Database
```

Example:

```text
Auth Router
    ↓
Auth Service
    ↓
User Repository
Session Repository
    ↓
PostgreSQL
```

---

# Current Folder Structure

```text
backend/app

├── api
│   ├── dependencies
│   │   └── auth.py
│   ├── v1
│   │   └── auth
│   │       └── router.py
│   └── routers.py

├── core
│   ├── config.py
│   ├── constants.py
│   └── security.py

├── db
│   ├── base.py
│   ├── mixins.py
│   └── session.py

├── models
│   ├── user.py
│   └── user_session.py

├── repositories
│   ├── user_repository.py
│   └── session_repository.py

├── schemas
│   └── auth
│       ├── login.py
│       ├── logout.py
│       ├── refresh.py
│       ├── register.py
│       └── token.py

├── services
│   └── auth_service.py

└── main.py
```

---

# Authentication Module Completed

## APIs

### Register

```http
POST /api/v1/auth/register
```

Creates a new user.

---

### Login

```http
POST /api/v1/auth/login
```

Returns:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

---

### Current User

```http
GET /api/v1/auth/me
```

Protected route.

Returns authenticated user.

---

### Refresh Token

```http
POST /api/v1/auth/refresh
```

Generates new access token.

---

### Logout

```http
POST /api/v1/auth/logout
```

Revokes refresh token session.

---

# Database Tables Implemented

## users

Fields:

```text
id
first_name
last_name
email
phone
password_hash
role
is_active
is_verified
created_at
updated_at
```

---

## user_sessions

Fields:

```text
id
user_id
refresh_token
is_revoked
expires_at
created_at
updated_at
```

Purpose:

* Store refresh tokens
* Enable logout
* Enable token revocation
* Multi-device session support

---

# Security Layer

Implemented in:

```text
app/core/security.py
```

Functions:

```python
hash_password()

verify_password()

create_access_token()

create_refresh_token()

decode_token()
```

Authentication Strategy:

```text
Access Token
    ↓
JWT
    ↓
Authorization Header
```

Refresh Token:

```text
JWT
    ↓
Stored in user_sessions table
```

---

# Dependency Injection Pattern

FastAPI dependency injection is used.

Example:

```python
db: AsyncSession = Depends(get_db)
```

Used for:

* Database Session Injection
* Current User Injection
* Future Role-Based Authorization

---

# Roles

Current Enum:

```text
ADMIN
CONSULTANT
CLIENT
SUPER_ADMIN
```

Default role during registration:

```text
CLIENT
```

---

# Completed Learning Outcomes

The developer now understands:

* FastAPI routing
* Dependency Injection
* SQLAlchemy Async
* Repository Pattern
* Service Layer Pattern
* JWT Authentication
* Refresh Token Strategy
* Session Revocation
* Alembic Migrations
* Pydantic Schemas
* Async Database Sessions

---

# Current Git Strategy

```text
main
│
├── saurabh-backend
│
├── saurabh-frontend
│
├── feature/auth
├── feature/profile
├── feature/consultants
├── feature/booking
└── feature/payments
```

Workflow:

```text
feature/*
      ↓
saurabh-backend
      ↓
main
```

Frontend:

```text
feature/*
      ↓
saurabh-frontend
      ↓
main
```

Never develop directly on main.

---

# Important Notes

Authentication module is considered COMPLETE.

Do NOT spend more time improving auth.

Move to business features.

---

# Next Target (Day 03)

## Consultant Module Foundation

Implement:

### Models

```text
consultant.py
expertise_category.py
consultant_expertise.py
availability.py
```

---

### Repositories

```text
consultant_repository.py
availability_repository.py
```

---

### Service

```text
consultant_service.py
```

---

### APIs

#### Become Consultant

```http
POST /consultants
```

Creates consultant profile.

Changes user role:

```text
CLIENT
  ↓
CONSULTANT
```

---

#### My Consultant Profile

```http
GET /consultants/me
```

---

#### Update Consultant Profile

```http
PATCH /consultants/me
```

---

#### Availability APIs

```http
POST   /availability
GET    /availability/me
PATCH  /availability/{id}
DELETE /availability/{id}
```

---

#### Expertise APIs

```http
GET /expertise
POST /expertise
```

---

# Future Roadmap

Phase 1

```text
Consultant Module
Availability Module
Expertise Module
```

Phase 2

```text
Consultant Search
Consultant Public Profile
```

Phase 3

```text
Booking System
```

Phase 4

```text
Payments
```

Phase 5

```text
Reviews & Ratings
```

Phase 6

```text
Admin Panel
```

---

# Current Project Health

Backend Foundation: 100%

Authentication: 100%

Business Features: 0%

Next Priority:

```text
Consultant Module
```
