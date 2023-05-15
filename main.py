from flask import Flask, jsonify
import requests
import matplotlib.pyplot as plt
import numpy as np
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api/stocks/<symbol>')
def get_stock_data(symbol):
    # Qui puoi integrare la tua API gratuita per i prezzi delle azioni, ad esempio Alpha Vantage
    api_key = 'TI0ZXOUYCFDJ9RJ5'
    base_url = 'https://www.alphavantage.co/query?'
    function = 'TIME_SERIES_DAILY_ADJUSTED'
    datatype = 'json'
    url = f'{base_url}function={function}&symbol={symbol}&apikey={api_key}&datatype={datatype}'
    response = requests.get(url)
    data = response.json()

    ###
    dates, adjusted_close_prices = extract_dates_and_adjusted_close(data)


    # Normalize prices to start at 100
    normalized_prices = normalize_prices(adjusted_close_prices)

    # Calculate statistics
    cumulative_return, annualized_return, annualized_volatility = calculate_statistics(adjusted_close_prices)
    
    # Return JSON
    output_json = {
        "symbol": symbol,
        "dates": dates,
        "normalized_prices": normalized_prices,
        "cumulative_return": cumulative_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility
    }

    # Plot the line chart
#    plt.plot(dates, normalized_prices, label=symbol)
#    plt.xlabel('Dates')
#    plt.ylabel('Normalized Prices')
#    plt.title('Stock Performance')
#    plt.legend()
#    plt.xticks(rotation=45)
#    plt.show()
    ###



    
    return jsonify(output_json)

# A function to extract dates and adjusted close prices from the JSON data
def extract_dates_and_adjusted_close(data):
    time_series = data["Time Series (Daily)"]
    dates = []
    adjusted_close_prices = []

    for date, daily_data in time_series.items():
        dates.append(date)
        adjusted_close_prices.append(float(daily_data["5. adjusted close"]))

    reversed_dates = dates[::-1]
    reversed_adjusted_close_prices = adjusted_close_prices[::-1]
    return reversed_dates, reversed_adjusted_close_prices

# A function to normalize stock prices to start at 100
def normalize_prices(prices):
    base_price = prices[0]
    normalized_prices = [100 * price / base_price for price in prices]
    return normalized_prices



def calculate_statistics(prices):
    # Calculate daily returns
    daily_returns = [prices[i + 1] / prices[i] - 1 for i in range(len(prices) - 1)]

    # Calculate cumulative return
    cumulative_return = (prices[-1] / prices[0]) - 1

    # Calculate annualized return
    num_days = len(daily_returns)
    annualized_return = (1 + cumulative_return) ** (252 / num_days) - 1

    # Calculate annualized volatility
    daily_returns_array = np.array(daily_returns)
    volatility = np.std(daily_returns_array)
    annualized_volatility = volatility * np.sqrt(252)

    return cumulative_return, annualized_return, annualized_volatility

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

