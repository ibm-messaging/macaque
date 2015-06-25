"""The Server code for the Macaque library for Flask style microservices
with MQ Light"""
import mqlight
import json
import logging


class Server(object):
    """Server class for macaque, for servicing calls to microservice
    endpoints"""

    def __init__(self,
            broker='amqp://127.0.0.1:5672',
            cid=None,
            security_options=None):
        self.services = {}
        self.client = mqlight.Client(broker,
            client_id=cid,
            security_options=security_options)
        self.logger = logging.getLogger(__name__)

    def service(self, endpoint, share_id=None, credit=5):
        """used as a decorator function, subscribes to an MQ Light topic
        and passes incoming messages to the decorated function"""
        def decorator(decorated):
            """The decorator function"""
            def on_sub(err, pattern, share):
                """on_sub callback"""
                if not err:
                    self.logger.debug("Listening on {0} with share id {1}"
                        .format(pattern, share))
                else:
                    self.logger.warning(err)
            sub_opt = {
                "auto_confirm": True,
                "credit": credit
            }
            self.services[endpoint] = decorated
            self.client.subscribe(endpoint,
                share=share_id,
                options=sub_opt,
                on_message=self.serve,
                on_subscribed=on_sub)
            return decorated
        return decorator

    def serve(self, message_type, data, delivery):
        """Handles passing incoming requests to the endpoint handler
        and sending the response messages"""
        resp_data = {}
        try:
            req_data = json.loads(data)
            resp_data['uuid'] = req_data['uuid']
            endpoint = delivery['destination']['topic_pattern']
            service_func = self.services.get(endpoint)
            if service_func:
                response = service_func(req_data['data'])
                resp_data['data'] = response
                if req_data['replyTo']:
                    self.client.send(req_data['replyTo'],
                        json.dumps(resp_data))
            else:
                raise ValueError('Endpoint "{}"" has not been registered'
                    .format(endpoint))
        except (ValueError, KeyError, TypeError) as error:
            self.logger.warning(error)
            return

    def close(self):
        """Stops the internal MQ Light client"""
        self.client.stop()
