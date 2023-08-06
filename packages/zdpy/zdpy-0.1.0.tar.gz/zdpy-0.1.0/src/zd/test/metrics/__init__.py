
import json
import boto3
import atexit
import logging
from functools import partial
from datadog import DogStatsd
from zocdoc.canoe.timehelp import to_utc


logger = logging.getLogger(__name__)


def to_lambda_metric_format(metric_type, timestamp, metric_name, value=1, tags=None):
    time_str = (to_utc(timestamp) if not hasattr(timestamp, 'strftime') else timestamp).strftime('%s')

    return 'MONITORING|{epoch}|{value}|{metric_type}|{metric_name}|#{tags}'.format(
            epoch=time_str,
            value=value,
            metric_type=metric_type,
            metric_name=metric_name,
            tags=','.join(tags or [])
        )


def cleanup_client(client):
    try:
        client.flush()
    except Exception as e:
        logger.info('{} failed on atexit cleanup {}'.format(type(client), e))


class MetricLambdaClient(object):
    @staticmethod
    def get_default_lambda_client():
        return boto3.client('lambda')

    @staticmethod
    def create(lambda_name=None, lambda_client=None):
        return MetricLambdaClient(
            lambda_name=lambda_name,
            lambda_client=(lambda_client or MetricLambdaClient.get_default_lambda_client())
        )

    def __init__(self, lambda_client=None, lambda_name=None):
        self.lambda_client = lambda_client
        self.lambda_name = lambda_name
        self._staged_messages = []

        atexit.register(cleanup_client, self)

    def _send_message(self, message):
        return self.lambda_client.invoke(
            FunctionName=self.lambda_name,
            InvocationType='Event',
            Payload=json.dumps(dict(payload=message))
        )

    def _stage_message(self, message):
        self._staged_messages.append(message)

    def flush(self):
        if self._staged_messages:
            self._send_message(self._staged_messages)
            self._staged_messages = []

    def send_metric(self, *args, **kwargs):
        self._send_message(to_lambda_metric_format(*args, **kwargs))

    def stage_metric(self, *args, **kwargs):
        self._stage_message(to_lambda_metric_format(*args, **kwargs))


class MockDogStatsd(object):
    def __init__(self, **kwargs):
        logger.debug('Create mock DogStatsd {}'.format(str(kwargs)))

    def __getattr__(self, item):
        def wrapper(*args, **kwargs):
            logger.debug('Calling {} with args {} and kwargs {}'.format(item, str(args), str(kwargs)))

        return wrapper


def get_datadog_client(app_config):
    if app_config.deployment_environment == 'dev':
        return MockDogStatsd()
    else:
        return DogStatsd(
            host=app_config.datadog_host,
            port=app_config.datadog_port,
            namespace=app_config.datadog_namespace,
            use_ms=True
        )
