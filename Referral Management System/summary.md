



 Project Summary: Referral Management System

 Problem Statement

Referral systems involve monetary rewards, which makes correctness, auditability, and safety critical. The challenge is to design a system that can reliably track referral rewards, handle retries without duplication, support reversals, and apply business rules in a clear and extensible way.
This project addresses that problem by combining a financial ledger backend with a rule-based flow builder for referral logic.



 High-Level Architecture

The project is split into two independent but complementary parts:

1. Part 1 – Financial Ledger System
   Responsible for safely recording referral rewards and reversals.
2. Part 2 – Rule-Based Flow Builder
   Responsible for defining when a referral reward should be issued.

This separation mirrors real-world systems where decision logic and financial accounting are intentionally decoupled.



 Part 1: Financial Ledger System

 How It Works

The ledger is implemented as an append-only financial record where every monetary event is stored as a new entry. Instead of modifying or deleting records, all changes (such as reversals) are represented as additional ledger entries.

 Data Model

Each ledger entry contains:

 user_id       – identifies the beneficiary
 amount        – positive for credits, negative for debits
 entry_type    – credit or debit
 status        – lifecycle state (pending, confirmed, paid, reversed)
 reference_id  – unique idempotency key
 reversal_id   – links a reversal to the original entry
 timestamp     – audit trail

A relational (SQL) database was chosen to guarantee ACID transactions, which are essential for financial correctness.



 Input → Processing → Output (Ledger)

Input

 User ID
 Reward amount
 Reference ID (unique per referral event)

Processing

1. Check for an existing ledger entry with the same reference_id (idempotency).
2. If none exists, create a new credit entry with pending status.
3. Allow controlled lifecycle transitions (pending → confirmed → paid).
4. For reversals, create a new debit entry with a deterministic reversal reference.
5. Return existing entries on repeated calls instead of duplicating data.

Output

 A ledger entry object representing the credit or reversal
 Deterministic, repeatable results even under retries

This design ensures:

 No double credits
 No accidental double reversals
 Full auditability of all reward movements



 Part 2: Rule-Based Flow Builder

 Purpose

Referral logic often changes and should not be hardcoded into the ledger. The rule engine defines conditions under which rewards should be triggered, independent of how rewards are recorded.

 Rule Representation

Rules are represented in JSON with a clear separation between:

 Conditions – boolean checks on referral state
 Actions – outcomes such as issuing a reward

Example:


IF referrer is a paid user
AND referred user subscribes
THEN issue ₹500 reward




 Visual Flow Builder

The UI provides a visual representation of the rule logic:

 Red nodes represent conditions
 Green nodes represent actions
 Connections show evaluation flow from left to right

The UI is intentionally lightweight and focuses on clarity of logic rather than full editing features.



 Input → Processing → Output (Rules)

Input

 Referral context (e.g., referrer status, subscription state)

Processing

1. Evaluate each condition against the context.
2. If all conditions pass, execute the configured actions.
3. Actions are currently printed/logged but are designed to integrate with the ledger.

Output

 Deterministic execution of referral actions
 Clear mapping between business rules and system behavior



 Bonus: Natural Language to Rule Conversion

A bonus component demonstrates how a natural language referral rule can be converted into structured rule JSON, simulating LLM-assisted configuration.
This shows how non-technical users could define referral logic while the system maintains strict structure internally.



 End-to-End Flow Summary

1. A referral event occurs.
2. Rule engine evaluates whether reward conditions are met.
3. If valid, the ledger creates a reward entry.
4. The ledger guarantees idempotency, correctness, and auditability.
5. Any reversal or retry is safely handled without duplication.



 Key Technical Principles Used

 Append-only ledger design
 Idempotent APIs
 Deterministic reference IDs
 Controlled state transitions
 Separation of decision logic and accounting
 Audit-friendly data modeling



 Conclusion

This project demonstrates how to design a referral system that treats money as a first-class concern. The focus is not on UI polish or feature completeness, but on correctness, clarity, and safe system design, which are critical for real-world financial workflows.
