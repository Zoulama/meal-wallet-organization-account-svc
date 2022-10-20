from pymongo.cursor import Cursor


class OrganizationEntity:

    def __init__(self, organization):
        self.organization = organization

    @classmethod
    def from_json_request(cls, json_request: dict):
        return cls(json_request)

    @classmethod
    def from_mongodb_document(cls, document: dict):
        document['organizationId'] = str(document['_id'])
        del (document['_id'])
        return cls(document)

    def to_mongodb_document(self):
        return self.organization

    def to_dict(self):
        return self.organization


class OrganizationCollection:

    def __init__(self, organizations):
        self.organizations = organizations

    @classmethod
    def from_mongodb_cursor(cls, cursor: Cursor):
        collection = []

        for document in cursor:
            collection.append(
                OrganizationEntity.from_mongodb_document(document)
            )

        return cls(collection)

    def to_list(self):
        collection = []

        for organization in self.organizations:
            collection.append(
                organization.to_dict()
            )
        return collection
