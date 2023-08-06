import pymongo
from configs.api_keys import MongoKeys


class MongoConnector():
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(
            f"mongodb+srv://little_t:{MongoKeys.get_cluster_password()}@clustertwitter.vd6bg.mongodb.net/ClusterTwitter?retryWrites=true&w=majority")
        self.db = self.client['tweetDB']
        self.user_collection = self.db['UserAccounts']
        self.tweet_collection = self.db['TweetDumps']
        self.tokens_collection = self.db['Tokens']


if __name__ == '__main__':
    foo = MongoConnector()
    #print(foo.user_collection.find_one({"twitter_id": -1}))
    #foo.tokens_collection.create_index([("state", 1)], unique=True)
