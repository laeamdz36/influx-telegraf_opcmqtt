"""Modulo to insertdata in InfluxDB3 Core"""
from influxdb_client_3 import (InfluxDBClient3, InfluxDBError, Point, WritePrecision,
                               WriteOptions, write_client_options)


def init_conn():
    """Start connection to influx server"""

    host = "http://localhost:8181"
    token = "apiv3_LM_SODQOqGjWUrayvX81i3fw9TrZBWGXGkT6MdDuKQifiSLx5HELA7B6DuKH0BZYEWTKAiDb_y0CmQ2tRZzQ3w"
    database = "new_database"

    return {"host": host, "token": token, "db": database}


def build_point(table: str, tag: dict, values: dict):
    """Build a point for line protocol to weite influxDB"""

    # Device is a dict for {"tag:value"}
    # {"device":"Name of the device"}, example {"device":"PLC_main"}
    # Definition for proyect
    # {"tag":"Name of the tag","tag_value":"Value of the tag"}
    # example {"tag":"device","tag_value":"PLC_main"}
    # values, is the files or data for that device
    # {"temp":10, "cpu":15, "speed":55}
    points: list[Point] = []
    for key, value in values.items():
        points.append(Point(table).tag(
            tag.get("tag"), tag.get("tag_value")).field(key, value))

    return points
