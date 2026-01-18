 Take-Home Challenge – Referral Management System

 Overview
This project is a partial implementation of a referral management system, designed to demonstrate system thinking, correctness in financial flows, and clean abstractions rather than feature completeness.

The solution is divided into two parts:
- Part 1: A financial ledger system for referral rewards
- Part 2: A rule engine and visual flow builder for defining referral logic

The focus was on correctness, auditability, and clarity of design.



 Part 1 – Financial Ledger System

 What is Implemented
- Immutable, append-only ledger entries
- Credit and reversal flows for referral rewards
- Reward lifecycle management (`pending → confirmed → paid / reversed`)
- Idempotent reward creation using a deterministic reference ID
- Audit-friendly data model

 Data Model Choice
I chose SQL (SQLite via SQLAlchemy) instead of NoSQL because:
- Financial data requires strong consistency and transactional guarantees
- ACID properties are critical for money-related systems
- Relational structure simplifies auditing and reconciliation

NoSQL could be considered at higher scale, but correctness and integrity were prioritized here.

 Correctness Guarantees
- Immutability: Ledger entries are append-only; reversals are represented as new offsetting entries
- Idempotency: Duplicate reward or reversal requests return the existing ledger entry
- Atomicity: Database transactions ensure safe state transitions



 Part 2 – Rule-Based Flow Builder

 What is Implemented
- A JSON-based rule representation separating conditions and actions
- A simple rule evaluation engine
- A visual flow builder UI with condition and action nodes
- Clear left-to-right logic flow for referral rules


