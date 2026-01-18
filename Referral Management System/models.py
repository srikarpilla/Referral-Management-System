from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class LedgerEntry(Base):
    __tablename__ = 'ledger_entries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)

    # Positive = credit, Negative = debit
    amount = Column(Float, nullable=False)

    # credit | debit
    entry_type = Column(String, nullable=False)

    # pending → confirmed → paid | reversed
    status = Column(String, nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow)

    # Idempotency key
    reference_id = Column(String, unique=True, nullable=False)

    # Links reversal entry to original
    reversal_id = Column(Integer, ForeignKey('ledger_entries.id'), nullable=True)

engine = create_engine('sqlite:///ledger.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine, expire_on_commit=False)
