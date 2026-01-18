from sqlalchemy.exc import IntegrityError
from models import Session, LedgerEntry

VALID_TRANSITIONS = {
    'pending': ['confirmed', 'reversed'],
    'confirmed': ['paid', 'reversed'],
    'paid': [],
    'reversed': []
}

def create_credit_reward(user_id, amount, reference_id):
    session = Session()
    try:
        existing = session.query(LedgerEntry).filter_by(reference_id=reference_id).first()
        if existing:
            return existing

        entry = LedgerEntry(
            user_id=user_id,
            amount=amount,
            entry_type='credit',
            status='pending',
            reference_id=reference_id
        )
        session.add(entry)
        session.commit()
        return entry

    except IntegrityError:
        session.rollback()
        return session.query(LedgerEntry).filter_by(reference_id=reference_id).first()
    finally:
        session.close()

def update_status(entry_id, new_status):
    session = Session()
    try:
        entry = session.query(LedgerEntry).get(entry_id)
        if not entry:
            raise ValueError("Ledger entry not found")

        if new_status not in VALID_TRANSITIONS[entry.status]:
            raise ValueError(f"Invalid transition {entry.status} → {new_status}")

        entry.status = new_status
        session.commit()
        return entry
    finally:
        session.close()
def reverse_reward(entry_id):
    
    session = Session()
    try:
        original = session.query(LedgerEntry).get(entry_id)
        if not original:
            raise ValueError("Original entry not found")

        #  Deterministic idempotency key
        reversal_reference = f"reversal_{original.reference_id}"

        existing_reversal = (
            session.query(LedgerEntry)
            .filter_by(reference_id=reversal_reference)
            .first()
        )
        if existing_reversal:
            return existing_reversal

        # Create reversal entry (append-only)
        reversal = LedgerEntry(
            user_id=original.user_id,
            amount=-original.amount,
            entry_type='debit',
            status='reversed',
            reference_id=reversal_reference,
            reversal_id=original.id
        )

        #  Lifecycle update (allowed metadata change)
        original.status = 'reversed'

        session.add(reversal)
        session.commit()
        return reversal

    finally:
        session.close()

