# MQTT
TOPIC = "query/sp_ranking/#"
DATA_FIELD = "data"
RESPONSE_ID_FIELD = "response-id"

# InfluxDB
POWER_MEASURE = "power"
STATUS_MEASURE = "status"
MEASURES = {POWER_MEASURE, STATUS_MEASURE}

ID_FIELD = "id"
ROW_FIELD = "row"
COLUMN_FIELD = "column"
DATE_FROM_FIELD = "from"
DATE_TO_FIELD = "to"
OP_FIELD = "operation"
TYPE_FIELD = "type"
TYPES = {"g", "p", "w"}  # group meeting room  # printer  # workspace

ID_REGEX = r"^[\w\._\d]+$"
DATETIME_REGEX = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d*)?Z"

FIELDS = [
    ID_FIELD,
    ROW_FIELD,
    COLUMN_FIELD,
    DATE_FROM_FIELD,
    DATE_TO_FIELD,
    OP_FIELD,
    TYPE_FIELD,
]

# https://docs.influxdata.com/influxdb/v1.8/query_language/functions/
OPERATIONS = {
    # aggregation
    "COUNT",
    "DISTINCT",
    "INTEGRAL",
    "MEAN",
    "MEDIAN",
    "MODE",
    "SPREAD",
    "STDDEV",
    "SUM",
    # selection
    "BOTTOM",
    "FIRST",
    "LAST",
    "MAX",
    "MIN",
    "PERCENTILE",
    "SAMPLE",
    "TOP",
}
