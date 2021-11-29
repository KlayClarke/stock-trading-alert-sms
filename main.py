import os
import requests
import itertools

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

AV_API_KEY = os.environ.get('AV_API_KEY')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

STOCK_ENDPOINT = 'https://www.alphavantage.co/query'
NEWS_ENDPOINT = 'https://newsapi.org/v2/everything'

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

parameters = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK,
    'apikey': 'AZP3JTBNUHAOYIYP'
}

response = requests.get(url=STOCK_ENDPOINT, params=parameters)
data = response.json()
daily_data = data['Time Series (Daily)']
two_day_data = dict(itertools.islice(daily_data.items(), 2))

two_day_close_list = []

for date in two_day_data:
    two_day_close_list.append(float(two_day_data[date]['4. close']))

close_diff = abs(two_day_close_list[1] - two_day_close_list[0])
percent_change = (close_diff / two_day_close_list[1])
print(percent_change)

if percent_change > .05:
    print('Get News')

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
