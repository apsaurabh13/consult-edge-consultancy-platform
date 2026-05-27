# Chatbot Module

## Purpose

Allow users to query application data using natural language.

---

# Supported Intents

booking_query

payment_status

review_lookup

consultant_availability

action_cancel

spend_summary

general

---

# Flow

User Message
↓
Intent Classification
↓
SQL Resolver
↓
Database Query
↓
Response Builder
↓
Response

---

# Example

User:

Show my upcoming consultations

Intent:

booking_query

SQL:

SELECT *
FROM consultations
WHERE client_id=:user_id

Response:

You have 3 upcoming consultations.