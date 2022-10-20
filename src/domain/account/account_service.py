from .account_entity import AccountEntity, AccountCollection
from .account_repository import AccountRepository, \
    AccountNotFoundException as AccountNotFoundRepositoryException


class AccountService:

    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def fetch(self, account_id):
        try:
            account_entity = self.account_repository.fetch(account_id)
            return FetchResponse(account_entity)
        except AccountNotFoundRepositoryException as e:
            raise AccountNotFoundException(e.__str__())

    def fetch_all(self, filters):
        account_collection = self.account_repository.fetch_all(filters)
        return FetchAllResponse(account_collection)

    def fetch_account_by_organization_id(self, organization_id):
        account_collection = self.account_repository.fetch_account_by_organization_id(
            organization_id
        )
        return FetchAllResponse(account_collection)

    def create(self, account_entity: AccountEntity):
        account_entity = self.account_repository.create(account_entity)
        return CreateUserResponse(account_entity)

    def update(self, account_id, account_entity: AccountEntity):
        account_entity = self.account_repository.update(account_id, account_entity)
        return UpdateResponse(account_entity)


class CreateUserResponse:

    def __init__(self, account_entity: AccountEntity):
        self.account_entity = account_entity

    def to_dict(self):
        return self.account_entity.to_dict()


class FetchAllResponse:

    def __init__(self, account_collection: AccountCollection):
        self.account_collection = account_collection

    def to_dict(self):
        return self.account_collection.to_list()


class FetchResponse:

    def __init__(self, account_entity: AccountEntity):
        self.account_entity = account_entity

    def to_dict(self):
        return self.account_entity.to_dict()


class UpdateResponse:
    def __init__(self, account_entity: AccountEntity):
        self.account_entity = account_entity

    def to_dict(self):
        return self.account_entity.to_dict()


class AccountNotFoundException(Exception):
    def __init__(self, message):
        super(AccountNotFoundException, self).__init__(message)
