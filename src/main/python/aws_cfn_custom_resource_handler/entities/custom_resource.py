__author__ = 'mhoyer'

import json


class CustomResourceEvent(object):

    valid_request_types = ["Create", "Update", "Delete"]

    def __init__(self, sqs_message):
        (self.id, self._message) = self._parse_message_body(sqs_message)
        self.properties = self._parse_properties(self._message)
        self._validate()

    def __repr__(self):
        return "REQUEST: action={0}, resource={1}, stack={2} (request-id={3})".format(self.get_property("RequestType"),
                                                                             self.get_property("LogicalResourceId"),
                                                                             self.get_property("StackId"),
                                                                             self.get_property("RequestId"))

    def _parse_message_body(self, sqs_message):
        body = json.loads(sqs_message.get_body())

        message = body["Message"]
        id = body["MessageId"]
        return (id, message)

    def _parse_properties(self, message):
        message = json.loads(message)
        return message

    def _validate(self):
        # validate request type
        assert self.properties["RequestType"] in self.valid_request_types, \
            "RequestType must be one of: {0}".format(self.valid_request_types)
        # there must be a physical resource id on update or delete requests
        if self.properties["RequestType"] in ["Update", "Delete"]:
            assert self.properties["PhysicalResourceId"]

    def get_property(self, key):
        return self.properties[key]


class CustomResourceResponse(object):

    valid_status_types = ["SUCCESS", "FAILED"]

    def __init__(self, status, logical_resource_id, physical_resource_id, stack_id, request_id, data):

        self.properties = {
            "Status": status,
            "LogicalResourceId": logical_resource_id,
            "StackId": stack_id,
            "RequestId": request_id,
        }
        if physical_resource_id:
            self.properties["PhysicalResourceId"] = physical_resource_id
        if data:
            self.properties["Data"] = data

        self._validate()

    def __repr__(self):
        return "RESPONSE: status={0}, resource={1}, stack={2} (request-id={3})".format(self.get_property("Status"),
                                                                             self.get_property("LogicalResourceId"),
                                                                             self.get_property("StackId"),
                                                                             self.get_property("RequestId"))

    def _validate(self):
        assert self.properties["Status"] in self.valid_status_types, \
            "Status must be one of: {0}".format(self.valid_status_types)
        for key in ["LogicalResourceId", "StackId", "RequestId"]:
            assert self.properties[key], "{0} is required".format(key)

    def get_json(self):
        return json.dumps(self.properties)

    def get_property(self, key):
        return self.properties[key]