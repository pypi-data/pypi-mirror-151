import markovify
import re
import emoji
from mongo_database.MongoReader import MongoReader
from mongo_database.MongoWriter import MongoWriter
from twitter_collection import tweet_collector


class MarkovTweetGeneration():
    def __init__(self, target_user: str) -> None:
        self.db_reader = MongoReader()
        self.tw_collector = tweet_collector.TwitterAPIConnector()
        self.target_user = target_user
        self.target_id = self.tw_collector.get_user(
            username=target_user).data['id']

    def _text_preperation(self):
        text_blob = ""
        cursor = self.db_reader.get_tweets_by_author_id(self.target_id)
        sentence_finishers = ['.', '?', '!']
        tweet_list = list(cursor)
        for tweet in tweet_list:
            text = tweet['text']
            # media posts
            # replace http and emoijs
            if re.search(r"http?s://t.co/\w{4,10}", text):
                text = re.sub(r"http?s://t.co/\w{4,10}", "", text)
                text = text[:len(text)-1]
            text = emoji.replace_emoji(text, '')
            text = re.sub(r"@", "", text)
            # add punctuation
            if len(text) == 1 or len(text) == 0:
                continue
            # occasional sentence will start with a blank
            if text[-1] not in sentence_finishers:
                text += '.'
            text = text.capitalize()
            text_blob += text + " "
        return text_blob

    def generate_tweet_text(self):
        text_corpus = self._text_preperation()
        Markov_Model = markovify.Text(
            input_text=text_corpus, well_formed=False)
        try:
            new_sentence = Markov_Model.make_short_sentence(
                min_chars=100, max_chars=150, tries=100).capitalize()
        # TooSmall
        except KeyError:
            return
        if new_sentence[0:2] == ". ":
            new_sentence = new_sentence[2:]
        if self.target_user[0] == '@':
            self.target_user = self.target_user[1:]
        return f"'{new_sentence}' - {self.target_user}"


if __name__ == '__main__':
    user = input("Twitter Handle: ")
    writer = MongoWriter()
    writer.insert_new_tweets(twitter_username=user)
    test_model = MarkovTweetGeneration(user)
    print(test_model.generate_tweet_text())
