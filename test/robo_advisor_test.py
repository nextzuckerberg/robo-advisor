import os
import pytest



from app.robo_advisor import to_usd, hasNumbers, response, write_to_csv, reccommendation, reasoning, divider



def test_to_usd():
    # it should apply USD formatting
    assert to_usd(4.50) == "$4.50"

    # it should display two decimal places
    assert to_usd(4.5) == "$4.50"

    # it should round to two places
    assert to_usd(4.55555) == "$4.56"

    # it should display thousands separators
    assert to_usd(1234567890.5555555) == "$1,234,567,890.56"

def test_hasNumbers():

    #should say True as there are some digits in the string
    assert hasNumbers("123as") == True

    #should say True as there are some digits in the string
    assert hasNumbers("12356") == True

    #should say False as there are no digits in the string
    assert hasNumbers("arhrs") == False


def test_response():
    #testing if function returns expected data in an expected format

    ticker = "MA"

    parsed_response = response(ticker)

    assert isinstance(parsed_response, dict)
    assert "Meta Data" in parsed_response.keys()
    assert "Time Series (Daily)" in parsed_response.keys()
    assert parsed_response["Meta Data"]["2. Symbol"] == ticker



def test_write_to_csv():

    # SETUP

    example_rows = [
        {"timestamp": "2019-06-08", "open": "101.0924", "high": "101.9500", "low": "100.5400", "close": "101.6300", "volume": "22165128"},
        {"timestamp": "2019-06-07", "open": "102.6500", "high": "102.6900", "low": "100.3800", "close": "100.8800", "volume": "28232197"},
        {"timestamp": "2019-06-06", "open": "102.4800", "high": "102.6000", "low": "101.9000", "close": "102.4900", "volume": "21122917"},
        {"timestamp": "2019-06-05", "open": "102.0000", "high": "102.3300", "low": "101.5300", "close": "102.1900", "volume": "23514402"},
        {"timestamp": "2019-06-04", "open": "101.2600", "high": "101.8600", "low": "100.8510", "close": "101.6700", "volume": "27281623"},
        {"timestamp": "2019-06-01", "open": '99.2798',  "high": "100.8600", "low": "99.1700",  "close": "100.7900", "volume": "28655624"}
    ]

    csv_filepath = os.path.join(os.path.dirname(__file__), "example_reports", "prices2.csv")

    if os.path.isfile(csv_filepath):
        os.remove(csv_filepath)

    assert os.path.isfile(csv_filepath) == False # just making sure the test was setup properly

    # INVOCATION

    result = write_to_csv(example_rows, csv_filepath)

    # EXPECTATIONS

    assert result == True
    assert os.path.isfile(csv_filepath) == True
    # TODO: consider also testing the file contents!


def test_reccommendation():
    assert reccommendation(10,11) == "Buy"
    assert reccommendation(10,30) == "Sell"

def test_reasoning():
    assert reasoning("Buy") == "The stock is most likely undervalued. This is because the latest close price is 20% or closer from the 52 week low."
    assert reasoning("Sell") == "The stock is most likely overvalued. This is because the latest close price is more than 20% away from the 52 week low."

def test_divider():
    assert divider() == "-------------------"
