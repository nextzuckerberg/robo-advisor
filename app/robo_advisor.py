# app/robo_advisor.py

import json
import csv
import os
import datetime

from dotenv import load_dotenv
import requests

import pandas as pd
import plotly.graph_objects as go

load_dotenv() #> loads contents of the .env file into the script's environment

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

def hasNumbers(inputString): #taken from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
    return any(char.isdigit() for char in inputString)

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")


#input validation:


if __name__ == "__main__":

    while True:

        symbol = input("Please input a stock symbol: ")
        symbol = symbol.upper()
        
        if hasNumbers(symbol) == True:
            print("Invalid entry. Stock symbol cannot contain a number. Please try again.")
        else:
            break


    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}"
    response  = requests.get(request_url)


    if "Error Message" in response.text:
        print("Sorry, symbol not found. Please try running the application again with a valid symbol.")
        exit()

    parsed_response = json.loads(response.text)

        
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
            

    tsd = parsed_response["Time Series (Daily)"]


    dates = list(tsd.keys())

    latest_day = dates[0] #maybe sort dates later


    latest_closing = tsd[latest_day]["4. close"]

    high_prices = []
    low_prices =  []

    for date in dates:
        high_price = tsd[date]["2. high"]
        high_prices.append(float((high_price)))
        low_price = tsd[date]["3. low"]
        low_prices.append(float((low_price)))

    recent_high = max(high_prices[0:100])
    year_high = max(high_prices[0:252])
    recent_low = min(low_prices[0:100])
    year_low = min(low_prices[0:252])


    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")


    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above

        for date in dates:
            daily_prices = tsd[date]

            writer.writerow({
            
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
            })
        
    #recommendation

    rec = str
    reason = str

    if float(year_low)/float(latest_closing) >= 0.8:
        rec = "Buy"
        reason = "The stock is most likely undervalued. This is because the latest close price is 20% or closer from the 52 week low." #provi
    else:
        rec = "Sell"
        reason = "The stock is most likely overvalued. This is because the latest close price is more than 20% away from the 52 week low." #provide some more explanation


    now = datetime.datetime.now()

    print("-------------------------")
    print(f"SELECTED SYMBOL: {symbol}")
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: " + now.strftime("%Y-%m-%d %I:%M %p"))
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_closing))}")
    print(f"52 WEEK HIGH: {to_usd(float(year_high))}")
    print(f"52 WEEK LOW: {to_usd(float(year_low))}")
    print("-------------------------")
    print(f"RECOMMENDATION: {rec}")
    print(f"RECOMMENDATION REASON: {reason}")
    print("-------------------------")
    print(f"WRITING DATA TO CSV: {os.path.abspath(csv_file_path)}")
    print("-------------------------")



    #The graphs taken from: https://plot.ly/python/plot-data-from-csv/


    while True:

        graphoption = input("Would you like to see the graph for your selected stock? Write 'Yes' or 'No'.")

        graphoption = graphoption.lower().title()

        if graphoption == "Yes":
            print("You should see the graph in your browser. Thank you for using my program!")
            df = pd.read_csv(csv_file_path)

            fig = go.Figure(go.Scatter(x = df['timestamp'], y = df['close'],
                            name='Share Prices (in USD)'))

            fig.update_layout(title= symbol + ' Prices over time (since the first trading day available)',
                            plot_bgcolor='rgb(230, 230,230)',
                            showlegend=True)
            

            fig.show()
            break
        elif graphoption == "No":
            print("Thank you for using my program!")
            break
        else:
            print("Please enter a valid id.")


    print("HAPPY INVESTING!")
    print("-------------------------")
