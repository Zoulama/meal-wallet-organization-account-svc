
class AccountAddress:

    def __init__(self, street_name: str, street_number: int,
                 city: str, post_code: str, state: str, country: str):
        self.street_name = street_name
        self.street_number = street_number
        self.city = city
        self.post_code = post_code
        self.state = state
        self.country = country

    @classmethod
    def from_json_request(cls, json_data: dict):
        return cls(json_data['streetName'], json_data['streetNumber'],
                   json_data['city'], json_data['postCode'],
                   json_data['state'], json_data['country'])

    @classmethod
    def from_mongodb_document(cls, document: dict):
        return cls(document['street_name'], document['street_number'],
                   document['city'], document['post_code'],
                   document['state'], document['country'])

    def to_dict(self):
        return self.__dict__
