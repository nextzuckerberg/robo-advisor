

from app.robo_advisor import to_usd, hasNumbers, response


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

