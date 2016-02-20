import tweepy
key = "kyq0ISGTw3wcstNioMi79cJ1i"
secret = "NPBfZeCDDGMs7AToHZFDJsLoeO2aCtZHX2JPJCJgjp6pThXydS"
token = "4552115599-IwS61Kgv5w2tcmvOzcVe9nYNoqW55CedJssMmv7"
tokenSecret = "kWtYh2JU7DPWHTUgozFopR6VCIjeGZ3ygQFGfLJlY7KUe"
auth = tweepy.OAuthHandler(key, secret)
auth.set_access_token(token, tokenSecret)
api = tweepy.API(auth)

