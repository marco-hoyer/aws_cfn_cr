__author__ = 'mhoyer'

from aws_cfn_custom_resource_handler.entities.custom_resource import CustomResourceEvent
from connectors.s3 import S3Bucket
import logging


class CloudFormationCustomEventHandler(object):

    def __init__(self, custom_resource_event):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S',level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.event = custom_resource_event
        self.response_bucket = S3Bucket(self.event.get_property("ResponseURL"))

    def handle_event(self):
        self.logger.info("Doing some action on request: " + self.event.id)
        self.send_response()

    def send_response(self, data):
        self.logger.info("Would put response in: " + str(self.response_bucket.url))
        #self.response_bucket.put(data)

