import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_api_key = "stock_api_key"
news_api_key = "news_api_key"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

account_sid = "account_sid"
auth_token = "auth_token"
client = Client(account_sid, auth_token)

stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key
}

news_parameters = {
    "q": "Tesla",
    "from": "2023-01-06",
    "sortBy": "popularity",
    "apiKey": news_api_key
}


new_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
new_response.raise_for_status()
news_data = new_response.json()
recent_article = news_data["articles"][0]
recent_article_information = f"{recent_article['title']}: {recent_article['description']}"

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()

stock_data = stock_response.json()["Time Series (Daily)"]
data_list = [value for key, value in stock_data.items()]
yesterday_close = data_list[0]['4. close']
day_before_close = data_list[1]['4. close']

difference = round(float(yesterday_close)-float(day_before_close), 2)
percent = round((difference/float(yesterday_close) * 100), 2)

if percent > 4:
    message = client.messages \
        .create(
        body=f"TSLA: %{percent} change, {recent_article_information}",
        from_='+19853085624',
        to='+14086470905'
    )
    print(message.status)


