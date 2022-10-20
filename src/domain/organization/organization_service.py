from .organization_entity import OrganizationEntity, OrganizationCollection
from .organization_repository import OrganizationRepository, \
    OrganizationNotFoundException as OrganizationNotFoundRepositoryException


class OrganizationService:

    def __init__(self, organization_repository: OrganizationRepository):
        self.organization_repository = organization_repository

    def fetch(self, organization_id):

        try:
            organization_entity = self.organization_repository.fetch(organization_id)
            return FetchResponse(organization_entity)
        except OrganizationNotFoundRepositoryException as e:
            raise OrganizationNotFoundException(e.__str__())

    def fetch_all(self, filters):
        organization_collection = self.organization_repository.fetch_all(filters)
        return FetchAllResponse(organization_collection)

    def create(self, organization_entity: OrganizationEntity):
        organization_entity = self.organization_repository.create(organization_entity)
        return CreateUserResponse(organization_entity)

    def update(self, plan_id, organization_entity: OrganizationEntity):
        organization_entity = self.organization_repository.update(plan_id, organization_entity)
        return UpdateResponse(organization_entity)


class CreateUserResponse:

    def __init__(self, organization_entity: OrganizationEntity):
        self.organization_entity = organization_entity

    def to_dict(self):
        return self.organization_entity.to_dict()


class FetchAllResponse:

    def __init__(self, organization_collection: OrganizationCollection):
        self.organization_collection = organization_collection

    def to_dict(self):
        return self.organization_collection.to_list()


class FetchResponse:

    def __init__(self, organization_entity: OrganizationEntity):
        self.organization_entity = organization_entity

    def to_dict(self):
        return self.organization_entity.to_dict()


class UpdateResponse:
    def __init__(self, organization_entity: OrganizationEntity):
        self.organization_entity = organization_entity

    def to_dict(self):
        return self.organization_entity.to_dict()


class OrganizationNotFoundException(Exception):
    def __init__(self, message):
        super(OrganizationNotFoundException, self).__init__(message)
