import asyncio

from st_sp_ranking import config
from st_sp_ranking import logger, influx
from st_sp_ranking import protocol
from st_sp_ranking.mqtt import MQTT


async def handle_message(self, topic: str, payload, properties):
    logger.log_info(f"Handle message: {payload}")
    response_topic = payload[protocol.RESPONSE_ID_FIELD]
    try:
        subtopics = topic.split("/")
        when, smartplug_id = subtopics[-2:]
        logger.log_info(f"Getting ranking: {when} - {smartplug_id}")
        ranking = influx.get_ranking(smartplug_id, when)
        logger.log_info(f"Ranking: {ranking}")
        response = {"data": ranking}
        self.publish(response_topic, response)
    except Exception as err:
        self.publish(response_topic, {"error": f"Error getting the ranking: {err}"})
    # TODO: how to reply if response topic is unknown?


if __name__ == "__main__":
    mqtt = MQTT("st_sp_ranking")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        mqtt.start(
            broker_host=config.MQTT_BROKER_HOST,
            message_handler=handle_message,
            topics=[protocol.TOPIC],
        )
    )
    loop.run_forever()
