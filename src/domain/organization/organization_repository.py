from pymongo.collection import Collection
from bson import ObjectId

from src.domain.organization.organization_entity import OrganizationEntity, OrganizationCollection


class OrganizationRepository:

    def __init__(self, mongodb_organization_collection: Collection):
        self.mongodb_organization_collection = mongodb_organization_collection

    def create(self, organization_entity: OrganizationEntity) -> OrganizationEntity:
        insert_one_result = self.mongodb_organization_collection.insert_one(organization_entity.to_dict())
        return self.fetch(insert_one_result.inserted_id)

    def fetch_all(self, filters) -> OrganizationCollection:
        query = {}

        if 'clientId' in filters:
            query['applications.credentials.oauth2.clientId'] = filters['clientId']

        cursor = self.mongodb_organization_collection.find(query)
        return OrganizationCollection.from_mongodb_cursor(cursor)

    def fetch(self, organization_id) -> OrganizationEntity:
        document = self.mongodb_organization_collection.find_one({'_id': ObjectId(organization_id)})
        if document is None:
            raise OrganizationNotFoundException('organization %s not found' % organization_id)
        return OrganizationEntity.from_mongodb_document(document)

    def update(self, organization_id, organization_entity: OrganizationEntity) -> OrganizationEntity:
        update_one_result = self.mongodb_organization_collection.update_one({'_id': ObjectId(organization_id)},
                                                                    {'$set': organization_entity.to_mongodb_document()})
        return self.fetch(organization_id)


class OrganizationNotFoundException(Exception):
    def __init__(self, message):
        super(OrganizationNotFoundException, self).__init__(message)
