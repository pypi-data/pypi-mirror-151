import datetime
import logging
from typing import Iterator

import msgpack
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.consumer.fetcher import ConsumerRecord
from kafka.producer.future import FutureRecordMetadata


def ensure_topics(bootstrap_servers, required_topics, num_partitions=4, replication_factor=1) -> bool:
    """
    Function that runs on start and ensures that topics are present.
    """
    from kafka import KafkaClient
    from kafka.admin import KafkaAdminClient
    from kafka.admin import NewTopic

    logging.info(f"Ensuring topics for: {required_topics}")
    client = KafkaClient(bootstrap_servers=bootstrap_servers)
    future = client.cluster.request_update()
    client.poll(future=future)
    metadata = client.cluster
    existing_topics = metadata.topics()

    topics_to_be_created = [topic_name for topic_name in required_topics if topic_name not in existing_topics]

    if not topics_to_be_created:
        logging.info(f"Topics: {required_topics} Topics are present already.")
        return True

    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers, client_id="topics_management")
    topic_list = []
    for topic_name in topics_to_be_created:
        logging.info(f"Topic: {topic_name} creating topic.")
        topic_list.append(
            NewTopic(
                name=topic_name,
                num_partitions=num_partitions,
                replication_factor=replication_factor,
            )
        )

    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    return True


def encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return {"__datetime__": True, "as_str": obj.strftime("%Y%m%dT%H:%M:%S.%f")}
    return obj


def decode_datetime(obj):
    if "__datetime__" in obj:
        obj = datetime.datetime.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S.%f")
    return obj


def compress_body(body):
    return msgpack.dumps(body, default=encode_datetime)


def decompress_body(body):
    return msgpack.loads(body, object_hook=decode_datetime)


def headers_to_dict(headers):
    response = {}
    for key_pair in headers:
        key = key_pair[0]
        value = key_pair[1].decode("utf-8")
        response[key] = value
    return response


def headers_from_dict(headers: dict[str, str]):
    response = []
    for key, value in headers.items():
        if not isinstance(key, str):
            raise ValueError("Header key should be a string")
        if not isinstance(value, str):
            raise ValueError("Header value should be a string")

        response.append((key, value.encode("utf-8")))

    return response


class Producer(KafkaProducer):
    def send(self, *args, **kwargs) -> FutureRecordMetadata:
        kwargs["value"] = compress_body(kwargs["value"])
        kwargs["headers"] = kwargs.get("headers", {})
        kwargs["headers"]["_content_type"] = "application/msgpack"
        kwargs["headers"]["_event_version"] = "1"
        kwargs["headers"] = headers_from_dict(kwargs["headers"])
        return super().send(*args, **kwargs)


class Consumer(KafkaConsumer):
    def __init__(self, *args, **kwargs):
        self.compatibility_map = {"1__application/msgpack": self.handle_v1_msgpack}
        self.interrupt_iteration = False
        return super().__init__(*args, **kwargs)

    def handle_v1_msgpack(self, item):
        return item._replace(value=decompress_body(item.value))

    def receive(self, timeout_ms=5000, max_records=None) -> Iterator[ConsumerRecord]:
        while not self.interrupt_iteration:
            response = self.poll(timeout_ms=timeout_ms, max_records=max_records)
            for _, messages in response.items():
                for message in messages:
                    item = message._replace(headers=headers_to_dict(message.headers))

                    event_type = f"{item.headers.pop('_event_version', '')}__{item.headers.pop('_content_type', '')}"
                    handler = self.compatibility_map.get(event_type)

                    if not handler:
                        logging.error(f"Message: {item.headers} is not compatible.")
                        continue

                    yield handler(item=item)
