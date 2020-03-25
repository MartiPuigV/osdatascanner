from abc import ABC, abstractmethod
from sys import stderr
import json
import pika
import argparse
from contextlib import contextmanager
import systemd.daemon
if systemd.daemon.booted():
    from systemd.daemon import notify as sd_notify
else:
    def sd_notify(status):
        return False
from prometheus_client import Summary

from ...utils.system_utilities import json_utf8_decode


def make_common_argument_parser():
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
            "--host",
            metavar="HOST",
            help="the AMQP host to connect to",
            default="localhost")
    parser.add_argument(
            "--debug",
            action="store_true",
            help="print all incoming messages to the console")

    monitoring = parser.add_argument_group("monitoring")
    monitoring.add_argument(
            "--prometheus-dir",
            metavar="DIR",
            help="the directory in which to drop a Prometheus description"
                    " of this pipeline stage",
            default=None)

    return parser


def make_sourcemanager_configuration_block(parser):
    configuration = parser.add_argument_group("configuration")
    configuration.add_argument(
            "--width",
            type=int,
            metavar="SIZE",
            help="allow each source to have at most %(metavar) "
                    "simultaneous open sub-sources",
            default=3)

    return configuration


def notify_ready():
    sd_notify("READY=1")


def notify_reloading():
    sd_notify("RELOADING=1")


def notify_stopping():
    sd_notify("STOPPING=1")


def notify_status(msg):
    sd_notify("STATUS={0}".format(msg))


def notify_watchdog():
    sd_notify("WATCHDOG=1")


def prometheus_summary(*args):
    """Decorator. Records a Prometheus summary observation for every call to
    the decorated function."""
    s = Summary(*args)

    def _prometheus_summary(func):
        return s.time()(func)
    return _prometheus_summary


def json_event_processor(listener):
    """Decorator. Automatically decodes JSON bodies for the wrapped Pika
    message callback, and automatically produces new messages for every (queue
    name, serialisable object) pair yielded by that callback."""

    def _wrapper(channel, method, properties, body):
        channel.basic_ack(method.delivery_tag)
        decoded_body = json_utf8_decode(body)
        if decoded_body:
            for routing_key, message in listener(
                    decoded_body, channel=method.routing_key):
                channel.basic_publish(exchange='',
                        routing_key=routing_key,
                        body=json.dumps(message).encode())
    return _wrapper


@contextmanager
def pika_session(*queues, **kwargs):
    parameters = pika.ConnectionParameters(**kwargs)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    for q in queues:
        channel.queue_declare(q, passive=False,
                durable=True, exclusive=False, auto_delete=False)

    try:
        yield channel
    finally:
        connection.close()


class PikaConnectionHolder(ABC):
    """A PikaConnectionHolder manages a blocking connection to a RabbitMQ
    server. (Like Pika itself, it is not thread safe.)"""

    def __init__(self, **kwargs):
        self._parameters = pika.ConnectionParameters(**kwargs)
        self._connection = None
        self._channel = None

    def make_connection(self):
        """Constructs a new Pika connection."""
        return pika.BlockingConnection(self._parameters)

    @property
    def connection(self):
        """Returns the managed Pika connection, creating one if necessary."""
        if not self._connection:
            self._connection = self.make_connection()
        return self._connection

    def make_channel(self):
        """Constructs a new Pika channel."""
        return self.connection.channel()

    @property
    def channel(self):
        """Returns the managed Pika channel, creating one (and a backing
        connection) if necessary."""
        if not self._channel:
            self._channel = self.make_channel()
        return self._channel

    def clear(self):
        """Closes the managed Pika connection, if there is one."""
        if self._connection:
            try:
                self._connection.close()
            except pika.exceptions.ConnectionWrongStateError:
                pass
        self._channel = None
        self._connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_info, exc_tb):
        self.clear()


class PikaPipelineRunner(PikaConnectionHolder):
    def __init__(self, *,
            read=set(), write=set(), source_manager=None, **kwargs):
        super().__init__(**kwargs)
        self._read = set(read)
        self._write = set(write)
        self._pending = []

        self.source_manager = source_manager

    def make_channel(self):
        """As PikaConnectionHolder.make_channel, but automatically declares all
        of the read and write queues used by this pipeline stage."""
        channel = super().make_channel()
        for q in self._read.union(self._write):
            channel.queue_declare(q, passive=False,
                    durable=True, exclusive=False, auto_delete=False)
        return channel

    @abstractmethod
    def handle_message(self, message_body, *, channel=None):
        """Responds to the given message by yielding zero or more (queue name,
        JSON-serialisable object) pairs to be sent as new messages."""

    def dispatch_pending(self, *, expected: int):
        """Sends all pending messages.

        This method does not attempt to handle Pika exceptions, but a message
        will not be removed from the pending list if an exception is raised
        while it's being processed."""
        outstanding = len(self._pending)
        if outstanding > expected:
            print(("PikaPipelineRunner.dispatch_pending:"
                    " unexpectedly long queue length {0},"
                    " dispatching").format(outstanding), file=stderr)
        while self._pending:
            routing_key, message = self._pending[0]
            try:
                self.channel.basic_publish(
                        exchange='',
                        routing_key=routing_key,
                        body=json.dumps(message).encode())
            except pika.exceptions.StreamLostError:
                # (just to make it explicit that this might happen)
                raise
            self._pending = self._pending[1:]

    def run_consumer(self):
        """Runs the Pika channel consumer loop in another loop. Connection
        failures in the Pika loop are silently handled without dropping any
        messages."""

        def _queue_callback(channel, method, properties, body):
            """Handles an AMQP message by calling the handle_message function
            and sending everything that it yields as a new message.

            If handle_message takes too long and the underlying Pika connection
            is closed, then this function will continue to collect yielded
            messages and will schedule them to be sent when the connection is
            reopened."""
            channel.basic_ack(method.delivery_tag)
            self.dispatch_pending(expected=0)
            decoded_body = json_utf8_decode(body)
            if decoded_body:
                failed = False
                for routing_key, message in self.handle_message(
                        decoded_body, channel=method.routing_key):
                    # Try to dispatch messages as soon as they're generated,
                    # but store them for later if the connection is dropped
                    self._pending.append((routing_key, message))
                    if not failed:
                        try:
                            self.dispatch_pending(expected=1)
                        except pika.exceptions.StreamLostError:
                            failed = True

        while True:
            try:
                for q in self._read:
                    self.channel.basic_consume(q, _queue_callback)
                self.dispatch_pending(expected=0)
                self.channel.start_consuming()
            except (pika.exceptions.StreamLostError,
                    pika.exceptions.ConnectionWrongStateError):
                # Flush the channel and connection and continue the loop
                self._channel = None
                self._connection = None
                pass
            except:
                self.channel.stop_consuming()
                raise
