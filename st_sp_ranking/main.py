import asyncio

from st_sp_ranking import config
from st_sp_ranking import protocol
from st_sp_ranking.mqtt import MQTT

if __name__ == "__main__":
    mqtt = MQTT("st_sp_ranking")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        mqtt.start(
            broker_host=config.MQTT_BROKER_HOST,
            message_handler=mqtt.handle_message,
            topics=[protocol.TOPIC],
        )
    )
    loop.run_forever()
