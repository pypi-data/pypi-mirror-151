
import uuid
import math
import json
import boto3
import logging
from itertools import chain
from collections import namedtuple
from zocdoc.canoe.tools import list_to_batches


logger = logging.getLogger(__name__)


class SqsMessageWrapper(object):
    def __init__(self, message_object):
        self.message_object = message_object
        self.__body = None

    @property
    def body(self):
        if self.__body is None:
            try:
                self.__body = json.loads(self.message_object.body)
            except:
                self.__body = self.message_object.body

        return self.__body

    def __getattr__(self, item):
        return getattr(self.message_object, item)


class SqsMessageEventRecord(SqsMessageWrapper):
    def __init__(self, event_record, *args, **kwargs):
        super(SqsMessageEventRecord, self).__init__(*args, **kwargs)
        self.event_record = event_record


def queue_approximate_number_of_messages(queue_resource):
    return int(queue_resource.attributes.get('ApproximateNumberOfMessages') or '0')


def query_sqs_messages(queue, max_message_count=10):
    BOTO3_MAXIMUM_INPUT = 10  # boto3 maximum input

    min_number_of_tries = int(math.ceil(max_message_count / 10.0))

    try_count, new_msgs = 0, []
    while (
            len(new_msgs) < max_message_count and
            try_count < min_number_of_tries and
            queue_approximate_number_of_messages(queue)):
        try:
            try_count += 1
            num_of_messages_get = min(BOTO3_MAXIMUM_INPUT, max_message_count, max_message_count - len(new_msgs))
            msgs = queue.receive_messages(MaxNumberOfMessages=num_of_messages_get)
            new_msgs.extend(SqsMessageWrapper(m) for m in msgs)
        except Exception as e:
            logger.info('Error on pinging queue - ' + str(e))
            logger.error(e)
            print(e)

    return new_msgs


def to_sqs_delete_entries(messages):
    return [{'Id': str(i), 'ReceiptHandle': msg.receipt_handle} for i, msg in enumerate(messages)]


def delete_sqs_messages(queue, entries):
    """
    can only delete 10 per batch. that sucks. i want more.

    :param queue: the boto3 queue resource
    :param entries: [{'Id': 'str id', 'ReceiptHandle': 'str'}, ...]
    """

    processed, response = 0, {'Successful': [], 'Failed': []}
    while processed < len(entries):
        try:
            next_batch = entries[processed:min((processed+10), len(entries))]
            next_resp = queue.delete_messages(Entries=next_batch)
            response['Successful'].extend(next_resp.get('Successful'))
            response['Failed'].extend(next_resp.get('Failed', []))

            processed += len(next_batch)
        except Exception as e:
            logger.info(
                'Message: Failure on SQS.Queue batch message delete - Error: {err} - QueueUrl: {queue_url}'.format(
                    err=str(type(e)) + str(e),
                    queue_url=queue.url
                )
            )

            raise e

    return response


def send_sqs_messages(queue, messages, is_fifo_queue=False):
    """
    can only send 10 per batch. that sucks. i want more.

    :param queue: the boto3 queue resource
    :param entries: list of dictionaries each of the form
        {
            'message_body': (optional) json serializable blob, default = whole blob
            'id': (optional) str, default = str(int corresponding to input list index)
            'message_deduplication_id': (optional) str, default = guid
            'message_group_id': (optional) str, default = '1' so all messages in same group
        }
        """
    BOTO3_MAXIMUM_INPUT = 10

    def to_message_parameters(id, message_blob, is_fifo):
        input_params = dict(
            Id=message_blob.get('id') or id,
            MessageBody=json.dumps(message_blob.get('message_body') or message_blob)
        )
        if is_fifo:
            input_params.update(
                MessageDeduplicationId=message_blob.get('message_deduplication_id') or str(uuid.uuid4()),
                MessageGroupId=message_blob.get('message_group_id') or '1',
            )
        return input_params

    response = dict(Successful=[], Failed=[])
    try:
        for batch_number, message_batch in enumerate(list_to_batches(messages, BOTO3_MAXIMUM_INPUT)):
            as_valid_input_params = [
                to_message_parameters(str(batch_number*BOTO3_MAXIMUM_INPUT + i), message, is_fifo_queue)
                for i, message in enumerate(message_batch)
            ]
            batch_response = queue.send_messages(Entries=as_valid_input_params)
            response['Successful'].extend(batch_response.get('Successful') or [])
            response['Failed'].extend(batch_response.get('Failed') or [])
    except Exception as e:
        logger.info(
            'Message: Failure on SQS.Queue batch send message - Error: {err} - QueueUrl: {queue_url}'.format(
                err=str(type(e)) + str(e),
                queue_url=queue.url
            )
        )

        raise e

    return response

_object_info_fields = [
    'bucket_name', 'bucket_arn', 'object_key', 'object_eTag', 'object_sequencer',
    'object_size', 'region', 'event_name', 'event_version', 'event_time'
]
S3EventObjectInfo = namedtuple('S3EventObjectInfo', _object_info_fields)


def sqs_s3_messages(sqs_message):
    def to_s3_event_summary(record):
        # full message format https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html
        s3_bucket = record.get('s3').get('bucket')
        s3_object = record.get('s3').get('object')
        return S3EventObjectInfo(
            s3_bucket.get('name'),
            s3_bucket.get('arn'),
            s3_object.get('key'),
            s3_object.get('eTag'),
            s3_object.get('sequencer'),
            s3_object.get('size'),
            record.get('awsRegion'),
            record.get('eventName'),
            record.get('eventVersion'),
            record.get('eventTime')
        )
    filtered_fields_messages = [SqsMessageEventRecord(to_s3_event_summary(rec), sqs_message)
                                for rec in json.loads(sqs_message.body['Message']).get('Records', []) if 's3' in rec]
    return filtered_fields_messages


def latest_s3_message_by_key(sqs_s3_msgs):
    if not sqs_s3_msgs:
        return []

    kv = {(msg.event_record.object_key, msg.event_record.object_sequencer): msg for msg in sqs_s3_msgs}

    list_agg = {u_k: [] for u_k in set(k for k, _ in kv.keys())}
    for k, v in kv.keys():
        list_agg[k].append(v)

    latest = [(k, sorted(v)[-1]) for k, v in list_agg.items()]

    return [kv[latest_kv] for latest_kv in latest]


class SqsQueue(object):
    def __init__(self, queue_name, message_transformer=None, sqs_resource=None):
        self.queue_name = queue_name
        self.sqs_resource = sqs_resource or boto3.resource('sqs')
        self.queue = None
        self.message_transformer = message_transformer

    def get_queue(self):
        self.queue = self.sqs_resource.get_queue_by_name(QueueName=self.queue_name)
        return self

    def approximate_number_of_messages(self):
        return queue_approximate_number_of_messages(self.queue)

    def fifo_queue(self):
        return (self.queue.attributes.get('FifoQueue') or '').lower() == 'true'

    def has_messages(self):
        return self.approximate_number_of_messages() > 0

    def receive_messages(self, **kwargs):
        update_func = self.message_transformer if self.message_transformer else (lambda m: [m])
        return list(chain(*[update_func(msg) for msg in query_sqs_messages(queue=self.queue, **kwargs)]))

    def delete_messages(self, messages):
        try:
            resp = delete_sqs_messages(self.queue, entries=to_sqs_delete_entries(messages))

            successful = resp.get('Successful', [])
            success_ct = len(successful)

            log_msg = 'Message: Removed messages from queue - DeletedMessageCount: {} - DeletedAllMessages: {}'
            logger.info(log_msg.format(success_ct, len(messages) == success_ct))

            failed = resp.get('Failed', [])
            if failed:
                log_msg = 'Message: Subset of SQS.Queue batch delete calls failed - FailedDeletes: {}'
                logger.info(log_msg.format([dict(messages[fail['Id']], **fail) for fail in failed]))

            return resp
        except:
            pass

    def send_messages(self, messages):
        return send_sqs_messages(self.queue, messages, self.fifo_queue())
