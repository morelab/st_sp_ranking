from os import path
import configparser

_config = configparser.ConfigParser()
_config_path = path.join(
    *path.split(path.dirname(path.abspath(__file__)))[:-1], "config", "config.ini"
)
_config.read(_config_path)

_influxdb_config = _config["INFLUXDB"]
_logger_config = _config["LOGGER"]
_mqtt_config = _config["MQTT"]

# Configuration variables
# InfluxDB
INFLUX_HOST = _influxdb_config["host"]
INFLUX_PORT = _influxdb_config["port"]
INFLUX_DB = _influxdb_config["db"]
# Logger
LOGGER_VERBOSE = _logger_config.getboolean("verbose")
# MQTT
MQTT_BROKER_HOST = _mqtt_config.get("broker_host")
MQTT_BROKER_PORT = int(_mqtt_config.get("broker_port"))
MQTT_RESPONSE_TIMEOUT = int(_mqtt_config.get("response_timeout"))
