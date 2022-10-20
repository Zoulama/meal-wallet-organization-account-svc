from pymongo.cursor import Cursor


class AccountEntity:

    def __init__(self, account):
        self.account = account

    @classmethod
    def from_json_request(cls, json_request: dict):
        return cls(json_request)

    @classmethod
    def from_mongodb_document(cls, document: dict):
        document['accountId'] = str(document['_id'])
        del (document['_id'])
        return cls(document)

    def to_mongodb_document(self):
        return self.account

    def to_dict(self):
        return self.account


class AccountCollection:

    def __init__(self, accounts):
        self.accounts = accounts

    @classmethod
    def from_mongodb_cursor(cls, cursor: Cursor):
        collection = []

        for document in cursor:
            collection.append(
                AccountEntity.from_mongodb_document(document)
            )

        return cls(collection)

    def to_list(self):
        collection = []

        for account in self.accounts:
            collection.append(
                account.to_dict()
            )
        return collection
