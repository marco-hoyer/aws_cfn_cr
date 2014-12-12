__author__ = 'mhoyer'

import json


class CustomResourceEvent(object):

    valid_request_types = ["Create", "Update", "Delete"]

    def __init__(self, sqs_message):
        (self.id, self._message) = self._parse_message_body(sqs_message)
        self.properties = self._parse_properties(self._message)
        self._validate_message_data()

    def _parse_message_body(self, sqs_message):
        message_metadata = {}
        body = json.loads(sqs_message.get_body())

        message = body["Message"]
        id = body["MessageId"]
        return (id, message)

    def _parse_properties(self, message):
        properties = {}

        message = json.loads(message)
        return message

    def _validate_message_data(self):
        # validate request type
        assert self.properties["RequestType"] in self.valid_request_types, \
            "RequestType must be one of: {0}".format(self.valid_request_types)
        # there must be a physical resource id on update or delete requests
        if self.properties["RequestType"] in ["Update", "Delete"]:
            assert self.properties["PhysicalResourceId"]

    def get_property(self, key):
        return self.properties[key]


class CustomResourceResponse(object):

    def __init__(self, properties_dict):
        pass
