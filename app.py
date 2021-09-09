from flask import Flask, render_template, request, redirect
import logging, os
from adapters import payment_adapters

app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        try:
            result = payment_adapters.PaymentAdapters(request.form['amount'], request.form['currency'],
                                             request.form['descriptions']).get_payment_url()
            if 'form' in result:
                return result
            else:
                return redirect(result)
        except Exception as e:
            logging.error(e)
    elif request.method == 'GET':
        return render_template('index.html')

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    if os.environ.get('ENV') == "heroku":
        app.run(debug=False)
    else:
        app.run(host="0.0.0.0", port="5000",debug=True)
