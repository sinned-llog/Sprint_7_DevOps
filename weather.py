import requests
from pprint import pprint

response = requests.get(
    url="https://api.openweathermap.org/data/2.5/weather",
    params={
        "q": "Bretten",
        "appid": "7e504b9564034e82eed30bee738c9a1d"
    }
)

print(response.status_code)
pprint(response.json())