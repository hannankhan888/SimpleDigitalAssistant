import yfinance as yf
import csv


def get_symbol(company_name: str) -> str:
    try:
        with open('symbols.csv', mode='r') as inp:
            reader = csv.reader(inp)
            stock_dict = {rows[0]: rows[1] for rows in reader}
        stock_lower_dict = {k.lower(): v for(k, v) in stock_dict.items()}
        return stock_lower_dict.get(company_name)

    except:
        return "none"


user_inquiry = input("What company stock price would you like to know about: ").lower()
if get_symbol(user_inquiry) != "none":
    company = yf.Ticker(get_symbol(user_inquiry))

    print(company.info['shortName'] + " (" + company.info['symbol'] + ")")
    print("Current Price: ", company.info['currentPrice'])
    print("Recommendation: ", company.info['recommendationKey'])
else:
    print("The company symbol cannot be found.   ")
