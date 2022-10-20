from pymongo import MongoClient as BaseMongodbClient
from os import environ as env
from pymongo.collection import Collection


class MongodbClient:
    def __init__(self):
        self.mongodb_username = env.get("DB_MONGO_USERNAME")
        self.mongodb_password = env.get("DB_MONGO_PASSWORD")
        self.mongodb_host = env.get("DB_MONGO_HOST")
        self.mongodb_port = env.get("DB_MONGO_PORT")
        self.mongodb_uri_scheme = env.get("DB_MONGO_URI_SCHEME")
        self.mongodb_dbname = env.get("DB_MONGO_DATABASE")

        self.mongodb_client = BaseMongodbClient('%s://%s:%s@%s' % (
            self.mongodb_uri_scheme,
            self.mongodb_username,
            self.mongodb_password,
            self.mongodb_host))

        self.mongodb_database = self.mongodb_client[self.mongodb_dbname]

    def __getattr__(self, name: str) -> Collection:
        """Get a collection by name.

        Raises :class:`~pymongo.errors.InvalidName` if an invalid
        database name is used.

        :Parameters:
          - `name`: the name of the collection to get
        """

        return self.mongodb_database[name]
