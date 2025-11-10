import time
from py_plc.plc_classes import PLCcmplx
from influxdb_client_3 import (InfluxDBClient3, InfluxDBError, Point, WritePrecision,
                               WriteOptions, write_client_options)


def config_server():
    """Config the target server"""

    # Need to write all complete address
    host = "http://localhost:8181"
    token = "apiv3_LM_SODQOqGjWUrayvX81i3fw9TrZBWGXGkT6MdDuKQifiSLx5HELA7B6DuKH0BZYEWTKAiDb_y0CmQ2tRZzQ3w"
    database = "new_database"

    return {"host": host, "token": token, "db": database}


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
    wco = write_client_options(success_callback=success,
                               error_callback=error,
                               retry_callback=retry,
                               write_options=write_options)

    conf = config_server()
    # create point
    plc1 = PLCcmplx("192.168.10.10")
    try:
        while True:
            # plc1.read_tags()
            r = plc1.read_tag("gb_temperature")
            print(r)
            points = [Point("PLC_MAIN").tag(
                "PLC_NAME", "CMPLX_1").field("temperature", r[1])]
            with InfluxDBClient3(host=conf.get("host"),
                                 token=conf.get("token"),
                                 database=conf.get("db"),
                                 write_client_options=wco) as client:
                client.write(points, write_precision='s')
            # time.sleep(3)
    except KeyboardInterrupt as e:
        print("Program finished")
        raise e
