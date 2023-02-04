import requests

url = "http://localhost:5000/submitmove"

data = {
    "from": 'e7',
    "to": 'e6',
    # "promote": "Q"
}

r = requests.post(url, data)

print(r.status_code)
print(r.headers)
print(r.text)

url = "http://localhost:5000/gettimeleft"

data = {
    "player": 1
}

r = requests.post(url, data)
print(r.status_code)
print(r.headers)
print(r.text)