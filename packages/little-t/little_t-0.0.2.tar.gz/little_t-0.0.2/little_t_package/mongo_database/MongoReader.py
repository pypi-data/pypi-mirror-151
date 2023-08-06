from mongo_database.MongoConnector import MongoConnector
from mongo_database.data import User


class MongoReader():
    def __init__(self) -> None:
        self.connector = MongoConnector()

    def get_user_by_twitter_id(self, twitter_id=None):
        if twitter_id is not None:
            if isinstance(twitter_id, str):
                try:
                    twitter_id = int(twitter_id)
                except TypeError:
                    return None
                cursor = self.connector.user_collection.find_one(
                    {'twitter_id': twitter_id})
                return cursor
        else:
            raise TypeError("Twitter ID Required")

    def get_tweets_by_author_id(self, twitter_id=None):
        if twitter_id is not None:
            if isinstance(twitter_id, int):
                twitter_id = twitter_id
            return self.connector.tweet_collection.find({'author_id': twitter_id})
        else:
            raise TypeError("Twitter ID Required")

    def get_callback_token(self, state):
        try:
            return self.connector.tokens_collection.find_one({'state': state})
        except ValueError:
            return


if __name__ == '__main__':
    foo = MongoReader()
    me = foo.get_user_by_twitter_id(858911602053074944)
    print(foo.get_callback_token(state="8D4WqIyOZPSKAMYplCrbIb8bqufwYx"))
