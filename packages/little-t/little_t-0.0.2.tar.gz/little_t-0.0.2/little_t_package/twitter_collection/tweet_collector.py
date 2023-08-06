import requests
from tweepy.cursor import Cursor
from configs.api_keys import TwitterKeys, AWSKeys
import tweepy
import tweepy.errors
import mongo_database.MongoReader


class TwitterAPIConnector():
    def __init__(self) -> None:
        self.client = tweepy.Client(
            bearer_token=TwitterKeys.get_BEARER_TOKEN(), wait_on_rate_limit=True)

    def get_user(self, *, id=None, username=None):
        if id is not None:
            try:
                response = self.client.get_user(id=id)
                return response
            except tweepy.errors.BadRequest:
                return
        elif username is not None:
            try:
                if username[0] == '@':
                    username = username[1:]
                response = self.client.get_user(username=username)
                return response
            except tweepy.errors.BadRequest:
                return
        else:
            raise TypeError("ID or username is required")

    def get_tweets(self, *, id=None, username=None, amount: int = 3, repeat=False):
        if id is not None:
            user = self.get_user(id=id)
            if user == None:
                raise ValueError(f"Could not get {id}'s data")

        elif username is not None:
            user = self.get_user(username=username)
            if user == None:
                raise ValueError(f"Could not get {username}'s data")
        else:
            raise TypeError("ID or username is required")

        if repeat:
            exclude = ["retweets", "replies"]
            max_results = 100
            response_list = []
            for response in tweepy.Paginator(self.client.get_users_tweets,
                                             user.data['id'],
                                             max_results=max_results,
                                             exclude=exclude).flatten(1000):
                response_list.append(response)
            return response_list
        else:
            return self.client.get_users_tweets(user.data['id'], exclude=["replies", "retweets"])

    def get_oauth_tokens(self):
        client = TwitterKeys.get_CLIENT_ID()
        client_secret = TwitterKeys.get_CLIENT_SECRET()
        redirect_uri = AWSKeys.get_API_URL() + 'callback'
        scope = ["tweet.read", "tweet.write", "users.read", "offline.access"]
        user_handler = tweepy.OAuth2UserHandler(client_id=client, scope=scope,
                                                redirect_uri=redirect_uri,
                                                client_secret=client_secret
                                                )
        #auth = user_handler.get_authorization_url()
        mr = mongo_database.MongoReader.MongoReader()
        foo = user_handler.authorization_url(url=redirect_uri, state="8D4WqIyOZPSKAMYplCrbIb8bqufwYx")
        print(foo) 


if __name__ == '__main__':
    #target = input("Give User: ")
    api = TwitterAPIConnector()
    # target = "@biggayduck"
    # response = api.get_user(username=target)
    # foo = api.get_tweets(id=response.data['id'], repeat=True)
    # for tweet in foo:
    #     print(tweet.id)
    print(api.get_oauth_tokens())

