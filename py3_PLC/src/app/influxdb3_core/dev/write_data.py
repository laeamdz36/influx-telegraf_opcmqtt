"""
Development module to write data into a InfluxDB3 database with line protocol
"""
import time
import random
from influxdb_client_3 import (InfluxDBClient3, InfluxDBError, Point, WritePrecision,
                               WriteOptions, write_client_options)


def get_num():
    """Return a random number"""

    return random.randint(1, 10)


def config_server():
    """Config the target server"""

    # Need to write all complete address
    host = "http://localhost:8181"
    token = "apiv3_LM_SODQOqGjWUrayvX81i3fw9TrZBWGXGkT6MdDuKQifiSLx5HELA7B6DuKH0BZYEWTKAiDb_y0CmQ2tRZzQ3w"
    database = "new_database"

    return {"host": host, "token": token, "db": database}


def get_point():
    """Return a point line protocol"""

    point = [Point("Dev_table").tag(
        "ValueTag", "Random1").field("integer", get_num())]

    return point


def success(self, data: str):
    print(f"Successfully wrote batch: data: {data}")


def error(self, data: str, exception: InfluxDBError):
    print(
        f"Failed writing batch: config: {self}, data: {data} due: {exception}")


def retry(self, data: str, exception: InfluxDBError):
    print(
        f"Failed retry writing batch: config: {self}, data: {data} retry: {exception}")


if __name__ == "__main__":

    # Configure options for batch writing.
    write_options = WriteOptions(batch_size=500,
                                 flush_interval=10_000,
                                 jitter_interval=2_000,
                                 retry_interval=5_000,
                                 max_retries=5,
                                 max_retry_delay=30_000,
                                 exponential_base=2)

    # Create an options dict that sets callbacks and WriteOptions.
    wco = write_client_options(success_callback=success,
                               error_callback=error,
                               retry_callback=retry,
                               write_options=write_options)

    # Instantiate a synchronous instance of the client with your
    # InfluxDB credentials and write options, such as Gzip threshold, default tags,
    # and timestamp precision. Default precision is nanosecond ('ns').
    # retrive server config
    conf = config_server()
    for i in range(100):
        points = get_point()
        with InfluxDBClient3(host=conf.get("host"),
                             token=conf.get("token"),
                             database=conf.get("db"),
                             write_client_options=wco) as client:

            client.write(points, write_precision='s')
        time.sleep(5)
