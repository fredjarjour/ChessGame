import requests
import time
from threading import Thread

def print_response(resp):
    print('--- NETWORK REQUEST ---')
    print(f'Status code: {resp.status_code}')
    print('Network response: ')
    print(resp.text)
    print('-----------------------')


def login(session, username):
    login_data = {
        'user': username
    }
    r = session.post(login_url, login_data)
    print()
    print(f'Description: Logging in {username}')
    print_response(r)

def move(session, from_coord, to_coord):
    move_data = {
        'from': from_coord,
        'to': to_coord
    }
    r = session.post(submit_move_url, move_data)
    
    print()
    print(f'Description: Moving from {from_coord} to {to_coord}')
    print_response(r)

def wait_for_move(session: requests.Session):
    r = session.get(get_move_url)
    print()
    print(f'Description: Received move {r.text}')
    print_response(r)

def get_time_left(player):
    r = requests.post(get_time_left_url, {'player': player})
    print()
    print(f'Description: Getting seconds left for player: {player}')
    print_response(r)

# useful url's
login_url = "http://localhost:5000/login"
submit_move_url = "http://localhost:5000/submitmove"
get_time_left_url = "http://localhost:5000/gettimeleft"
get_move_url = "http://localhost:5000/getmove"

def magnus_thread():
    session = requests.Session()
    username = "Magnus"

    login(session, username)

    # wait for black to login
    time.sleep(1)

    # send a move and start listening for the opp's move
    move(session, 'e2', 'e4')
    wait_for_move(session)

    # think about your next move
    time.sleep(1)

    move(session, 'c2', 'c4')
    wait_for_move(session)

    # think about your next move
    time.sleep(1)

    move(session, 'h2', 'h3')
    # wait_for_move(session)

    # ... and so on

def hikaru_thread():
    session = requests.Session()
    username = "Hikaru"

    # wait for white player to log in, then log in
    time.sleep(0.5)
    login(session, username)

    # black player starts listening for white's move
    wait_for_move(session)

    # think about next move
    time.sleep(1)

    # black player moves after receiving the move
    move(session, 'e7', 'e5')
    wait_for_move(session)
    
    # think about next move
    time.sleep(1)

    move(session, 'h7', 'h5')

    # ... and so on

white_thread = Thread(target=magnus_thread)
black_thread = Thread(target=hikaru_thread)
white_thread.start()
black_thread.start()

white_thread.join()
black_thread.join()

print("Any player, regardless of login status can query the timer")
print("White player seconds left:")
get_time_left('w')

print("Black player seconds left:")
get_time_left('b')