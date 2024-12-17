import requests

url = 'https://www.google.com'
response_google = requests.post(url)
print(response_google) ## 200 é ok
