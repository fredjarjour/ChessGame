import requests

def print_response(resp):
    print(f'Status: {resp.status_code}')
    print(resp.text)
    print('----------')

# useful url's
login = "http://localhost:5000/login"
submit_move = "http://localhost:5000/submitmove"
get_time_left = "http://localhost:5000/gettimeleft"

# create a session for each player to automatically handle cookies
white_session = requests.Session()
white_username = "Magnus"
black_session = requests.Session()
black_username = "Hikaru"

print("White player logs in")
login_data = {
    'user': white_username
}
r = white_session.post(login, login_data)
print_response(r)

print("Black player logs in")
login_data = {
    'user': black_username
}
r = black_session.post(login, login_data)
print_response(r)


print("White player moves from e2 to e4")
move_data = {
    'from': 'e2',
    'to': 'e4'
}
r = white_session.post(submit_move, move_data)
print_response(r)

print("Black player moves from e7 to e5")
move_data = {
    'from': 'e7',
    'to': 'e5'
}
r = black_session.post(submit_move, move_data)
print_response(r)
def print_response(resp):
    print(f'Status: {resp.status_code}')
    print(resp.text)
    print('----------')

# useful url's
login = "http://localhost:5000/login"
submit_move = "http://localhost:5000/submitmove"
get_time_left = "http://localhost:5000/gettimeleft"

# create a session for each player to automatically handle cookies
white_session = requests.Session()
white_username = "Magnus"
black_session = requests.Session()
black_username = "Hikaru"

print("White player logs in")
login_data = {
    'user': white_username
}
r = white_session.post(login, login_data)
print_response(r)

print("Black player logs in")
login_data = {
    'user': black_username
}
r = black_session.post(login, login_data)
print_response(r)


print("White player moves from e2 to e4")
move_data = {
    'from': 'e2',
    'to': 'e4'
}
r = white_session.post(submit_move, move_data)
print_response(r)

print("Black player moves from e7 to e5")
move_data = {
    'from': 'e7',
    'to': 'e5'
}
r = black_session.post(submit_move, move_data)
print_response(r)

print("If black player tries to move out of turn")
move_data = {
    'from': 'a7',
    'to': 'a6'
}
r = black_session.post(submit_move, move_data)
print_response(r)
r = black_session.post(submit_move, move_data)
print_response(r)

print("But after the white player plays")
move_data = {
    'from': 'a2',
    'to': 'a3'
}
r = white_session.post(submit_move, move_data)
print_response(r)
print("But after the white player plays")
move_data = {
    'from': 'a2',
    'to': 'a3'
}
r = white_session.post(submit_move, move_data)
print_response(r)

print("The black player's move get's through")
move_data = {
    'from': 'a7',
    'to': 'a6'
}
r = black_session.post(submit_move, move_data)
print_response(r)
print("The black player's move get's through")
move_data = {
    'from': 'a7',
    'to': 'a6'
}
r = black_session.post(submit_move, move_data)
print_response(r)

print("If the player gives an illegal move")
move_data = {
    'from': 'h8',
    'to': 'a1'
}
r = white_session.post(submit_move, move_data)
print_response(r)
print("If the player gives an illegal move")
move_data = {
    'from': 'h8',
    'to': 'a1'
}
r = white_session.post(submit_move, move_data)
print_response(r)

print("Any player, regardless of login status can query the timer")
print("White player seconds left:")
time_data = {
    'player': 'w'
}
r = requests.post(get_time_left, time_data)
print_response(r)
r = requests.post(get_time_left, time_data)
print_response(r)

print("Black player seconds left:")
time_data = {
    'player': 'b'
}
r = requests.post(get_time_left, time_data)
print_response(r)