#index.py

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        amount = request.form.get('amount')

        # Validate the symbol
        if not symbol or not get_current_price(symbol):
            message = 'Invalid symbol'
        # Validate the amount
        elif not amount or not amount.isdigit() or float(amount) <= 0:
            message = 'Invalid amount'
        else:
            # Pass the symbol and amount to your strategy
            result = execute_strategy(symbol, float(amount))
            message = f'Trade executed: {result}'
            
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)