__author__ = 'mhoyer'

from aws_cfn_custom_resource_handler.event_handler import CloudFormationCustomEventHandler


class StackConfigurationEventHandler(CloudFormationCustomEventHandler):

    def handle_event(self):
        self.logger.info("The StackConfigurationEventHandler handles event id: " + str(self.event.id))
        self.send_response("my data")