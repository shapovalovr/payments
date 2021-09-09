import pytest, random, requests, sys, os, datetime
sys.path.append(os.getcwd())
from adapters import payment_adapters
from db.db_worker import add_payment

@pytest.mark.parametrize("amount, currency, description", [(round(random.randint(0, 100),2),'USD', f'{round(random.randint(0, 100))}-test'),
                                                           (str(round(random.randint(0, 100),2)),'USD', f"{round(random.randint(0, 100))}-test"),
                                                           (str(round(random.randint(0, 100),2)),'USD', f"{round(random.randint(0, 100))}-test")])
def test_payments_usd_good(amount, currency, description):
    assert requests.get(payment_adapters.PaymentAdapters(amount, currency, description).get_payment_url()).status_code == 200

@pytest.mark.parametrize("amount, currency, description", [(round(random.randint(0, 100),2),'EUR', f'{round(random.randint(0, 100))}-test'),
                                                           (str(round(random.randint(0, 100),2)),'EUR', f"{round(random.randint(0, 100))}-test"),
                                                           (str(round(random.randint(0, 100),2)),'EUR', f"{round(random.randint(0, 100))}-test")])
def test_payments_eur_good(amount, currency, description):
    assert requests.get(payment_adapters.PaymentAdapters(amount, currency, description).get_payment_url()).status_code == 200

@pytest.mark.parametrize("amount, currency, description", [(round(random.randint(10, 100),2),'RUB', f'{round(random.randint(0, 100))}-test'),
                                                           (str(round(random.randint(10, 100),2)),'RUB', f"{round(random.randint(0, 100))}-test"),
                                                           (str(round(random.randint(10, 100),2)),'RUB', f"{round(random.randint(0, 100))}-test")])
def test_payments_rub_good(amount, currency, description):
    assert requests.get(payment_adapters.PaymentAdapters(amount, currency, description).get_payment_url()).status_code == 200

@pytest.mark.parametrize("amount, currency, description", [(round(random.randint(0, 100),2),'UAH', f'{round(random.randint(0, 100))}-test'),
                                                           (str(round(random.randint(0, 100),2)),'PZL', f"{round(random.randint(0, 100))}-test"),
                                                           (str(round(random.randint(0, 100),2)),'MXN', f"{round(random.randint(0, 100))}-test"),
                                                           (str(round(random.randint(0, 100), 2)), 'BTC', f"{round(random.randint(0, 100))}-test"),
                                                           (str(round(random.randint(0, 100),2)),'BCH', f"{round(random.randint(0, 100))}-test")
                                                           ])
def test_payments_incorrect_currency(amount, currency, description):
    with pytest.raises(TypeError):
        payment_adapters.PaymentAdapters(amount, currency, description).get_payment_url()
    # assert payment_adapters.PaymentAdapters(amount, currency, description).get_payment_url() == '<h>Incorrect currency</h>'

def test_db_worker_good():
    add_payment(round(random.randint(0, 100)), round(random.randint(0, 100),2), 'test', 'TES', datetime.datetime.now(), f'{round(random.randint(0, 100))}-test')

# def test_db_worker_fail():
#     with pytest.raises(NameError or DataError):
#         add_payment(round(random.randint(0, 100)), round(random.randint(0, 100),2), 'test-currency', 'TEST', datetime.datetime.now(), f'{round(random.randint(0, 100))}-test')