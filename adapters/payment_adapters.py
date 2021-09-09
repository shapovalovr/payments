from hashlib import sha256
import logging, requests, json, random, datetime
from core import config
from currency.currency import currency_list
from db.db_worker import add_payment
from flask import url_for

class PaymentAdapters():
    def __init__(self, amount, currency, descriptions):
        try:
            self.amount = amount
            self.order_id = random.randint(0, 100)
            self.currency = currency_list[currency]
            self.currency_client = currency
            self.descriptions = descriptions
        except Exception as e:
            logging.error(e)
            return url_for('error', _external=True)

    def get_payment_url(self):
        try:
            logging.info(
                f"{datetime.datetime.now()} Created payment №: {self.order_id} in the amount of {self.amount} in currency {self.currency_client} with description: {self.descriptions}")
            if self.currency == '840':
                add_payment(self.order_id, self.amount, self.currency_client, 'BILL', datetime.datetime.now(), self.descriptions)
                return self.get_bill_url()
            elif self.currency == '978':
                add_payment(self.order_id, self.amount, self.currency_client, 'PAY', datetime.datetime.now(), self.descriptions)
                return self.get_pay_Url()
            elif self.currency == '643':
                add_payment(self.order_id, self.amount, self.currency_client, 'INVOICE', datetime.datetime.now(), self.descriptions)
                return self.get_invoice()
            else:
                logging.error(f"{datetime.datetime.now()} Incorrect currency: {self.currency_client}")
                return url_for('error', _external=True)
        except Exception as e:
            logging.error(e)
            return url_for('error', _external=True)


    def get_sign(self):
        if self.currency == '978':
            hashvalue = sha256(
                f"{self.amount}:{self.currency}:{config.PAY_SHOP_ID}:{self.order_id}{config.PAY_SECRET}".encode(
                    'utf-8')).hexdigest()
        elif self.currency == '840':
            hashvalue = sha256(
                f"{self.currency}:{self.amount}:{self.currency}:{config.BILL_SHOP_ID}:{self.order_id}{config.PAY_SECRET}".encode(
                    'utf-8')).hexdigest()
        elif self.currency == '643':
             hashvalue = sha256(
                f"{self.amount}:{self.currency}:{config.INVOICE_PAYWAY}:{config.INVOICE_SHOP_ID}:{self.order_id}{config.INVOICE_SECRET}".encode(
                    'utf-8')).hexdigest()
        return hashvalue


    def get_pay_Url(self):
        hashvalue = self.get_sign()
        payload = f'<form name="Pay" method="post" action="{config.PAY_URL}" accept-charset="UTF-8"> ' \
                  f'  <input type="hidden" name="amount" value="{self.amount}"/> ' \
                  f'  <input type="hidden" name="currency" value="{self.currency}"/> ' \
                  f'  <input type="hidden" name="shop_id" value="{config.PAY_SHOP_ID}"/> ' \
                  f'  <input type="hidden" name="sign" value="{hashvalue}"/> ' \
                  f'  <input type="hidden" name="shop_order_id" value="{self.order_id}"/>' \
                  f'  <input type="submit"/> <input type="hidden" name="description" value="{self.descriptions}"/> ' \
                  f'</form>'
        headers = {
            'Content-Type': 'text/html'
        }
        response = requests.post(config.PAY_URL, headers=headers, data=payload)
        if response.status_code == 200:
            logging.info(f"Response code: {response.status_code} With response {response.text}")
            return response.url
        else:
            logging.error(f"Response code: {response.status_code} With response {response.text}")


    def get_bill_url(self):
        hashvalue = self.get_sign()
        payload = json.dumps({
            "description": self.descriptions,
            "payer_currency": self.currency,
            "shop_amount": self.amount,
            "shop_currency": self.currency,
            "shop_id": config.BILL_SHOP_ID,
            "shop_order_id": self.order_id,
            "sign": hashvalue
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(config.BILL_URL, headers=headers, data=payload)
        response.json()['data']['url']
        if response.status_code == 200:
            logging.info(f"Response code: {response.status_code} With response {response.text}")
            return response.json()['data']['url']
        else:
            logging.error(f"Response code: {response.status_code} With response {response.text}")


    def get_invoice(self):
        hashvalue = self.get_sign()
        payload = json.dumps({
            "amount": self.amount,
            "currency": int(self.currency),
            "description": self.descriptions,
            "payway": config.INVOICE_PAYWAY,
            "shop_id": config.INVOICE_SHOP_ID,
            "shop_order_id": self.order_id,
            "sign": hashvalue
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(config.INVOICE_URL, headers=headers, data=payload)
        data_info = response.json()["data"]["data"]
        response_data = response.json()["data"]
        if response.status_code == 200:
            logging.info(f"Response code: {response.status_code} With response {response.text}")
            form_start = f'<form name="source" method="{response_data["method"]}" action="{response_data["url"]}" accept-charset="UTF-8">'
            form_end = f'  <input type="submit"/>' \
                       f'</form>'
            for keys in data_info.keys():
                form_start += f'  <input type="hidden" name="{keys}"  value="{data_info[keys]}" />'
            return form_start + form_end
        else:
            logging.error(f"Response code: {response.status_code} With response {response.text}")
