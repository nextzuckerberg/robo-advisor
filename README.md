# Robo-Advisor Project

## Installation
Fork this repository, clone it (choose a familiar download location such as Desktop). Then, navigate to your repository from command line:
```sh
cd ~/'download location'/robo-advisor
```
## Setup and Security
Consider creating a virtual environment called something like stocks-env:
```sh
conda create -n stocks-env python=3.7 # (first time only)
```
Then, activate your virtual environment:
```sh
conda activate stocks-env
```
From the created virtual environment, install the required packages specified in the "requirements.txt" file you created:
```sh
pip install -r requirements.txt
```
Your program needs an API Key to issue requests to the AlphaVantage API. Program's source code, however, should absolutely not include the secret API Key value. Instead, you should set an environment variable called ALPHAVANTAGE_API_KEY, and your program should read the API Key from this environment variable at run-time.

You need to create an env file and put the following inside:
```sh
ALPHAVANTAGE_API_KEY="your API key"
```

## Usage
To run the script, type the following in the command line:
```sh
python app/robo_advisor.py
```

No you should be able to enter a stock ticker. 
The program will return the latest close price, 52 week high, 52 week low, and recommendation. Also, if you want to the program will return the graph with the stock prices over time.

if you have any questions regarding the application, please contact me at stocks@wallstreet.edu