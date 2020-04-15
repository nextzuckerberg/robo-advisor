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

def hasNumbers(inputString): #function checks if s string contains some digits taken from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
    return any(char.isdigit() for char in inputString)

#simple function to make sure dividers are of equal length
def divider():
    return "-------------------"

def response(ticker):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
    response  = requests.get(request_url)
    error(response)
    parsed_response = json.loads(response.text)
    return parsed_response

def error(response):
    if "Error Message" in response.text:
        print("Sorry, symbol not found. Please try running the application again with a valid symbol.")
        exit()    

def transform_response(parsed_response):
    tsd = parsed_response["Time Series (Daily)"]
    rows = []
    for date, daily_prices in tsd.items():
        row = {
                
                "timestamp": date,
                "open": daily_prices["1. open"],
                "high": daily_prices["2. high"],
                "low": daily_prices["3. low"],
                "close": daily_prices["4. close"],
                "volume": daily_prices["5. volume"]
                }
        rows.append(row)
    return rows


def write_to_csv(rows, csv_file_path):
    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for row in rows:
            writer.writerow(row)
    return True
                    
def reccommendation(recent_low, latest_closing):
    rec = str
    if float(recent_low)/float(latest_closing) >= 0.8:
        rec = "Buy"
    else:
        rec = "Sell"
    return rec

def reasoning(rec):
    reason = str
    if rec == "Buy":
        reason = "The stock is most likely undervalued. This is because the latest close price is 20% or closer from the 52 week low."
    else:
        reason = "The stock is most likely overvalued. This is because the latest close price is more than 20% away from the 52 week low."
    return reason

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


    parsed_response = response(symbol)

    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
            
    rows = transform_response(parsed_response)

    latest_closing = rows[0]["close"]
    year_high = [row["high"] for row in rows] # list comprehension for mapping purposes!
    year_low = [row["low"] for row in rows] # list comprehension for mapping purposes!
    recent_high = max(year_high)
    recent_low = min(year_low)


    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

    write_to_csv(rows, csv_file_path)
        
    #recommendation
 

    now = datetime.datetime.now()

    print(divider())
    print(f"SELECTED SYMBOL: {symbol}")
    print(divider())
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: " + now.strftime("%Y-%m-%d %I:%M %p"))
    print(divider())
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_closing))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print(divider())
    print(f"RECOMMENDATION: {reccommendation(recent_low,latest_closing)}")
    print(f"RECOMMENDATION REASON: {reasoning(reccommendation)}")
    print(divider())
    print(f"WRITING DATA TO CSV: {os.path.abspath(csv_file_path)}")
    print(divider())

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
    print(divider())


