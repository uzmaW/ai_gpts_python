import requests
import json 
from settings import FMP_API_KEY
# Define financial statement functions
def get_income_statement(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())

def get_balance_sheet(ticker, period, limit):
    # Code to fetch and return cash flow statement
    pass
def get_cash_flow_statement(ticker, period, limit):
    # Code to fetch and return cash flow statement
    pass
def get_key_metrics(ticker, period, limit):
    # Code to fetch and return cash flow statement
    pass
def get_financial_ratios(ticker, period, limit):
    # Code to fetch and return cash flow statement
    pass
def get_financial_growth(ticker, period, limit):
    # Code to fetch and return cash flow statement
    pass


# Map available functions
available_functions = {
    "get_income_statement": get_income_statement,
    "get_balance_sheet": get_balance_sheet,
    "get_cash_flow_statement": get_cash_flow_statement,
    "get_key_metrics": get_key_metrics,
    "get_financial_ratios": get_cash_flow_statement,
    "get_financial_growth": get_financial_ratios
}