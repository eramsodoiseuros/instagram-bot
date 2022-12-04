# Instagram Bot to track Followers

The bot will track the followers of the Instagram user specified by the `YOUR_USERNAME` variable.
To get the user's ID, it makes a `GET request to the https://www.instagram.com/{username}/?__a=1 endpoint`, where `username` is the username of the user you want to track. The `response` to this request contains the user's ID, which is then used to make a request to the `followers endpoint` to get the list of followers.
The followers are printed and returned by the track_followers() method.
