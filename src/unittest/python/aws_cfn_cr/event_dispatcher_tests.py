__author__ = 'mhoyer'

from aws_cfn_cr.interface import BaseCustomResourceEventHandler
from aws_cfn_cr.entities.custom_resource import CustomResourceEvent
from unittest2 import TestCase
from mock import Mock, patch, _Call


class BaseCustomResourceEventHandlerTests(TestCase):

    def test(self):
        pass