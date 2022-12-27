import requests
import sys


class InstagramBot:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.access_token = None
        self.user_id = None
        self.csrftoken = None
        self.session_id = None

    def login(self, username: str, password: str):
        response = requests.post('https://www.instagram.com/accounts/login/ajax/', json={
            'username': username,
            'password': password
        })

        if response.status_code == 200:
            self.user_id = response.cookies['ds_user_id']
            self.session_id = response.cookies['sessionid']
            self.csrftoken = response.headers['csrftoken']
        else:
            print('Login failed')

    def authenticate(self, username: str, password: str):
        endpoint = "https://www.instagram.com/accounts/login/ajax/"
        headers = {
            "referer": "https://www.instagram.com/",
            "x-csrftoken": self.csrftoken,
            "x-instagram-ajax": "1",
            "x-requested-with": "XMLHttpRequest",
        }
        payload = {
            "username": username,
            "password": password,
            "api_key": self.api_key,
        }
        response = requests.post(endpoint, headers=headers, data=payload)

        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
            self.user_id = response.json()["user_id"]
            self.csrftoken = response.cookies["csrftoken"]
            self.session_id = response.cookies["sessionid"]
            return True
        else:
            return False

    def follow(self, username: str):
        user_id = self.get_user_id(username)

        response = requests.post(f'https://www.instagram.com/web/friendships/{user_id}/follow/', headers={
            'x-csrftoken': self.csrftoken,
            'x-requested-with': 'XMLHttpRequest'
        })

        if response.status_code == 200:
            print(f'Followed {username}')
        else:
            print('Follow failed')

    def unfollow(self, username: str):
        user_id = self.get_user_id(username)

        response = requests.post(f'https://www.instagram.com/web/friendships/{user_id}/unfollow/', headers={
            'x-csrftoken': self.csrftoken,
            'x-requested-with': 'XMLHttpRequest'
        })

        if response.status_code == 200:
            print(f'Unfollowed {username}')
        else:
            print('Unfollow failed')

    def get_user_id(self, username: str):
        response = requests.get(f"https://api.instagram.com/v1/users/search?q={username}&access_token={self.api_key}")
        data = response.json()
        user_info = data['data']

        print(f"Username: {user_info['username']}")
        print(f"Full name: {user_info['full_name']}")
        print(f"Profile picture: {user_info['profile_picture']}")
        print(f"Bio: {user_info['bio']}")

        return user_info

    def get_media_items(self, username: str):
        user_id = self.get_user_id(username)

        response = requests.get(
            f"https://api.instagram.com/v1/users/{user_id}/media/recent?access_token={self.api_key}")
        data = response.json()
        media_items = data['data']

        for media_item in media_items:
            print(f"Media item ID: {media_item['id']}")
            print(f"Media item type: {media_item['type']}")
            print(f"Media item link: {media_item['link']}")
            print(f"Media item caption: {media_item['caption']['text']}")
            print()

        return media_items

    def get_media_item_comments(self, media_item_id: str):
        response = requests.get(
            f"https://api.instagram.com/v1/media/{media_item_id}/comments?access_token={self.api_key}")
        data = response.json()
        comments = data['data']

        for comment in comments:
            print(f"Commenter: {comment['from']['username']}")
            print(f"Comment: {comment['text']}")
            print()

        return comments

    def get_media_item_likes(self, media_item_id: str):
        response = requests.get(f"https://api.instagram.com/v1/media/{media_item_id}/likes?access_token={self.api_key}")
        data = response.json()
        likes = data['data']

        for like in likes:
            print(f"Liker: {like['username']}")

        return likes

    def search(self, query: str, type: str):
        if type == "user":
            type_param = "users"
        elif type == "hashtag":
            type_param = "tags"
        elif type == "place":
            type_param = "places"
        else:
            raise ValueError("Invalid search type")

        response = requests.get(
            f"https://api.instagram.com/v1/{type_param}/search?q={query}&access_token={self.api_key}")
        data = response.json()
        search_results = data['data']

        for search_result in search_results:
            if type == "user":
                print(f"Username: {search_result['username']}")
            elif type == "hashtag":
                print(f"Hashtag: {search_result['name']}")
            elif type == "place":
                print(f"Place: {search_result['name']}")

        return search_results

    def get_followers(self, username: str):
        response = requests.get(
            f"https://api.instagram.com/v1/users/self/followed-by?access_token={self.api_key}&username={username}")
        data = response.json()
        followers = data['data']

        for follower in followers:
            print(follower['username'])

        return followers

    def get_following(self, username: str):
        response = requests.get(
            f"https://api.instagram.com/v1/users/self/follows?access_token={self.api_key}&username={username}")
        data = response.json()
        following = data['data']

        for account in following:
            print(account['username'])

        return following

    def get_non_followers(self, username: str):
        response = requests.get(
            f"https://api.instagram.com/v1/users/self/followed-by?access_token={self.api_key}&username={username}")
        followers = {follower['username'] for follower in response.json()['data']}

        response = requests.get(
            f"https://api.instagram.com/v1/users/self/follows?access_token={self.api_key}&username={username}")
        following = {account['username'] for account in response.json()['data']}
        non_followers = followers - following

        for non_follower in non_followers:
            print(non_follower)

        return non_followers

    def like(self, media_item_id: str):
        endpoint = f"https://api.instagram.com/v1/media/{media_item_id}/likes"
        headers = {
            "referer": f"https://www.instagram.com/p/{media_item_id}/",
            "x-csrftoken": self.csrftoken,
            "x-instagram-ajax": "1",
            "x-requested-with": "XMLHttpRequest",
        }
        payload = {
            "access_token": self.access_token,
            "user_id": self.user_id,
        }
        response = requests.post(endpoint, headers=headers, data=payload)

        if response.status_code == 200:
            return True
        else:
            return False

    def unlike(self, media_item_id: str):
        endpoint = f"https://api.instagram.com/v1/media/{media_item_id}/likes"
        headers = {
            "referer": f"https://www.instagram.com/p/{media_item_id}/",
            "x-csrftoken": self.csrftoken,
            "x-instagram-ajax": "1",
            "x-requested-with": "XMLHttpRequest",
        }
        payload = {
            "access_token": self.access_token,
            "user_id": self.user_id,
        }
        response = requests.delete(endpoint, headers=headers, data=payload)

        if response.status_code == 200:
            return True
        else:
            return False


api_key_ = ""
bot = InstagramBot(api_key_)

username_ = sys.argv[1]
followers_ = bot.get_followers(username_)
following_ = bot.get_following(username_)
non_followers_ = bot.get_non_followers(username_)
media_items_ = bot.get_media_items(username_)

# media_item_id = ""
# comments_ = bot.get_media_item_comments(media_item_id_)
# likes_ = bot.get_media_item_likes(media_item_id_)

# query_ = ""
# search_type_ = ""  # "user", "hashtag", or "place"
# search_results_ = bot.search(query_, search_type_)