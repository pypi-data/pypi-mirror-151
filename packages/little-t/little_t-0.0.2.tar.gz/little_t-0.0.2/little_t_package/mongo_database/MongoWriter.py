from mongo_database.MongoConnector import MongoConnector
from mongo_database.data import User, CallbackToken
from mongo_database.data.Tweet import Tweet
from twitter_collection import tweet_collector
import pymongo.errors
import datetime


class MongoWriter():

    def __init__(self) -> None:
        self.connector = MongoConnector()
        self.tw_collector = tweet_collector.TwitterAPIConnector()

    def insert_twitter_user(self, twitter_id=None, twitter_username=None) -> None:

        # Handle if ID or Username
        if twitter_id is not None:
            user_response = self.tw_collector.get_user(id=twitter_id)
        elif twitter_username is not None:
            user_response = self.tw_collector.get_user(
                username=twitter_username)
        else:
            raise TypeError("Twitter ID or Username required")

        # Wrap data to document object for upload
        new_twitter_user = User.TwitterUser()
        new_twitter_user.twitter_id = user_response.data['id']
        new_twitter_user.username = user_response.data['username']
        new_twitter_user.last_updated = datetime.datetime.now()

        try:
            self.connector.user_collection.insert_one(
                new_twitter_user.to_mongo())
        except pymongo.errors.DuplicateKeyError:
            return

    def insert_new_tweets(self, twitter_id=None, twitter_username=None, new_user=False):
        if twitter_id is not None:
            user_info = self.tw_collector.get_user(id=twitter_id)
            if self.connector.user_collection.find_one({"twitter_id": twitter_id}) == None:
                self.insert_twitter_user(twitter_id=twitter_id)

        elif twitter_username is not None:
            user_info = self.tw_collector.get_user(
                username=twitter_username)
            if twitter_username[0] == '@':
                twitter_username = twitter_username[1:]
            if self.connector.user_collection.find_one({"username": twitter_username}) == None:
                self.insert_twitter_user(twitter_username=twitter_username)
        else:
            raise TypeError("Twitter ID or Username required")

        initial_response = self.tw_collector.get_tweets(
            id=user_info.data['id'], amount=10)
        oldest_tweet = initial_response.meta['oldest_id']

        if self.connector.tweet_collection.find_one({"tweet_id": int(oldest_tweet)}) != None:
            return

        tweet_list = self.tw_collector.get_tweets(
            id=user_info.data['id'], amount=100, repeat=True)
        new_mongo_tweet_list = []
        for i, tweet in enumerate(tweet_list):
            mongo_tweet = Tweet()
            mongo_tweet.author_id = user_info.data['id']
            mongo_tweet.tweet_id = tweet.data['id']
            mongo_tweet.text = tweet.data['text']
            new_mongo_tweet_list.append(mongo_tweet.to_mongo())
        self.connector.tweet_collection.insert_many(new_mongo_tweet_list)

    def insert_callback_token(self, code, state):
        token_data = CallbackToken.CallbackToken()
        token_data.state = state
        token_data.code = code
        token_data.insert_date = datetime.datetime.now()
        try:
            self.connector.tokens_collection.insert_one(token_data.to_mongo())
        except pymongo.errors.DuplicateKeyError:
            return


if __name__ == '__main__':
    writer = MongoWriter()
    # writer.insert_twitter_user(twitter_username="@KusaAlexM")
    # writer.insert_new_tweets(twitter_username="@ElonMusk")
