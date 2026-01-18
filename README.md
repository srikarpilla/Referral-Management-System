This project is a small referral management system built to explore how referral rewards can be handled safely and clearly. It focuses on two core problems: deciding when a referral reward should be issued, and recording that reward in a way that is correct, auditable, and resilient to retries or failures.

The backend uses an immutable ledger approach to track referral credits and reversals, ensuring idempotency and proper lifecycle handling for money-related flows. On top of that, a simple rule engine and visual flow builder are used to express referral logic in a clear, structured way, separating business rules from financial accounting.

The implementation is intentionally partial and lightweight, with an emphasis on system design, correctness, and reasoning rather than UI polish or feature completeness.
