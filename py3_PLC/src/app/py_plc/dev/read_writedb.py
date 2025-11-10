from influxdb_client_3 import (InfluxDBClient3, InfluxDBError, Point, WritePrecision,
                               WriteOptions, write_client_options)


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


if __name__ == "__main__":

    # tag dev
    table = "Table1"
    tag = {"tag": "PLC", "tag_value": "PLC_MAIN"}
    values = {"temp1": 15, "hum1": 30}
    ps = build_point(table, tag, values)
    print(ps)
