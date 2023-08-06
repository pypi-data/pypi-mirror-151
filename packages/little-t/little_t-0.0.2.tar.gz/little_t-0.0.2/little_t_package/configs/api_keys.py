import os
from dotenv import load_dotenv


class AWSKeys():
    load_dotenv()

    @staticmethod
    def get_API_URL():
        return os.environ.get('AWS_LAMBDA_URL')


class MongoKeys():
    """
    Static Class to get .env variables for MongoDB Authentication.
    """
    load_dotenv()

    @staticmethod
    def get_cluster_name():
        return os.environ.get('CLUSTER_NAME')

    @staticmethod
    def get_cluster_password():
        return os.environ.get('CLUSTER_PASSWORD')


class TwitterKeys():
    # Initialize dotenv within class call
    load_dotenv()
    """
    Static Class to get .env variables for Twitter API Developer safely.
    """
    @staticmethod
    def get_API_KEY():
        """Returns Twitter Developer API_KEY"""
        return os.environ.get('API_KEY')

    @staticmethod
    def get_API_KEY_SECRET():
        """Returns Twitter Developer API_KEY_SECRET"""
        return os.environ.get('API_KEY_SECRET')

    @staticmethod
    def get_BEARER_TOKEN():
        """Returns Twitter Developer BEARER_TOKEN"""
        return os.environ.get('BEARER_TOKEN')

    @staticmethod
    def get_ACCESS_TOKEN():
        """Returns Twitter Developer ACCESS_TOKEN"""
        return os.environ.get('ACCESS_TOKEN')

    @staticmethod
    def get_ACCESS_TOKEN_SECRET():
        """Returns Twitter Developer ACCESS_TOKEN_SECRET"""
        return os.environ.get('ACCESS_TOKEN_SECRET')

    @staticmethod
    def get_CLIENT_ID():
        """Returns Twitter Developer ACCESS_TOKEN_SECRET"""
        return os.environ.get('CLIENT_ID')

    @staticmethod
    def get_CLIENT_SECRET():
        """Returns Twitter Developer ACCESS_TOKEN_SECRET"""
        return os.environ.get('CLIENT_SECRET')


if __name__ == '__main__':
    print(TwitterKeys.get_ACCESS_TOKEN_SECRET())
