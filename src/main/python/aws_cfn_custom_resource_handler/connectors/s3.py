__author__ = 'mhoyer'

import requests
import json


class S3Bucket(object):

    def __init__(self, url):
        self.url = url

    def put(self, data):
        requests.put(self.url, data=json.dumps(data)).raise_for_status()