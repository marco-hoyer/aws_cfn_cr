__author__ = 'mhoyer'

from boto.ec2 import cloudwatch
from boto.utils import get_instance_metadata
import datetime


class CloudwatchMetricWriter(object):

    CW_NAMESPACE = "CloudFormationCustomResourceHandler"

    def __init__(self, region="eu-west-1"):
        self.connection = cloudwatch.connect_to_region(region)

    def _get_instance_metadata(self):
        metadata = get_instance_metadata()
        return metadata['instance-id'], metadata['instance-type']

    def send_metrics(self, instance_id, instance_type, metrics, unit):
        self.connection.put_metric_data(self.CW_NAMESPACE, metrics.keys(),
                                        metrics.values(), unit=unit,
                                        dimensions={"InstanceType": instance_type, "InstanceId": instance_id})

    def example_send_metric(self):
        metadata = self._get_instance_metadata()
        metrics = {'AverageGetRequestDuration': 1.2,
                   'AveragePostRequestDuration': 2.2}
        self.send_metrics(metadata[0], metadata[1], metrics, "Milliseconds")


if __name__ == '__main__':
    cw = CloudwatchMetricWriter()
    print cw.example_send_metric()