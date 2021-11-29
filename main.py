import os
import requests
import itertools
from twilio.rest import Client


UP_CHANGE_SIGN = '🔺'
DOWN_CHANGE_SIGN = '🔻'
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

twilio_account_sid = os.environ.get('ACCOUNT_SID')
twilio_auth_token = os.environ.get('AUTH_TOKEN')
twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

PERSONAL_PHONE_NUMBER = os.environ.get('PERSONAL_PHONE_NUMBER')

AV_API_KEY = os.environ.get('AV_API_KEY')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

STOCK_ENDPOINT = 'https://www.alphavantage.co/query'
NEWS_ENDPOINT = 'https://newsapi.org/v2/everything'

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

parameters = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK,
    'apikey': AV_API_KEY
}

response = requests.get(url=STOCK_ENDPOINT, params=parameters)
data = response.json()
daily_data = data['Time Series (Daily)']
two_day_data = dict(itertools.islice(daily_data.items(), 2))

two_day_close_price = []
two_day_dates_list = []

for date in two_day_data:
    two_day_dates_list.append(date)
    two_day_close_price.append(float(two_day_data[date]['4. close']))

close_diff = two_day_close_price[0] - two_day_close_price[1]
percent_change = (close_diff / two_day_close_price[1])

print(close_diff)
print(percent_change)
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

news_api_parameters = {
    'q': STOCK,
    'from': two_day_dates_list[0],
    'sortBy': 'popularity',
    'apikey': NEWS_API_KEY
}

news_response = requests.get(url=NEWS_ENDPOINT, params=news_api_parameters)
news_data = news_response.json()

articles = news_data['articles'][:3]

substantial_change = False

if percent_change < -.03 or percent_change > .03:
    substantial_change = True
    print('Substantial Change is TRUE')

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

CHANGE_DIRECTIONAL = None

percent_change_formatted = abs(round((percent_change * 100), 2))



if substantial_change:
    for article in articles:
        title = article['title']
        description = article['description']
        if percent_change < 0:
            CHANGE_DIRECTIONAL = DOWN_CHANGE_SIGN
        elif percent_change > 0:
            CHANGE_DIRECTIONAL = UP_CHANGE_SIGN
        print(f'{STOCK}: {CHANGE_DIRECTIONAL}{percent_change_formatted}\n'
              f'Headline:{title}\nBrief: {description}')


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
