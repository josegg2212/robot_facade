import paho.mqtt.client as mqtt
import time
import json
import sys
import os

sys.path.append(os.path.abspath('./logger'))
from logging_config import Logger
logger=Logger.get_logger()

class MQTTClient:
    """
    subscriptions: list of tuples (topic, qos, callback function)
    """

    def __init__(self, client_id: str, host: str, port: int, keepalive: int, qos: int = 1, clean_session: bool = False,
                 subscriptions=[], broker_usr="", broker_pass=""):
        """
        Parameters
        ----------
        :client_id : str. Unique identifier for the program running MQTTClient.
        :host : str. IP address of MQTT Broker.
        :port : int. Port of MQTT Broker.
        :qos : int <optional>. Standard Quality of Service for subscription and publications.
        :clean_session : bool <optional>. Clean session for the client, also in reconnections.

        :subscription : list. List with initial subscriptions.
            Receives list of tuples with following fields:
            : topic : str. Topic subscription name.
            : qos : str. QoS of subscrition.
            : callback : function. Function that will be executed when messages are received.

        :broker_usr : str <optional>. Broker user for authentication.
        :broker_pass : str <optional>. Broker password for authentication.
        """
        self.client_id = client_id
        self.host = host
        self.port = port
        self.keepalive = keepalive

        # Store initial subscriptions
        self.subscriptions = dict()
        for topic, qos, callback in subscriptions:
            self.subscriptions[topic] = dict()
            self.subscriptions[topic]["topic"] = topic
            self.subscriptions[topic]["qos"] = qos
            self.subscriptions[topic]["callback"] = callback

        self.rc = 1

        self.qos = qos

        self.mqtt_client = mqtt.Client(client_id=self.client_id, clean_session=clean_session,transport="websockets")
        # self.mqtt_client = mqtt.Client(client_id=self.client_id, clean_session=clean_session)

        # Authenticate in broker
        if (broker_usr != ""):
            self.mqtt_client.username_pw_set(broker_usr, broker_pass)

        # Control unintentional disconnnections
        self.disconnect_flag = False

        # Set callbacks
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_message = self.on_message  # Default callback for subscriber
        
        
    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connection result: " + str(mqtt.connack_string(rc)))
 

    def connect(self):
        """
        Start connection to broker and create subscriptions
        """
        while self.rc != 0:
            try:
                self.rc = self.mqtt_client.connect(self.host, self.port, self.keepalive)
                logger.info("Mqtt connected")

                for s in self.subscriptions.keys():
                    subscription = self.subscriptions.get(s)
                    self.subscribe(subscription["topic"], subscription["qos"], subscription["callback"])

            except Exception as e:
                logger.error("Failed to connect to MQTT broker:", str(e))
            time.sleep(1)  # Sleep to give time to connect

    def on_disconnect(self, client, userdata, rc):
        # Attempt to reconnect if disconnection is not intentional
        if rc != mqtt.MQTT_ERR_SUCCESS:
            if not self.disconnect_flag:
                logger.error("Unexpected disconnection.")
                logger.info("Trying reconnection")
                self.rc = rc
                self.connect()

    def disconnect(self):
        """
        Close connection to broker.
        """
        logger.info("Disconnecting from broker")
        self.disconnect_flag = True
        self.mqtt_client.disconnect()

    def spin_forever(self):
        """
        Call this function when thread blocking behavior is desired
        """
        self.mqtt_client.loop_forever()

    def spin_start(self):
        """
        Call this function when non blocking thread behavior is desired
        """
        self.mqtt_client.loop_start()

    def on_message(self, client, userdata, msg):
        """
        This method needs to be implememented by subclases.
        Message needs to be deserialized (json).
        Callbacks registeres with subscribe must have the same arguments.
        """
        raise NotImplementedError

    def publish(self, msg, topic: str, qos: int = 1):
        """
        Publish message in topic

        Parameters
        ----------
        :msg : any. Message to be published. JSON is recommended.
        :topic : str. Topic to publish.
        :qos : int. Quality of Service to publish message.
        """
        # logger.info(f"Publish: {topic} {msg}")
        self.mqtt_client.publish(topic, msg, qos)

    def subscribe(self, topic: str, qos: int, callback, add_to_subscriptions: bool = True):
        """
        Create subscription in topic and register callback

        Parameters
        ----------
        :topic : str. Topic to publish.
        :qos : int. Quality of Service to publish message.
        :callback : function. Callback function to be executed
        :add_to_subscriptions : bool <optional>. Register subscription in subscriptions list.
        """
        logger.info(f"Subscribing to {topic}")
        self.mqtt_client.message_callback_add(topic, callback)
        self.mqtt_client.subscribe(topic=topic, qos=qos)

        if (add_to_subscriptions):
            self.subscriptions[topic] = dict()
            self.subscriptions[topic]["topic"] = topic
            self.subscriptions[topic]["qos"] = qos
            self.subscriptions[topic]["callback"] = callback


if __name__ == '__main__':


    ip="10.8.0.1"
    port=8881
    client=MQTTClient("ClientePrueba",  ip, port, 60, qos=2,
                                      subscriptions=[])
    client.connect()
