import os
import requests
import itertools
from twilio.rest import Client

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
if percent_change < 0:
    CHANGE_DIRECTIONAL = '🔻'
elif percent_change > 0:
    CHANGE_DIRECTIONAL = '🔺'

percent_change_formatted = abs(round((percent_change * 100), 2))
articles_formatted = [f'{STOCK}: {CHANGE_DIRECTIONAL}{percent_change_formatted}\n'
                      f'Headline:{article["title"]}\nBrief: {article["description"]}' for article in articles]

if substantial_change:
    for article in articles_formatted:
        client = Client(twilio_account_sid, twilio_auth_token)
        message = client.messages \
            .create(
            body=article,
            from_=f'{twilio_phone_number}',
            to=f'{PERSONAL_PHONE_NUMBER}'
        )
