__author__ = 'mhoyer'

from aws_cfn_custom_resource_handler.entities.custom_resource import CustomResourceResponse
from connectors.s3 import S3Bucket
import logging
from yapsy.IPlugin import IPlugin


class CloudFormationCustomEventHandler(object):

    def __init__(self, custom_resource_event):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s',
                            datefmt='%d.%m.%Y %H:%M:%S',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        self.event = custom_resource_event
        self.response_bucket = S3Bucket(self.event.get_property("ResponseURL"))

    def convert_properties_to_kv_string(self, properties):
        kv_string = ""
        for key in properties:
            kv_string += "{0}={1}\n".format(key, properties[key])
        return kv_string

    def handle_event(self):
        self.logger.info("Handling request: " + self.event.id)


        properties = self.event.get_property("ResourceProperties")
        user_data = self.convert_properties_to_kv_string(properties)

        response = CustomResourceResponse("SUCCESS",
                                          self.event.get_property("LogicalResourceId"),
                                          self.event.get_property("LogicalResourceId"),
                                          self.event.get_property("StackId"),
                                          self.event.get_property("RequestId"),
                                          {"UserData": user_data})

        self.logger.debug(response)
        self.response_bucket.put(response)


class BaseCustomResourceEventHandler(IPlugin):

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s',
                            datefmt='%d.%m.%Y %H:%M:%S',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def handle_event(self, event):
        return {}