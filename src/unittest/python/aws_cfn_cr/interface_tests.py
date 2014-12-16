__author__ = 'mhoyer'

from aws_cfn_cr.interface import BaseCustomResourceEventHandler
from aws_cfn_cr.entities.custom_resource import CustomResourceEvent
from unittest2 import TestCase
from mock import Mock, patch, _Call


class BaseCustomResourceEventHandlerTests(TestCase):

    def _get_call_params_from_mock(self, mock):
        return mock.call_args_list[0][0][0]

    @patch('aws_cfn_cr.connectors.s3.S3Bucket.put')
    def test_send_response(self, s3_bucket_put_mock):

        event_mock = Mock(spec=CustomResourceEvent)
        event_mock.id = "mocked_event_id"

        event_mock.get_property.return_value = "property"

        handler = BaseCustomResourceEventHandler()
        handler.send_response("SUCCESS", event_mock, None)
        response = self._get_call_params_from_mock(s3_bucket_put_mock)

        self.assertEqual(response.properties["Status"], "SUCCESS")
        self.assertEqual(response.properties["StackId"], "property")
        self.assertEqual(response.properties["RequestId"], "property")
        self.assertEqual(response.properties["LogicalResourceId"], "property")


    @patch('aws_cfn_cr.connectors.s3.S3Bucket.put')
    def test_send_response_raises_error_with_none_event_properties(self, s3_bucket_put_mock):

        event_mock = Mock(spec=CustomResourceEvent)
        event_mock.id = "mocked_event"

        event_mock.get_property.return_value = None

        with self.assertRaises(AssertionError) as error:
            handler = BaseCustomResourceEventHandler()
            handler.send_response("SUCCESS", event_mock, None)
            response = self._get_call_params_from_mock(s3_bucket_put_mock)