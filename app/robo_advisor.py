# app/robo_advisor.py

import json
import csv

import requests


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71




request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
response  = requests.get(request_url)


parsed_response = json.loads(response.text)


last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]


tsd = parsed_response["Time Series (Daily)"]


dates = list(tsd.keys())

latest_day = dates[0] #maybe sort dates later


#breakpoint()


latest_closing = tsd[latest_day]["4. close"]

high_prices = []
low_prices =  []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float((high_price)))
    low_price = tsd[date]["3. low"]
    low_prices.append(float((low_price)))

recent_high = max(high_prices)
recent_low = min(low_prices)


    


recent_high = max(high_prices)



 



print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_closing))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("WRITING DATA TO CSV")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


csv_file_path = "data/prices.csv" # a relative filepath

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=["city", "name"])
    writer.writeheader() # uses fieldnames set above
    writer.writerow({"city": "New York", "name": "Yankees"})
    writer.writerow({"city": "New York", "name": "Mets"})
    writer.writerow({"city": "Boston", "name": "Red Sox"})
    writer.writerow({"city": "New Haven", "name": "Ravens"})