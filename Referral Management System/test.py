from ledger import create_credit_reward, reverse_reward, update_status
from models import Session, LedgerEntry

session = Session()
session.query(LedgerEntry).delete()
session.commit()
session.close()

credit = create_credit_reward(1, 500, "ref123")
print(f"Created credit: ID={credit.id}, Status={credit.status}")

dup = create_credit_reward(1, 500, "ref123")
print(f"Duplicate credit: ID={dup.id}")

update_status(credit.id, "confirmed")
print("Updated to confirmed")

reversal = reverse_reward(credit.id)
print(f"Reversal: ID={reversal.id}, Amount={reversal.amount}")

dup_rev = reverse_reward(credit.id)
print(f"Duplicate reversal: ID={dup_rev.id}")
