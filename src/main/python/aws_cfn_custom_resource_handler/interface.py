__author__ = 'mhoyer'

from aws_cfn_custom_resource_handler.entities.custom_resource import CustomResourceResponse
from connectors.s3 import S3Bucket
import logging
from yapsy.IPlugin import IPlugin


class BaseCustomResourceEventHandler(IPlugin):

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s',
                            datefmt='%d.%m.%Y %H:%M:%S',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def handle_event(self, event):
        return {}

    def send_response(self, status, event, data, physical_resource_id=None):
        response_bucket = S3Bucket(event.get_property("ResponseURL"))

        self.logger.info("Sending response for: " + event.id)
        response = CustomResourceResponse(status,
                                          event.get_property("LogicalResourceId"),
                                          physical_resource_id,
                                          event.get_property("StackId"),
                                          event.get_property("RequestId"),
                                          data)

        self.logger.debug(response)
        response_bucket.put(response)