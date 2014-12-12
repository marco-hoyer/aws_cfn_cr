__author__ = 'mhoyer'

from threading import Thread
import logging

from entities.custom_resource import CustomResourceEvent
from connectors.sqs import SqsQueue
from aws_cfn_custom_resource_handler.event_handlers.StackConfiguration import StackConfigurationEventHandler


class EventObserver(object):

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S',level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.sqs_queue = SqsQueue()


    def dispatch_event(self, sqs_message):
        event = CustomResourceEvent(sqs_message)

        self.logger.info("Handling request with id: {0}".format(event.get_property("RequestId")))
        resource_type = event.get_property("ResourceType").lstrip("Custom::")

        if resource_type == "StackConfiguration":
            self.logger.info("Found StackConfigurationHandler for resource-type: {0}".format(resource_type))
            eventhandler = StackConfigurationEventHandler(event)
            eventhandler.handle_event()

        # response_dict = {}
        # response_dict["Status"] = "SUCCESS"
        # response_dict["StackId"] = stack_id
        # response_dict["RequestId"] = request_id
        # if physical_resource_id:
        #     response_dict["PhysicalResourceId"] = physical_resource_id
        # else:
        #     response_dict["PhysicalResourceId"] = stack_id
        # response_dict["LogicalResourceId"] = logical_resource_id
        #
        # response = S3Bucket(s3_response_url)
        # self.logger.info("RESPONSE URL: " + str(s3_response_url))
        # self.logger.info("RESPONSE: " + str(response_dict))
        # self.logger.info("RESPONSE TYPE: " + str(type(response_dict)))
        #
        # try:
        #     response.put(response_dict)
        # except Exception as e:
        #     self.logger.error("Couldn't put response to s3 bucket")
        #     self.logger.exception(e)

        #TODO: determine if event should always get deleted from queue or only if the response was successful
        #self.sqs_queue.delete_message(event)
        #self.logger.info("Deleted event from queue: " + str(event))

    def event_loop(self):
        while True:
            sqs_messages = self.sqs_queue.get_messages()
            if sqs_messages:
                self.logger.info("Found {0} events in the queue".format(len(sqs_messages)))
            for sqs_message in sqs_messages:
                thread = Thread(target=self.dispatch_event, args=(sqs_message,))
                thread.start()


if __name__ == "__main__":
    event_observer = EventObserver()
    event_observer.event_loop()