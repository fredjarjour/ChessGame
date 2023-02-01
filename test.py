import requests

url = "http://localhost:5000/submitmove"

data = {
    "from": 'e2',
    "to": 'e4'
}

r = requests.post(url, data)