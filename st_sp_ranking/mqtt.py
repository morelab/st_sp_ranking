import asyncio
import json
from typing import Dict, List, Any, Callable, Coroutine, Optional

from gmqtt import Client as MQTTClient
from gmqtt.mqtt.constants import MQTTv311

from st_sp_ranking import logger
from st_sp_ranking import protocol, influx

MQTTTopic = str
MQTTPayload = bytes
MQTTProperties = Dict
MessageHandler = Callable[
    [MQTTTopic, MQTTPayload, MQTTProperties], Coroutine[Any, Any, None]
]


class MQTT(MQTTClient):
    """
    MQTT client class, which sends and receives MQTT messages.

    :ivar message_handler: async function that handles MQTT messages
    :ivar running: boolean that represents if the server is running.
    """

    message_handler: MessageHandler
    running: bool
    topics: List[MQTTTopic]

    def __init__(self, client_id):
        """
        Initializes the MQTT client.

        :param client_id: MQTT client id
        """
        MQTTClient.__init__(self, client_id)
        self.message_handler = ...
        self.running = False
        self.topics = []
        self._STARTED = asyncio.Event()
        self._STOP = asyncio.Event()

    def on_connect(self, client, flags, rc, properties):
        logger.log_info_verbose("CONNECTED")
        # subscribe to topics to ensure subscriptions are maintained after
        # connection loss
        for topic in self.topics:
            self.subscribe(topic)

    def on_message(self, client, topic, payload, qos, properties):
        asyncio.create_task(self.message_handler(topic, payload, properties))
        logger.log_info_verbose("RECV MSG:" + payload.decode())

    def on_disconnect(self, client, packet, exc=None):
        logger.log_info_verbose("DISCONNECTED")

    def on_subscribe(self, client, mid, qos, properties):
        logger.log_info_verbose("SUBSCRIBED")

    async def start(
        self,
        broker_host: str,
        message_handler: MessageHandler,
        topics: List[MQTTTopic],
        token: str = None,
    ):
        """
        Runs the MQTT client.

        :param broker_host: MQTT broker IP
        :param message_handler: async function for handling incoming messages.
        :param topics: topics to which MQTT client will subscribe.
        :param token: optional token credential for MQTT security.
        :return:
        """
        if self.running:
            raise RuntimeError("MQTT already running")
        self.message_handler = message_handler  # type: ignore
        asyncio.create_task(self._run_loop(broker_host, token, topics))
        self.running = True
        await self._STARTED.wait()
        logger.log_info_verbose(
            f"MQTT Server started on: {broker_host}. Listening to {topics}"
        )

    async def stop(self):
        """
        Stops MQTT client.

        :return:
        """
        if self.running:
            self._STOP.set()
            self._STARTED = asyncio.Event()
            self._STOP = asyncio.Event()
            self.running = False

    async def _run_loop(
        self, broker_host: str, token: Optional[str], topics: List[MQTTTopic]
    ):
        """
        Method that starts the MQTT client and waits for it to stop.

        :param broker_host: MQTT broker IP.
        :param token: optional token credential for MQTT security
        :param topics: topics to which MQTT client will subscribe.
        :return:
        """
        if token:
            self.set_auth_credentials(token, None)
        self.topics = topics
        # connect will trigger on_connect() which will subscribe to topics
        await self.connect(broker_host, version=MQTTv311)
        self._STARTED.set()
        await self._STOP.wait()
        await self.disconnect()

    async def handle_message(self, topic: str, payload, properties):
        logger.log_info(f"Handle message: {payload}")
        response_topic = json.loads(payload.decode())[protocol.RESPONSE_ID_FIELD]
        try:
            subtopics = topic.split("/")
            when, smartplug_id = subtopics[-2:]
            logger.log_info(f"Getting ranking: {when} - {smartplug_id}")
            ranking_position, ranking_amount = await influx.get_ranking(
                smartplug_id, when
            )
            logger.log_info(f"Ranking: {ranking_position}")
            response = {
                "data": {"position": ranking_position, "amount": ranking_amount}
            }
            self.publish(response_topic, response)
        except Exception as err:
            self.publish(response_topic, {"error": f"Error getting the ranking: {err}"})
        # TODO: how to reply if response topic is unknown?
