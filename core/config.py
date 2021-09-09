import os
from envyaml import EnvYAML

if os.environ.get('ENV') == "heroku":
    PAY_URL = os.environ.get('PAY_URL')
    PAY_SHOP_ID = os.environ.get('PAY_SHOP_ID')
    PAY_SECRET = os.environ.get('PAY_SECRET')

    BILL_URL = os.environ.get('BILL_URL')
    BILL_SHOP_ID = os.environ.get('BILL_SHOP_ID')
    BILL_SECRET = os.environ.get('BILL_SECRET')

    INVOICE_URL = os.environ.get('INVOICE_URL')
    INVOICE_SHOP_ID = os.environ.get('INVOICE_SHOP_ID')
    INVOICE_SECRET = os.environ.get('INVOICE_SECRET')
    INVOICE_PAYWAY = os.environ.get('INVOICE_PAYWAY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres','postgresql')
else:
    secrets = EnvYAML('./resources/application-secret.yml')
    PAY_URL = secrets['pay.url']
    PAY_SHOP_ID = secrets['pay.shop_id']
    PAY_SECRET = secrets['pay.secret']

    BILL_URL = secrets['piastrix.url']
    BILL_SHOP_ID = secrets['piastrix.shop_id']
    BILL_SECRET = secrets['piastrix.secret']

    INVOICE_URL = secrets['invoice.url']
    INVOICE_SHOP_ID = secrets['invoice.shop_id']
    INVOICE_SECRET = secrets['invoice.secret']
    INVOICE_PAYWAY = secrets['invoice.payway']

    POSTGRES_SERVER = secrets['db_info.db_host']
    POSTGRES_USER = secrets['db_info.db_user']
    POSTGRES_PASSWORD = secrets['db_info.db_pass']
    POSTGRES_DB = secrets['db_info.db_name']
    SQLALCHEMY_DATABASE_URI = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB}")