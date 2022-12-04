import requests
from requests.structures import CaseInsensitiveDict
import json


class InstagramBot:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.user_id = None
        self.csrftoken = None
        self.session_id = None

    def login(self):
        # First, get the user's ID, csrftoken, and session ID by making a request to the login page
        response = requests.get('https://www.instagram.com/accounts/login/')

        # Extract the user's ID, csrftoken, and session ID from the response headers
        self.user_id = response.cookies['ds_user_id']
        self.csrftoken = response.cookies['csrftoken']
        self.session_id = response.cookies['sessionid']

        # Set up the login payload
        login_payload = {
            'username': self.username,
            'password': self.password
        }

        # Set up the login headers
        login_headers = CaseInsensitiveDict()
        login_headers['X-CSRFToken'] = self.csrftoken
        login_headers['Referer'] = 'https://www.instagram.com/accounts/login/'

        # Make a POST request to the login endpoint to log in to the Instagram account
        response = requests.post('https://www.instagram.com/accounts/login/ajax/', data=login_payload,
                                 headers=login_headers)

        # If the login was successful, the response will have a 200 status code

    def track_followers(self, user_id: str):
        # Set up the query parameters for the request
        query_params = {
            'user_id': user_id
        }

        # Set up the request headers
        headers = CaseInsensitiveDict()
        headers['X-CSRFToken'] = self.csrftoken
        headers['X-Instagram-AJAX'] = '1'
        headers['X-Requested-With'] = 'XMLHttpRequest'

        # Make a GET request to the followers endpoint to get the list of followers
        response = requests.get('https://www.instagram.com/query/', params=query_params, headers=headers)

        # Parse the response data
        data = json.loads(response.text)

        # Get the list of followers from the response data
        followers = data['followers']

        # Print the list of followers
        for follower in followers:
            print(follower['username'])

        # Return the list of followers
        return followers



YOUR_USERNAME = ""
YOUR_PASSWORD = ""

bot = InstagramBot(YOUR_USERNAME, YOUR_PASSWORD)
bot.login()

response = requests.get(f"https://www.instagram.com/{YOUR_USERNAME}/?__a=1")
data = json.loads(response.text)
user_id = data['graphql']['user']['id']

followers = bot.track_followers(user_id)