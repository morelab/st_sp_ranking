import datetime
from typing import Union, Tuple

import aioinflux
import strict_rfc3339 as rfc339
from aioinflux import iterpoints

from st_sp_ranking import config

Ranking = int
TimeRange = Union["today", "week", "month"]
Rfc3339 = str

ranking = {}


async def get_ranking(smartplug_id: str, when: TimeRange) -> Ranking:
    if when in ranking and smartplug_id in ranking[when]:
        return ranking[when][smartplug_id]
    await calculate_set_ranking(when)
    return ranking[when][smartplug_id]


async def calculate_set_ranking(when: TimeRange):
    global ranking
    ranking[when] = {}

    ranking = await get_ranking_from_influx(when)
    position = 1
    for smartplug_id, consumption in ranking:
        ranking[when][smartplug_id] = position
        position += 1


async def get_ranking_from_influx(when):
    time_from, time_to = get_time_range(when)
    query = f"SELECT sum(value) FROM power WHERE '{time_from}' <= time AND time <= '{time_to}' GROUP BY id"
    async with aioinflux.InfluxDBClient(
            host=config.INFLUX_HOST, port=config.INFLUX_PORT, db=config.INFLUX_DB
    ) as client:
        response = await client.query(query)
        unordered_ranking = []
        for series in response["results"]:
            for point in series["series"]:
                id = point["tags"]["id"]
                value = point["values"][point["columns"].index("sum")]
                unordered_ranking.append((id, value))
        return sorted(unordered_ranking, key=lambda p: p[1], reverse=True)


def get_time_range(when: TimeRange) -> Tuple[Rfc3339, Rfc3339]:
    if when == "today":
        time_from = datetime.datetime.today() - datetime.timedelta(days=1)
    elif when == "week":
        time_from = datetime.datetime.today() - datetime.timedelta(weeks=1)
    elif when == "month":
        time_from = datetime.datetime.today() - datetime.timedelta(days=31)
    else:
        raise Exception("Invalid time-range for ranking. Available: 'today', 'week' and 'month'")
    return rfc339.timestamp_to_rfc3339_localoffset(time_from.timestamp()), rfc339.now_to_rfc3339_localoffset()
