from azure.core.exceptions import ResourceExistsError
from azure.storage.queue import QueueClient

import pandas as pd
import time


def now():
    return pd.to_datetime("now").tz_localize("UTC")


class AzureQueue:
    def __init__(self, connection_string, queue_name, autocreate=True):
        self._queue = QueueClient.from_connection_string(conn_str=connection_string, queue_name=queue_name)
        self._queue_name = queue_name

        if autocreate:
            self.create()

    @property
    def raw(self):
        return self._queue

    @property
    def name(self):
        return self._queue_name

    def create(self):
        try:
            self._queue.create_queue()
        except ResourceExistsError as e:
            pass

    def pop(self, count=1, acknowledge_timeout=30, wait_timeout=-1, pooling_interval_seconds=0.1):
        start = now()

        messages = []

        while len(messages) == 0:

            messages = [AzureQueueMessage(self, m, acknowledge_timeout) for m in
                        self._queue.receive_messages(max_messages=count, visibility_timeout=acknowledge_timeout)]

            if wait_timeout != -1 and (now() - start).total_seconds() >= wait_timeout:
                raise TimeoutError("Receival of new messages timed out.")

            if len(messages) == 0:
                time.sleep(pooling_interval_seconds)

        return messages

    def push(self, content, time_to_live_seconds=604800):
        self._queue.send_message(content, time_to_live=time_to_live_seconds)

    def __len__(self):
        properties = self._queue.get_queue_properties()
        count = properties.approximate_message_count
        return count

    def clear(self):
        self._queue.clear_messages()

    def destroy(self):
        self._queue.delete_queue()

    def __str__(self):
        return f'[Azure Queue (Name: {self.name}; Queued elements: {len(self)})]'

    def __repr__(self):
        return str(self)


class AzureQueueMessage:
    def __init__(self, owner, message, acknowledge_timeout=30):
        self._owner = owner
        self._message = message
        self._acknowledge_timeout = acknowledge_timeout
        self._fetched_time = now()
        self._updated_time = now()
        self._acknowledged = False

    @property
    def acknowledged(self):
        return self._acknowledged

    @property
    def raw(self):
        return self._message

    @property
    def content(self):
        return self._message.content

    @property
    def fetched_time(self):
        return self._fetched_time

    @property
    def updated_time(self):
        return self._updated_time

    @property
    def remaining_acknowledge_timeout(self):
        return self._acknowledge_timeout - (now() - self._updated_time).total_seconds() if not self.acknowledged else 0

    def acknowledge(self):
        if self._acknowledged:
            return

        raw_queue = self._owner.raw
        raw_queue.delete_message(self._message.id,
                                 self._message.pop_receipt)

        self._acknowledged = True

    def update(self, content=None, acknowledge_timeout=30):
        if content is None:
            content = self.content

        raw_queue = self._owner.raw

        self._message = raw_queue.update_message(self._message.id,
                                                 self._message.pop_receipt,
                                                 visibility_timeout=acknowledge_timeout,
                                                 content=content)

        self._acknowledge_timeout = acknowledge_timeout
        self._updated_time = now()

    def __len__(self):
        return len(self.content)

    def __str__(self):
        tick = "X" if self.acknowledged else " "
        return f'[{tick}] Azure message - Queue: "{self._owner.name}", Len: {len(self)}, ' \
               f'Remaining ACK time: {self.remaining_acknowledge_timeout} seconds'

    def __repr__(self):
        return str(self)
