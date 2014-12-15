__author__ = 'mhoyer'

import sys
import logging
from threading import Thread
from entities.custom_resource import CustomResourceEvent
from connectors.sqs import SqsQueue
from aws_cfn_custom_resource_handler.event_handler import CloudFormationCustomEventHandler


class EventObserver(object):

    failed_event_threshold = 2
    failed_events = {}

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s',
                            datefmt='%d.%m.%Y %H:%M:%S',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        self.sqs_queue = SqsQueue()

    def increment_failure_counter(self, event):
        if event.id in self.failed_events:
            self.failed_events[event.id] += 1
        else:
            self.failed_events[event.id] = 1

        return self.failed_events[event.id]

    def get_resource_type_name(self, event):
        return event.get_property("ResourceType").lstrip("Custom::")

    def dispatch_event(self, sqs_message):
        event = CustomResourceEvent(sqs_message)

        self.logger.info("Handling event: {0}".format(event.id))
        self.logger.debug(event)
        resource_type = self.get_resource_type_name(event)

        # TODO: add plugin mechanism executing handlers based on resource_type name
        try:
            eventhandler = CloudFormationCustomEventHandler(event)
            eventhandler.handle_event()
        except Exception as e:

            failure_count = self.increment_failure_counter(event)
            self.logger.error("Couldn't handle event: "
                              "{0}, error was {1} (try {2}/{3})".format(event, str(e), failure_count,
                                                                        self.failed_event_threshold))

            if failure_count < self.failed_event_threshold:
                sys.exit(1)

        self.sqs_queue.delete_message(sqs_message)
        self.logger.info("Deleted event from queue: {0}".format(event.id))

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