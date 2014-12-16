__author__ = 'mhoyer'

import aws_cfn_custom_resource_handler.interface as interface


class DefaultCustomResourceEventHandler(interface.BaseCustomResourceEventHandler):

    name = "Default"

    def handle_event(self, event):
        self.logger.info("Handling event {0}".format(event))