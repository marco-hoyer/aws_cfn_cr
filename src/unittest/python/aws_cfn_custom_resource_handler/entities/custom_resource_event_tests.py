__author__ = 'mhoyer'

import unittest2
from mock import Mock
from aws_cfn_custom_resource_handler.entities.custom_resource import CustomResourceEvent
from boto.sqs.message import Message


class CustomResourceEventTests(unittest2.TestCase):

    CFN_MESSAGE_BODY = {
        "SignatureVersion": "1",
        "Timestamp": "2014-12-12T15:02:38.213Z",
        "Signature": "YbEQEfJe038hnFNQ3hh3S3d1lGDySSXLyTT9VY+Y3Rpe5XYHoX9xNmyoIrG/V4Fo95Ee6DYNI7QrPjuVgQzTdNm5SjvLgqmLGHtcTfH9wTN7FBnQNySpMrYcOFNJb2zwtA/Fkz3gwzirgThxWzELOhr6qcSdXj6AqxWha+RjsNb+kQqHtcqlT7vMaHePgSToSqyDYBhy3+5/FFFw7At5BZQtIC8KQZtacRcbjdkYKL9aukrJaUD/5hJEY3AWW3rHP9vkpKYFHrTz+21aej5DIppWVDYTBl0d0FCTlP+xkD965ypNkOMEvbmBzFmTuvxg68PDbIwC6qlxWKAtOYBq+A==",
        "SigningCertURL": "https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-d6d679a1d18e95c2f9ffcf11f4f9e198.pem",
        "MessageId": "b756841d-f0a8-5841-a3ef-c918f5660f61",
        "Message": "{\"RequestType\":\"Update\"}",
        "UnsubscribeURL": "https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:202084488265:is24-cfn-custom-resources:aa1048c5-b841-42fc-95e0-b3ea4c42e28c",
        "Type": "Notification",
        "TopicArn": "arn:aws:sns:eu-west-1:202084488265:is24-cfn-custom-resources",
        "Subject": "AWS CloudFormation custom resource request"
    }





    def test_sqs_message_parsing(self):
        message_mock = Mock(spec=Message)
        print unicode(self.CFN_MESSAGE_BODY)
        message_mock.get_body.return_value = unicode(self.CFN_MESSAGE_BODY)
        cre = CustomResourceEvent(message_mock)
        print vars(cre)