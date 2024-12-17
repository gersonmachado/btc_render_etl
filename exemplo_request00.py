import requests

url = 'https://api.coinbase.com/v2/prices/spot'
response = requests.get(url)
print(response) ## 200 é ok

url = 'https://www.google.com'
response_google = requests.post(url)
print(response_google) ## 200 é ok
