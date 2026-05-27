# Database Design

## Tables

users

consultations

transactions

reviews

chat_messages

---

# Relationships

User
│
├── Client
│
└── Consultant
│
▼
Consultation
│
├── Transaction
│
└── Review

---

# Database

PostgreSQL

---

# ORM

SQLAlchemy Async

---

# Migration Tool

Alembic