__author__ = 'mhoyer'

import requests
import json
import logging


class S3Bucket(object):

    def __init__(self, url):
        self.url = url

        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s',
                            datefmt='%d.%m.%Y %H:%M:%S',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        logging.getLogger("requests").setLevel(logging.WARNING)

    def put(self, response):
        self.logger.debug("Sending response with properties: {0}".format(response.properties))
        requests.put(self.url, data=json.dumps(response.properties)).raise_for_status()