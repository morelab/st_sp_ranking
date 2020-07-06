import datetime
from typing import Union, Tuple, Dict

import aioinflux
import strict_rfc3339 as rfc339

from st_sp_ranking import config

RankingPosition = int
RankingAmount = int
TimeRange = Union["today", "week", "month"]
Rfc3339 = str


async def get_ranking(
    smartplug_id: str, when: TimeRange
) -> Tuple[RankingPosition, RankingAmount]:
    ranking = await get_calculate_ranking(when)
    if smartplug_id not in ranking:
        raise ValueError(f"There is no ranking data for {smartplug_id}")
    return ranking[smartplug_id], len(ranking)


async def get_calculate_ranking(when: TimeRange) -> Dict[str, RankingPosition]:
    ranking = {}
    tupled_ranking = await get_ranking_from_influx(when)
    position = 1
    for smartplug_id, consumption in tupled_ranking:
        ranking[smartplug_id] = position
        position += 1
    return ranking


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
                value = point["values"][0][point["columns"].index("sum")]
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
        raise Exception(
            "Invalid time-range for ranking. Available: 'today', 'week' and 'month'"
        )
    return (
        rfc339.timestamp_to_rfc3339_localoffset(time_from.timestamp()),
        rfc339.now_to_rfc3339_localoffset(),
    )
