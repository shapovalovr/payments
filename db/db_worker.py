from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy, logging
from models.payments import Payments
from flask import url_for
from core.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

def create_table():
    if not engine.dialect.has_schema(engine, 'payments'):
        engine.execute(sqlalchemy.schema.CreateSchema('payments'))
        Base.metadata.create_all(engine)

def add_payment(order_id, amount, currency, payment_type, created_at, description):
    try:
        create_table()
        payment = Payments(order_id = order_id, amount = amount, currency = currency, payment_type = payment_type, created_at = created_at, description = description)
        session.add(payment)
        session.commit()
    except Exception as e:
        logging.error(e)