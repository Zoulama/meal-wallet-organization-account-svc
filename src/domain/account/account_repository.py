from pymongo.collection import Collection
from bson import ObjectId

from src.domain.account.account_entity import AccountEntity, AccountCollection


class AccountRepository:

    def __init__(self, mongodb_account_collection: Collection):
        self.mongodb_account_collection = mongodb_account_collection

    def create(self, account_entity: AccountEntity) -> AccountEntity:
        insert_one_result = self.mongodb_account_collection.insert_one(account_entity.to_dict())
        return self.fetch(insert_one_result.inserted_id)

    def fetch_all(self, filters) -> AccountCollection:
        cursor = self.mongodb_account_collection.find(filters)
        return AccountCollection.from_mongodb_cursor(cursor)

    def fetch(self, account_id) -> AccountEntity:
        document = self.mongodb_account_collection.find_one({'_id': ObjectId(account_id)})
        if document is None:
            raise AccountNotFoundException('account %s not found' % account_id)
        return AccountEntity.from_mongodb_document(document)

    def fetch_account_by_organization_id(self, organization_id) -> AccountCollection:
        cursor = self.mongodb_account_collection.find(
            {
                "organizationId": organization_id
            }
        )
        return AccountCollection.from_mongodb_cursor(cursor)

    def update(self, account_id, account_entity: AccountEntity) -> AccountEntity:
        update_one_result = self.mongodb_account_collection.update_one({'_id': ObjectId(account_id)},
                                                                    {'$set': account_entity.to_mongodb_document()})
        return self.fetch(account_id)


class AccountNotFoundException(Exception):
    def __init__(self, message):
        super(AccountNotFoundException, self).__init__(message)
