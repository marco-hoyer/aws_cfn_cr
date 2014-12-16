__author__ = 'mhoyer'

import sys
import logging
from threading import Thread

from yapsy.PluginManager import PluginManager

from entities.custom_resource import CustomResourceEvent
from connectors.sqs import SqsQueue


class EventDispatcher(object):

    failed_event_threshold = 2
    failed_events = {}

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s',
                            datefmt='%d.%m.%Y %H:%M:%S',
                            level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.plugin_manager = PluginManager()
        self.plugin_manager.setPluginPlaces(["plugins"])
        self.plugin_manager.setPluginInfoExtension('plugin')
        self._init_plugins()

        self.sqs_queue = SqsQueue()

    def _init_plugins(self):
        self.plugin_manager.collectPlugins()
        for pluginInfo in self.plugin_manager.getAllPlugins():
            self.plugin_manager.activatePluginByName(pluginInfo.name)
            self.logger.info("Loaded plugin: {0}".format(pluginInfo.name))

    def get_plugin_by_name(self, name):
        plugin = self.plugin_manager.getPluginByName(name)
        if not plugin:
            plugin = self.plugin_manager.getPluginByName("Default")

        self.logger.info("Choose {0} handler for resource name {1}".format(plugin.name, name))
        return plugin

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

        try:
            event_handler = self.get_plugin_by_name(resource_type)
            event_handler.plugin_object.handle_event(event)
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
            # TODO: handle errors here
            sqs_messages = self.sqs_queue.get_messages()
            if sqs_messages:
                self.logger.info("Found {0} events in the queue".format(len(sqs_messages)))
            for sqs_message in sqs_messages:
                thread = Thread(target=self.dispatch_event, args=(sqs_message,))
                thread.start()

    def load_plugins(self):
        pass


if __name__ == "__main__":
    event_observer = EventDispatcher()
    event_observer.event_loop()