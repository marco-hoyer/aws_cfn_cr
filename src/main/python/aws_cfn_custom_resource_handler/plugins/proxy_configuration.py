__author__ = 'mhoyer'

import aws_cfn_custom_resource_handler.interface as interface


class ProxyConfigurationCustomResourceEventHandler(interface.BaseCustomResourceEventHandler):

    name = "ProxyConfiguration"

    def handle_event(self, event):
        self.logger.info("Handling event {0}".format(event))
        self.send_response("SUCCESS", event, None, "blablubb")