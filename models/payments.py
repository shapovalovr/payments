from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Payments(Base):
    __tablename__ = 'payments_info'
    __table_args__ = {"schema": "payments"}

    id = Column(Integer, primary_key=True)
    order_id = Column('order_id', Integer)
    amount = Column('amount', VARCHAR(length=200))
    currency = Column('currency', VARCHAR(length=5))
    payment_type = Column('payment_type', VARCHAR(length=20))
    created_at = Column('created_at', TIMESTAMP)
    description = Column('description', VARCHAR(length=200))
