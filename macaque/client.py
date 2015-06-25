"""The Client code for the Macaque library for Flask style microservices
with MQ Light"""
import mqlight
import json
import uuid
import logging


class Client(object):
    """Client class for macaque, for making calls to microservice endpoints"""

    def __init__(self,
            broker='amqp://127.0.0.1:5672',
            cid=None,
            security_options=None):
        self.callbacks = {}
        sub_opt = {
            "auto_confirm": True
        }
        self.client = mqlight.Client(broker,
            client_id=cid,
            security_options=security_options)
        self.client.subscribe('response/' + self.client.get_id(),
            options=sub_opt,
            on_message=self.serve)
        self.logger = logging.getLogger(__name__)

    def call(self, endpoint, data, callback):
        """Wraps the data for the call in a struct that adds a uuid for
        tracking"""
        send_data = {}
        call_uuid = str(uuid.uuid4())
        self.callbacks[call_uuid] = callback
        send_data['uuid'] = call_uuid
        send_data['data'] = data
        send_data['replyTo'] = 'response/' + self.client.get_id()
        self.client.send(endpoint, json.dumps(send_data))

    def serve(self, message_type, data, delivery):
        """Handles passing responses for requests to their handlers"""
        self.logger.debug(data)
        try:
            response_data = json.loads(data)
            response_uuid = response_data['uuid']
            if response_uuid in self.callbacks:
                self.callbacks[response_uuid](response_data['data'])
                del self.callbacks[response_uuid]
        except (ValueError, KeyError, TypeError) as error:
            self.logger.debug(error)

    def close(self):
        """Stops the internal MQ Light client"""
        self.client.stop()
