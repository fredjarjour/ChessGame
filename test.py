import requests

# url = "http://localhost:5000/submitmove"

# data = {
#     "from": 'e2',
#     "to": 'e4'
# }

# r = requests.post(url, data)

# print(r.status_code)
# print(r.headers)
# print(r.text)

url = "http://localhost:5000/gettimeleft"

data = {
    "player": 1
}

r = requests.post(url, data)
print(r.status_code)
print(r.headers)
print(r.text)