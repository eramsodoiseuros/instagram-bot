import requests
from requests.structures import CaseInsensitiveDict
import json
import sys


class InstagramBot:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.user_id = None
        self.csrftoken = None
        self.session_id = None

    def login(self):
        response = requests.post('https://www.instagram.com/accounts/login/ajax/', json={
            'username': self.username,
            'password': self.password
        })

        if response.status_code == 200:
            # Extract the user's ID and session ID from the response cookies
            self.user_id = response.cookies['ds_user_id']
            self.session_id = response.cookies['sessionid']

            # Set the csrftoken to the value provided in the response headers
            self.csrftoken = response.headers['csrftoken']
        else:
            print('Login failed')

    def track_followers(self, user_id: str):
        query_params = {
            'user_id': user_id
        }

        headers = CaseInsensitiveDict()
        headers['X-CSRFToken'] = self.csrftoken
        headers['X-Instagram-AJAX'] = '1'
        headers['X-Requested-With'] = 'XMLHttpRequest'

        response = requests.get('https://www.instagram.com/query/', params=query_params, headers=headers)

        data = json.loads(response.text)

        followers = data['followers']

        for follower in followers:
            print(follower['username'])

        return followers


YOUR_USERNAME = sys.argv[1]
YOUR_PASSWORD = sys.argv[2]

bot = InstagramBot(YOUR_USERNAME, YOUR_PASSWORD)
bot.login()

response_ = requests.get(f"https://www.instagram.com/{YOUR_USERNAME}/?__a=1")
data_ = json.loads(response_.text)
user_id = data_['graphql']['user']['id']

followers_ = bot.track_followers(user_id)
