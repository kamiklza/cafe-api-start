import requests

params = {
    "location": "Hong Kong"
}

response = requests.get(url="google.com.hk", params=params)

print(response)